from __future__ import annotations

import asyncio
import logging
from typing import Any

from twat_search.web.config import Config
from twat_search.web.engines import standardize_engine_name
from twat_search.web.engines.base import SearchEngine, get_engine
from twat_search.web.exceptions import SearchError
from twat_search.web.models import SearchResult

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
        if k.startswith(std_engine_name + '_'):
            engine_specific[k[len(std_engine_name) + 1 :]] = v
        elif k.startswith(engine_name + '_'):  # For backward compatibility
            engine_specific[k[len(engine_name) + 1 :]] = v

    # Get non-prefixed parameters
    std_engines = [standardize_engine_name(e) for e in engines]
    non_prefixed = {k: v for k, v in kwargs.items() if not any(k.startswith(e + '_') for e in std_engines + engines)}

    return {**common_params, **engine_specific, **non_prefixed}


def init_engine_task(
    engine_name: str,
    config: Config,
    engines: list[str],
    kwargs: dict,
    common_params: dict,
    query: str,
) -> tuple[str, Any] | None:
    """
    Initialize a search engine task. If the engine is not configured or fails
    to initialize (due to missing dependencies, etc.), return None.
    """
    # Standardize engine name
    std_engine_name = standardize_engine_name(engine_name)

    # Try both standardized and original names for backward compatibility
    engine_config = config.engines.get(std_engine_name)
    if not engine_config:
        engine_config = config.engines.get(engine_name)
        if not engine_config:
            logger.warning(f"Engine '{engine_name}' not configured.")
            return None

    try:
        engine_params = get_engine_params(
            engine_name,
            engines,
            kwargs,
            common_params,
        )
        # Use standardized name to get the engine
        engine_instance: SearchEngine = get_engine(
            std_engine_name,
            engine_config,
            **engine_params,
        )
        logger.info(f"🔍 Querying engine: {engine_name}")
        return engine_name, engine_instance.search(query)
    except (ImportError, KeyError) as e:
        logger.warning(
            f"Engine '{engine_name}' is not available: {e}. The dependency may not be installed.",
        )
        return None
    except Exception as e:
        logger.error(f"Error initializing engine '{engine_name}': {e}")
        return None


async def search(
    query: str,
    engines: list[str] | None = None,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool = True,
    time_frame: str | None = None,
    config: Config | None = None,
    strict_mode: bool = False,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search across multiple engines.

    Args:
        query: The search query
        engines: List of engine names to use (or None for all enabled)
        num_results: Number of results to request from each engine (default: 5)
        country: Country code for search results
        language: Language code for search results
        safe_search: Whether to enable safe search (default: True)
        time_frame: Time frame for results (e.g., "day", "week", "month")
        config: Optional custom configuration
        strict_mode: If True and specific engines are requested, don't fall back to other engines
        **kwargs: Additional engine-specific parameters

    Returns:
        Combined list of search results from all engines

    Raises:
        SearchError: If no engines can be initialized
    """
    flattened_results: list[SearchResult] = []
    try:
        config = config or Config()
        explicit_engines_requested = engines is not None and len(engines) > 0

        # Get the list of engines to try
        engines_to_try = engines or list(config.engines.keys())
        if not engines_to_try:
            msg = 'No search engines configured'
            raise SearchError(msg)

        # Standardize engine names
        engines_to_try = [standardize_engine_name(e) for e in engines_to_try]

        common_params = {
            k: v
            for k, v in {
                'num_results': num_results,
                'country': country,
                'language': language,
                'safe_search': safe_search,
                'time_frame': time_frame,
            }.items()
            if v is not None
        }

        tasks = []
        engine_names = []

        # Track which engines were explicitly requested but failed to initialize
        failed_engines = []

        for engine_name in engines_to_try:
            task = init_engine_task(
                engine_name,
                config,
                engines_to_try,
                kwargs,
                common_params,
                query,
            )
            if task is not None:
                engine_names.append(task[0])
                tasks.append(task[1])
            elif explicit_engines_requested:
                failed_engines.append(engine_name)

        # If strict mode is on, specific engines were requested, and all of them failed,
        # don't try to fall back to other engines
        if strict_mode and explicit_engines_requested and not tasks:
            failed_engines_str = ', '.join(failed_engines)
            msg = f"Requested engines ({failed_engines_str}) could not be initialized. Use strict_mode=False to fall back to other available engines."
            raise SearchError(msg)

        # If no tasks but not in strict mode, try to fall back to default engines
        if not tasks and explicit_engines_requested and not strict_mode:
            logger.warning(
                f"None of the requested engines {engines_to_try} could be initialized. "
                'Falling back to all available engines.',
            )
            # Get all available engines as fallback
            for engine_name in config.engines:
                if engine_name not in engines_to_try:  # Skip already tried engines
                    task = init_engine_task(
                        engine_name,
                        config,
                        [
                            engine_name,
                        ],
                        kwargs,
                        common_params,
                        query,
                    )
                    if task is not None:
                        engine_names.append(task[0])
                        tasks.append(task[1])

        if not tasks:
            msg = 'No search engines could be initialized. Make sure at least one engine dependency is installed.'
            raise SearchError(msg)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for engine_name, result in zip(engine_names, results, strict=False):
            if isinstance(result, Exception):
                logger.error(
                    f"Search with engine '{engine_name}' failed: {result}",
                )
            elif isinstance(result, list):
                logger.info(
                    f"✅ Engine '{engine_name}' returned {len(result)} results",
                )
                flattened_results.extend(result)
            else:
                logger.info(
                    f"⚠️ Engine '{engine_name}' returned no results or unexpected type: {type(result)}",
                )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise

    return flattened_results
