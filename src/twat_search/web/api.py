from __future__ import annotations

import asyncio
import logging
from collections.abc import Coroutine
from typing import Any

from twat_search.web.config import Config, EngineConfig
from twat_search.web.engines import standardize_engine_name
from twat_search.web.engines.base import SearchEngine, get_engine, get_registered_engines
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
        if k.startswith(std_engine_name + "_"):
            engine_specific[k[len(std_engine_name) + 1 :]] = v
        elif k.startswith(engine_name + "_"):  # For backward compatibility
            engine_specific[k[len(engine_name) + 1 :]] = v

    # Get non-prefixed parameters
    std_engines = [standardize_engine_name(e) for e in engines]
    non_prefixed = {k: v for k, v in kwargs.items() if not any(k.startswith(e + "_") for e in std_engines + engines)}

    return {**common_params, **engine_specific, **non_prefixed}


def init_engine_task(
    engine_name: str,
    query: str,
    config: Config,
    **kwargs: Any,
) -> tuple[str, Coroutine[Any, Any, list[SearchResult]]]:
    """
    Initialize a search engine and create a task for searching.
    """
    # Standardize engine name for lookups
    std_engine_name = standardize_engine_name(engine_name)

    # Get engine configuration
    engine_config = config.engines.get(std_engine_name)
    if not engine_config:
        # Fallback to non-standardized name for backward compatibility
        engine_config = config.engines.get(engine_name)
        if not engine_config:
            logger.warning(f"Engine '{engine_name}' not configured.")
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
        return engine_name, engine_instance.search(query)
    except Exception as e:
        logger.warning(
            f"Failed to initialize engine '{engine_name}': {type(e).__name__}",
        )
        logger.error(f"Error initializing engine '{engine_name}': {e}")
        raise


async def search(
    query: str,
    engines: list[str] | None = None,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool = True,
    time_frame: str | None = None,
    config: Config | None = None,
    strict_mode: bool = True,
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
        strict_mode: If True (default), don't fall back to other engines when specific engines are requested
        **kwargs: Additional engine-specific parameters

    Returns:
        Combined list of search results from all engines

    Raises:
        SearchError: If no engines can be initialized
    """
    flattened_results: list[SearchResult] = []

    try:
        # Initialize configuration if not provided
        config = config or Config()

        # Determine which engines to use
        explicit_engines_requested = engines is not None and len(engines) > 0
        engines_to_try = engines or list(config.engines.keys())

        if not engines_to_try:
            msg = "No search engines configured"
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
        }

        # First attempt with specific engines or all enabled engines
        engine_names: list[str] = []
        tasks: list[Coroutine[Any, Any, list[SearchResult]]] = []
        failed_engines: list[str] = []

        # Prepare all engine tasks
        for engine_name in engines_to_try:
            try:
                # Pass all parameters including kwargs to init_engine_task
                task = init_engine_task(
                    engine_name,
                    query,
                    config,
                    engines=engines_to_try,
                    common_params=common_params,
                    num_results=num_results,
                    **kwargs,
                )
                if task is not None:
                    engine_names.append(task[0])
                    tasks.append(task[1])
            except Exception as e:
                logger.warning(f"Failed to initialize engine '{engine_name}': {e}")
                failed_engines.append(engine_name)
                continue  # Log the exception and continue

        # Log any failed engines
        if failed_engines:
            failed_engines_str = ", ".join(failed_engines)
            logger.warning(f"Failed to initialize engines: {failed_engines_str}")

        # If no engines could be initialized
        if not tasks:
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
                    task = init_engine_task(
                        engine_name,
                        query,
                        config,
                        engines=[engine_name],
                        common_params=common_params,
                        num_results=num_results,
                        **kwargs,
                    )
                    if task is not None:
                        engine_names.append(task[0])
                        tasks.append(task[1])
                        break
                except Exception as e:
                    logger.debug(f"Failed to initialize engine {engine_name}: {e}")
                    continue

            if not tasks:
                msg = "No search engines could be initialized"
                logger.error(msg)
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
