# this_file: src/twat_search/web/api.py
"""Multi-engine web search API for twat-search.

This module is the main entry point for programmatic web searches.  The
top-level :func:`search` coroutine fans a query out to multiple search engines
concurrently and returns a unified list of :class:`~twat_search.web.models.SearchResult`
objects.

Supported engines (registered in ``twat_search/web/engines/``)
---------------------------------------------------------------
API, scraper, browser, and LLM-assisted engines are registered behind the same
provider-neutral interface, plus a ``mock`` engine for tests.

Most engines require an API key in the environment.  Check each engine module's
``PROVIDER_HELP`` dict for the exact variable name.

Usage::

    import asyncio
    from twat_search.web.api import search

    results = asyncio.run(search("open source LLMs", engines=["brave", "duckduckgo"]))
    for r in results:
        print(r.title, r.url)

Passing ``engines=None`` tries all engines that are configured in the active
:class:`~twat_search.web.config.Config`.  Results from every engine are
merged into a single flat list; the order reflects the engine preference
and the order results were returned.

Engine-specific parameters can be passed as keyword arguments prefixed with
the engine name, e.g. ``brave_country="GB"`` sets the ``country`` parameter
only for the Brave engine.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from twat_cache import ucache

from twat_search.web.browser import BrowserChallengeError
from twat_search.web.config import Config, EngineConfig
from twat_search.web.engines import standardize_engine_name
from twat_search.web.engines.base import SearchEngine, get_engine, get_registered_engines
from twat_search.web.exceptions import SearchError
from twat_search.web.llm import (
    decompose_search_query,
    rerank_search_results,
    rewrite_search_query,
    synthesize_search_answer,
)
from twat_search.web.routes import get_route_policy, select_route_engines
from twat_search.web.transports import enrich_engine_request

if TYPE_CHECKING:
    from collections.abc import Coroutine

from twat_search.web.models import (
    EngineOutcome,
    EngineExecutionContext,
    EngineParameterSet,
    EngineRequest,
    SearchFailure,
    SearchRequest,
    SearchResponse,
    SearchResult,
)

logger = logging.getLogger(__name__)


def get_engine_params(
    engine_name: str,
    engines: list[str],
    kwargs: dict,
    common_params: dict,
) -> dict:
    """Return final provider params for a single engine."""
    return build_engine_execution_context(
        engine_name=engine_name,
        engines=engines,
        kwargs=kwargs,
        common_params=common_params,
    ).params


def build_engine_parameter_set(
    engine_name: str,
    engines: list[str],
    kwargs: dict,
    common_params: dict,
) -> EngineParameterSet:
    """Parse raw engine kwargs into typed common, engine-specific, and passthrough groups."""
    std_engine_name = standardize_engine_name(engine_name)
    std_engines = [standardize_engine_name(e) for e in engines]
    prefixes = tuple(dict.fromkeys((std_engine_name, engine_name)))

    engine_specific = {}
    for key, value in kwargs.items():
        if key.startswith(std_engine_name + "_"):
            engine_specific[key[len(std_engine_name) + 1 :]] = value
        elif key.startswith(engine_name + "_"):
            engine_specific[key[len(engine_name) + 1 :]] = value

    control_keys = {"engines", "common_params", "route", "route_policy", "engine_request", "execution_context"}
    non_prefixed = {
        key: value
        for key, value in kwargs.items()
        if key not in control_keys
        and key not in common_params
        and not any(key.startswith(engine + "_") for engine in std_engines + engines)
    }

    params = {**common_params, **engine_specific, **non_prefixed}
    param_sources = dict.fromkeys(common_params, "common")
    param_sources.update(dict.fromkeys(engine_specific, "engine_specific"))
    param_sources.update(dict.fromkeys(non_prefixed, "passthrough"))

    return EngineParameterSet(
        engine=std_engine_name,
        requested_engines=tuple(std_engines),
        common_params=common_params,
        engine_specific_params=engine_specific,
        passthrough_params=non_prefixed,
        params=params,
        param_sources=param_sources,
        engine_specific_prefixes=prefixes,
    )


def build_engine_execution_context(
    engine_name: str,
    engines: list[str],
    kwargs: dict,
    common_params: dict,
) -> EngineExecutionContext:
    """
    Build a typed engine execution context by merging:
    - parameters prefixed with the engine name,
    - any non-prefixed parameters,
    - and the common parameters.
    """
    parameter_set = build_engine_parameter_set(
        engine_name=engine_name,
        engines=engines,
        kwargs=kwargs,
        common_params=common_params,
    )

    return EngineExecutionContext(
        engine=parameter_set.engine,
        route=kwargs.get("route"),
        request_policy=kwargs.get("request_policy"),
        parameter_set=parameter_set,
        params=parameter_set.params,
        param_sources=parameter_set.param_sources,
        engine_specific_prefixes=parameter_set.engine_specific_prefixes,
    )


def _classify_failure(error: Exception) -> tuple[str, bool]:
    """Classify provider failures into first-class failure kinds."""
    if isinstance(error, BrowserChallengeError):
        if error.evidence.blocked:
            return "block", True
        if error.evidence.needs_consent:
            return "block", False
        return "provider_error", True
    message = str(error).lower()
    error_type = type(error).__name__.lower()
    if "api key" in message or "unauthorized" in message or "forbidden" in message:
        return "auth", False
    if "timeout" in message or "timeout" in error_type:
        return "timeout", True
    if "captcha" in message or "blocked" in message or "rate limit" in message:
        return "block", True
    if "parse" in message or "json" in message:
        return "parse", False
    if "schema" in message or "field" in message:
        return "schema_drift", False
    return "provider_error", True


def _failure_details(error: Exception) -> dict[str, Any]:
    """Extract serializable diagnostic details from known exception types."""
    if isinstance(error, BrowserChallengeError):
        return error.evidence.to_failure_details()
    return {}


def init_engine_task(
    engine_name: str,
    query: str,
    config: Config,
    engine_request: EngineRequest | None = None,
    **kwargs: Any,
) -> tuple[str, Coroutine[Any, Any, EngineOutcome]] | EngineOutcome:
    """
    Initialize a search engine and create a task for searching.

    This function handles the initialization of a search engine and creates
    a coroutine for performing the search. It includes robust error handling
    to prevent failures from affecting other engines.

    Args:
        engine_name: Name of the engine to initialize
        query: Search query
        config: Configuration object
        **kwargs: Additional parameters for the engine

    Returns:
        A tuple of (engine_name, search_coroutine) or a failed outcome if initialization fails
    """
    # Standardize engine name for lookups
    std_engine_name = standardize_engine_name(engine_name)

    # Get engine configuration from the canonical provider code.
    engine_config = config.engines.get(std_engine_name)
    if not engine_config:
        logger.warning(f"Engine '{std_engine_name}' not configured, using default configuration.")
        engine_config = EngineConfig(enabled=True)

    # Extract the num_results from the kwargs if present
    num_results = kwargs.get("num_results")
    if num_results is not None:
        logger.debug(f"Initializing engine '{engine_name}' with num_results={num_results}")

    try:
        # Build engine-specific parameters
        execution_context = build_engine_execution_context(
            engine_name=engine_name,
            engines=kwargs.get("engines", []),
            kwargs=kwargs,
            common_params=kwargs.get("common_params", {}),
        )
        engine_request = engine_request or EngineRequest(
            engine=std_engine_name,
            query=query,
            params=execution_context.params,
            execution=execution_context,
            route=kwargs.get("route"),
        )
        if engine_request.execution is None:
            engine_request = engine_request.model_copy(update={"execution": execution_context})
        engine_request = enrich_engine_request(engine_request)

        # Create engine instance
        engine_instance: SearchEngine = get_engine(
            engine_name,
            engine_config,
            **engine_request.params,
        )

        logger.info(f"🔍 Querying engine: {engine_name}")

        # Create a wrapper coroutine that handles exceptions
        async def search_with_error_handling() -> EngineOutcome:
            try:
                results = await engine_instance.search(engine_request.query)
                if results:
                    return EngineOutcome(engine=engine_name, status="ok", request=engine_request, results=results)
                return EngineOutcome(
                    engine=engine_name,
                    status="empty",
                    request=engine_request,
                    failure=SearchFailure(
                        engine=engine_name,
                        kind="empty",
                        message=f"Engine '{engine_name}' returned no results",
                    ),
                )
            except Exception as e:
                logger.error(f"Search with engine '{engine_name}' failed: {e}")
                kind, retryable = _classify_failure(e)
                return EngineOutcome(
                    engine=engine_name,
                    status="failed",
                    request=engine_request,
                    failure=SearchFailure(
                        engine=engine_name,
                        kind=kind,
                        message=str(e),
                        exception_type=type(e).__name__,
                        retryable=retryable,
                        details=_failure_details(e),
                    ),
                )

        return engine_name, search_with_error_handling()
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        # Provide more specific error messages based on error type
        if "API key" in error_msg:
            logger.error(
                f"Failed to initialize engine '{engine_name}': Missing or invalid API key. "
                f"Check your environment variables or configuration.",
            )
        elif "disabled" in error_msg:
            logger.warning(f"Engine '{engine_name}' is disabled. Enable it in your configuration to use it.")
        else:
            logger.error(f"Failed to initialize engine '{engine_name}': {error_type}: {error_msg}")

        return EngineOutcome(
            engine=engine_name,
            status="failed",
            request=engine_request,
            failure=SearchFailure(
                engine=engine_name,
                kind="initialization",
                message=error_msg,
                exception_type=error_type,
                retryable=False,
            ),
        )


# @ucache(maxsize=1000, ttl=3600)  # Cache 1000 searches for 1 hour
async def search_detailed(
    query: str,
    engines: list[str] | None = None,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool = True,
    time_frame: str | None = None,
    config: Config | None = None,
    route: str | None = "best",
    strict_mode: bool = True,
    **kwargs: Any,
) -> SearchResponse:
    """
    Search across multiple engines and return structured per-engine outcomes.

    Args:
        query: The search query
        engines: List of engine names to use (or None for all enabled)
        num_results: Number of results to request from each engine (default: 5)
        country: Country code for search results
        language: Language code for search results
        safe_search: Whether to enable safe search (default: True)
        time_frame: Time frame for results (e.g., "day", "week", "month")
        config: Optional custom configuration
        route: Route preset to use when engines is None
        strict_mode: If True (default), flat `search()` raises when all requested engines fail to initialize
        **kwargs: Additional engine-specific parameters

    Returns:
        Detailed response with flat results, outcomes, and failures

    Raises:
        SearchError: If no engines can be initialized or if no engines are specified
    """
    rewrite_query_override = kwargs.pop("rewrite_query", None)
    decompose_query_override = kwargs.pop("decompose_query", None)
    rerank_results_override = kwargs.pop("rerank_results", None)
    synthesize_answer_override = kwargs.pop("synthesize_answer", None)
    request_params = dict(kwargs)
    if rewrite_query_override is not None:
        request_params["rewrite_query"] = bool(rewrite_query_override)
    if decompose_query_override is not None:
        request_params["decompose_query"] = bool(decompose_query_override)
    if rerank_results_override is not None:
        request_params["rerank_results"] = bool(rerank_results_override)
    if synthesize_answer_override is not None:
        request_params["synthesize_answer"] = bool(synthesize_answer_override)
    route_policy = get_route_policy(route)
    config = config or Config()
    result_processing_policy = config.result_processing.as_result_processing_policy()
    request = SearchRequest(
        query=query,
        engines=engines,
        route=route_policy.name,
        route_policy=route_policy,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        strict_mode=strict_mode,
        result_processing=result_processing_policy,
        params=request_params,
    )
    flattened_results: list[SearchResult] = []
    outcomes: list[EngineOutcome] = []

    try:
        search_query = query
        search_queries = [query]
        should_rewrite_query = (
            config.llm.query_rewrite if rewrite_query_override is None else bool(rewrite_query_override)
        )
        should_decompose_query = (
            config.llm.query_decomposition if decompose_query_override is None else bool(decompose_query_override)
        )
        should_rerank_results = (
            config.llm.result_rerank if rerank_results_override is None else bool(rerank_results_override)
        )
        should_synthesize_answer = (
            config.llm.answer_synthesis if synthesize_answer_override is None else bool(synthesize_answer_override)
        )
        if should_rewrite_query:
            try:
                llm_config = (
                    config.llm
                    if rewrite_query_override is None
                    else config.llm.model_copy(update={"query_rewrite": bool(rewrite_query_override)})
                )
                search_query = await rewrite_search_query(query, llm_config)
                request.params["llm_rewritten_query"] = search_query
            except Exception as e:
                logger.warning(f"LLM query rewrite failed; using original query: {e}")
                request.params["llm_rewrite_error"] = str(e)
        decompose_config = (
            config.llm
            if decompose_query_override is None
            else config.llm.model_copy(update={"query_decomposition": bool(decompose_query_override)})
        )
        search_queries = [search_query]
        if should_decompose_query:
            try:
                search_queries = await decompose_search_query(search_query, decompose_config)
                request.params["llm_search_queries"] = search_queries
                request.params["llm_decomposition"] = {
                    "model": decompose_config.model,
                    "prompt_version": "twat-search-decomposition-v1",
                    "query_count": len(search_queries),
                }
            except Exception as e:
                logger.warning(f"LLM query decomposition failed; using single query: {e}")
                request.params["llm_decomposition_error"] = str(e)
                search_queries = [search_query]
        rerank_config = (
            config.llm
            if rerank_results_override is None
            else config.llm.model_copy(update={"result_rerank": bool(rerank_results_override)})
        )
        synthesis_config = (
            config.llm
            if synthesize_answer_override is None
            else config.llm.model_copy(update={"answer_synthesis": bool(synthesize_answer_override)})
        )

        # Check if engines is an empty list (explicitly passed as [])
        if engines is not None and len(engines) == 0:
            msg = "No search engines configured"
            logger.error(msg)
            raise SearchError(msg)

        # Determine which engines to use
        if engines is None:
            engines_to_try = select_route_engines(
                config=config,
                route=route,
                available_engines=set(get_registered_engines()),
            )
        else:
            engines_to_try = engines

        # Check if engines_to_try is empty and raise an error
        if not engines_to_try:
            route_context = f" for route '{route}'" if engines is None else ""
            msg = f"No search engines configured{route_context}"
            logger.error(msg)
            raise SearchError(msg)

        # Log the number of results requested
        logger.debug(f"Search requested with num_results={num_results}")

        # Normalize engine names
        engines_to_try = [standardize_engine_name(e) for e in engines_to_try]

        request_policy = config.request_policy.as_request_policy(config.proxies)

        # Common parameters for all engines
        common_params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
            "browser_config": config.browser,
            "proxy_config": config.proxies,
            **request_policy.engine_kwargs(),
        }

        # First attempt with specific engines or all enabled engines
        engine_names: list[str] = []
        tasks: list[Coroutine[Any, Any, EngineOutcome]] = []
        task_queries: list[tuple[str, int, str]] = []
        failed_engines: list[str] = []

        # Prepare all engine tasks
        for engine_name in engines_to_try:
            try:
                # For the mock engine, ensure result_count is set correctly
                if engine_name == "mock":
                    # Check for engine-specific parameter first (mock_result_count)
                    if f"{engine_name}_result_count" in kwargs:
                        kwargs["result_count"] = kwargs[f"{engine_name}_result_count"]
                    # If not found, check if there's a default result_count in the engine config
                    elif "result_count" not in kwargs:
                        engine_config = config.engines.get(engine_name)
                        if engine_config and engine_config.default_params:
                            default_result_count = engine_config.default_params.get("result_count")
                            if default_result_count is not None:
                                kwargs["result_count"] = default_result_count

                # Pass all parameters including kwargs to init_engine_task
                for query_index, current_query in enumerate(search_queries):
                    task_result = init_engine_task(
                        engine_name,
                        current_query,
                        config,
                        engines=engines_to_try,
                        common_params=common_params,
                        route=route,
                        request_policy=request_policy,
                        num_results=num_results,
                        **kwargs,
                    )

                    # Check if initialization was successful
                    if isinstance(task_result, EngineOutcome):
                        outcomes.append(task_result)
                        failed_engines.append(engine_name)
                    else:
                        engine_names.append(task_result[0])
                        tasks.append(task_result[1])
                        task_queries.append((engine_name, query_index, current_query))
            except Exception as e:
                logger.warning(f"Unexpected error initializing engine '{engine_name}': {e}")
                failed_engines.append(engine_name)
                continue  # Log the exception and continue

        # Log any failed engines
        if failed_engines:
            failed_engines_str = ", ".join(failed_engines)
            logger.warning(f"Failed to initialize engines: {failed_engines_str}")

        # If no engines could be initialized and no structured failures exist, fail loudly.
        if not tasks and not outcomes:
            msg = f"No search engines could be initialized from selected engines: {', '.join(engines_to_try)}"
            logger.error(msg)
            raise SearchError(msg)

        # Execute all search tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True) if tasks else []

        for (engine_name, query_index, current_query), result in zip(task_queries, results, strict=False):
            if isinstance(result, Exception):
                logger.error(
                    f"Search with engine '{engine_name}' failed: {result}",
                )
                kind, retryable = _classify_failure(result)
                outcomes.append(
                    EngineOutcome(
                        engine=engine_name,
                        status="failed",
                        failure=SearchFailure(
                            engine=engine_name,
                            kind=kind,
                            message=str(result),
                            exception_type=type(result).__name__,
                            retryable=retryable,
                        ),
                    ),
                )
            elif isinstance(result, EngineOutcome):
                outcomes.append(result)
                result_count = len(result.results)
                if result_count > 0:
                    logger.info(
                        f"✅ Engine '{engine_name}' returned {result_count} results",
                    )
                    enriched_results = []
                    for provider_result in result.results:
                        raw = dict(provider_result.raw or {})
                        raw["query_fanout"] = {
                            "query": current_query,
                            "query_index": query_index,
                            "query_count": len(search_queries),
                        }
                        enriched_results.append(provider_result.model_copy(update={"raw": raw}))
                    result.results = enriched_results
                    flattened_results.extend(result.results)
                else:
                    logger.info(
                        f"⚠️ Engine '{engine_name}' returned no results",
                    )
            else:
                logger.warning(
                    f"⚠️ Engine '{engine_name}' returned unexpected type: {type(result)}",
                )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise

    if flattened_results and "result_processing_policy" in locals():
        flattened_results, result_metadata = result_processing_policy.process_results(flattened_results)
        request.params["result_processing"] = result_metadata

    # Log the total number of results found
    if flattened_results and "should_rerank_results" in locals() and should_rerank_results:
        try:
            flattened_results = await rerank_search_results(query, flattened_results, rerank_config)
            request.params["llm_rerank"] = {
                "model": rerank_config.model,
                "result_count": len(flattened_results),
            }
        except Exception as e:
            logger.warning(f"LLM result rerank failed; using provider order: {e}")
            request.params["llm_rerank_error"] = str(e)

    logger.info(f"Total results found across all engines: {len(flattened_results)}")
    failures = [outcome.failure for outcome in outcomes if outcome.failure is not None]
    answer = None
    if flattened_results and "should_synthesize_answer" in locals() and should_synthesize_answer:
        try:
            answer = await synthesize_search_answer(query, flattened_results, failures, synthesis_config)
            if answer is not None:
                request.params["llm_answer"] = {
                    "model": synthesis_config.model,
                    "cited_url_count": len(answer.cited_urls),
                    "source_failure_count": len(answer.source_failures),
                }
        except Exception as e:
            logger.warning(f"LLM answer synthesis failed; returning results without answer: {e}")
            request.params["llm_answer_error"] = str(e)

    return SearchResponse(
        request=request,
        engines=outcomes,
        results=flattened_results,
        failures=failures,
        answer=answer,
    )


async def search(
    query: str,
    engines: list[str] | None = None,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool = True,
    time_frame: str | None = None,
    config: Config | None = None,
    route: str | None = "best",
    strict_mode: bool = True,
    **kwargs: Any,
) -> list[SearchResult]:
    """Search across multiple engines and return a flat result list."""
    response = await search_detailed(
        query=query,
        engines=engines,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        config=config,
        route=route,
        strict_mode=strict_mode,
        **kwargs,
    )

    init_failure_kinds = {"initialization", "auth"}
    only_initialization_failures = bool(response.engines) and all(
        outcome.status == "failed" and outcome.failure is not None and outcome.failure.kind in init_failure_kinds
        for outcome in response.engines
    )
    if (strict_mode or engines) and only_initialization_failures:
        engine_names = engines or [outcome.engine for outcome in response.engines]
        msg = f"No search engines could be initialized from requested engines: {', '.join(engine_names)}"
        logger.error(msg)
        raise SearchError(msg)

    return response.results
