"""Multi-engine web search API for twat-search.

This module is the main entry point for programmatic web searches.  The
top-level :func:`search` coroutine fans a query out to multiple search engines
concurrently and returns a unified list of :class:`~twat_search.web.models.SearchResult`
objects.

Supported engines (registered in ``twat_search/web/engines/``)
---------------------------------------------------------------
brave, bing_scraper, google_scraper, duckduckgo, tavily, you, pplx
(Perplexity), serpapi, hasdata, falla, critique, and a ``mock`` engine for
testing.

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

from twat_search.web.config import Config, EngineConfig
from twat_search.web.engines import standardize_engine_name
from twat_search.web.engines.base import SearchEngine, get_engine, get_registered_engines
from twat_search.web.exceptions import SearchError
from twat_search.web.routes import select_route_engines

if TYPE_CHECKING:
    from collections.abc import Coroutine

from twat_search.web.models import EngineOutcome, SearchFailure, SearchRequest, SearchResponse, SearchResult

logger = logging.getLogger(__name__)


def get_engine_params(
    engine_name: str,
    engines: list[str],
    kwargs: dict,
    common_params: dict,
) -> dict:
    """
    Build engine-specific parameters by merging:
    - parameters prefixed with the engine name,
    - any non-prefixed parameters,
    - and the common parameters.
    """
    # Standardize engine name for parameter lookup
    std_engine_name = standardize_engine_name(engine_name)

    # Look for parameters with both standardized and original name prefixes
    engine_specific = {}
    for k, v in kwargs.items():
        if k.startswith(std_engine_name + "_"):
            engine_specific[k[len(std_engine_name) + 1 :]] = v
        elif k.startswith(engine_name + "_"):  # For backward compatibility
            engine_specific[k[len(engine_name) + 1 :]] = v

    # Get non-prefixed parameters
    std_engines = [standardize_engine_name(e) for e in engines]
    non_prefixed = {k: v for k, v in kwargs.items() if not any(k.startswith(e + "_") for e in std_engines + engines)}

    return {**common_params, **engine_specific, **non_prefixed}


def _classify_failure(error: Exception) -> tuple[str, bool]:
    """Classify provider failures into first-class failure kinds."""
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


def init_engine_task(
    engine_name: str,
    query: str,
    config: Config,
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

    # Get engine configuration
    engine_config = config.engines.get(std_engine_name)
    if not engine_config:
        # Fallback to non-standardized name for backward compatibility
        engine_config = config.engines.get(engine_name)
        if not engine_config:
            logger.warning(f"Engine '{engine_name}' not configured, using default configuration.")
            engine_config = EngineConfig(enabled=True)

    # Extract the num_results from the kwargs if present
    num_results = kwargs.get("num_results")
    if num_results is not None:
        logger.debug(f"Initializing engine '{engine_name}' with num_results={num_results}")

    try:
        # Build engine-specific parameters
        engine_params = get_engine_params(
            engine_name=engine_name,
            engines=kwargs.get("engines", []),
            kwargs=kwargs,
            common_params=kwargs.get("common_params", {}),
        )

        # Create engine instance
        engine_instance: SearchEngine = get_engine(
            engine_name,
            engine_config,
            **engine_params,
        )

        logger.info(f"🔍 Querying engine: {engine_name}")

        # Create a wrapper coroutine that handles exceptions
        async def search_with_error_handling() -> EngineOutcome:
            try:
                results = await engine_instance.search(query)
                if results:
                    return EngineOutcome(engine=engine_name, status="ok", results=results)
                return EngineOutcome(
                    engine=engine_name,
                    status="empty",
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
                    failure=SearchFailure(
                        engine=engine_name,
                        kind=kind,
                        message=str(e),
                        exception_type=type(e).__name__,
                        retryable=retryable,
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
        strict_mode: If True (default), don't fall back to other engines when specific engines are requested
        **kwargs: Additional engine-specific parameters

    Returns:
        Detailed response with flat results, outcomes, and failures

    Raises:
        SearchError: If no engines can be initialized or if no engines are specified
    """
    request = SearchRequest(
        query=query,
        engines=engines,
        route=route,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        strict_mode=strict_mode,
        params=kwargs,
    )
    flattened_results: list[SearchResult] = []
    outcomes: list[EngineOutcome] = []

    try:
        # Initialize configuration if not provided
        config = config or Config()

        # Check if engines is an empty list (explicitly passed as [])
        if engines is not None and len(engines) == 0:
            msg = "No search engines configured"
            logger.error(msg)
            raise SearchError(msg)

        # Determine which engines to use
        explicit_engines_requested = engines is not None and len(engines) > 0
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

        # Common parameters for all engines
        common_params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
            "proxy_url": config.proxies.httpx_proxy_url(),
        }

        # First attempt with specific engines or all enabled engines
        engine_names: list[str] = []
        tasks: list[Coroutine[Any, Any, EngineOutcome]] = []
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
                task_result = init_engine_task(
                    engine_name,
                    query,
                    config,
                    engines=engines_to_try,
                    common_params=common_params,
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
            except Exception as e:
                logger.warning(f"Unexpected error initializing engine '{engine_name}': {e}")
                failed_engines.append(engine_name)
                continue  # Log the exception and continue

        # Log any failed engines
        if failed_engines:
            failed_engines_str = ", ".join(failed_engines)
            logger.warning(f"Failed to initialize engines: {failed_engines_str}")

        # If no engines could be initialized and no structured failures exist.
        if not tasks and not outcomes:
            if strict_mode or explicit_engines_requested:
                # In strict mode or when engines were explicitly requested, don't fall back
                # This is important to prevent unintended fallbacks
                msg = f"No search engines could be initialized from requested engines: {', '.join(engines_to_try)}"
                logger.error(msg)
                raise SearchError(msg)

            # Try with any available engine as a fallback
            logger.warning("Falling back to any available search engine...")
            for engine_name in get_registered_engines():
                try:
                    # Pass all parameters including kwargs to init_engine_task
                    task_result = init_engine_task(
                        engine_name,
                        query,
                        config,
                        engines=[engine_name],
                        common_params=common_params,
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
                        logger.info(f"Successfully fell back to engine: {engine_name}")
                        break
                except Exception as e:
                    logger.debug(f"Failed to initialize fallback engine {engine_name}: {e}")
                    continue

            if not tasks:
                msg = "No search engines could be initialized"
                logger.error(msg)
                raise SearchError(msg)

        # Execute all search tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True) if tasks else []

        for engine_name, result in zip(engine_names, results, strict=False):
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

    # Log the total number of results found
    logger.info(f"Total results found across all engines: {len(flattened_results)}")
    failures = [outcome.failure for outcome in outcomes if outcome.failure is not None]
    return SearchResponse(
        request=request,
        engines=outcomes,
        results=flattened_results,
        failures=failures,
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
