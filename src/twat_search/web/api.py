# this_file: src/twat_search/web/api.py

"""
Main API module for the web search functionality.

This module provides the main search function that allows searching across
multiple engines with a unified interface.
"""

import asyncio
import logging
from typing import Any

from .config import Config
from .models import SearchResult
from .engines.base import SearchEngine, get_engine
from .exceptions import SearchError

# Set up logging
logger = logging.getLogger(__name__)


async def search(
    query: str,
    engines: list[str] | None = None,
    config: Config | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Performs a web search using the specified search engines.

    This function provides a unified interface to search across multiple engines
    and returns results in a consistent format.

    Args:
        query: The search query string.
        engines: A list of engine names to use (e.g., ["brave", "google"]).
                 If None, use all configured engines.
        config: A Config object. If None, use the default configuration.
        **kwargs: Engine-specific parameters (override defaults).
                 Use engine_param to override for all engines.
                 Use engine_name_param to override for a specific engine.

    Returns:
        A list of SearchResult objects.

    Raises:
        SearchError: If no engines are configured or if all searches fail.
    """
    # Load configuration if not provided
    if config is None:
        config = Config()

    # Use all configured engines if none specified
    if engines is None:
        engines = list(config.engines.keys())

    if not engines:
        msg = "No search engines configured."
        raise SearchError(msg)

    # Create search tasks for each engine
    search_tasks = []
    for engine_name in engines:
        try:
            engine_config = config.engines.get(engine_name)
            if engine_config is None:
                logger.warning(f"Engine '{engine_name}' not configured.")
                continue

            # Get engine-specific overrides from kwargs
            # example: brave_count=10 would override count just for Brave
            engine_kwargs = {
                k[len(engine_name) + 1 :]: v
                for k, v in kwargs.items()
                if k.startswith(engine_name + "_")
            }

            # Copy general kwargs (without engine prefix)
            general_kwargs = {
                k: v
                for k, v in kwargs.items()
                if not any(k.startswith(e + "_") for e in engines)
            }

            # Merge general kwargs and engine-specific kwargs
            # Engine-specific kwargs take precedence
            merged_kwargs = {**general_kwargs, **engine_kwargs}

            # Create the engine instance
            engine_instance: SearchEngine = get_engine(
                engine_name, engine_config, **merged_kwargs
            )

            # Log that we're querying this engine
            logger.info(f"🔍 Querying engine: {engine_name}")

            # Add the search task
            search_tasks.append((engine_name, engine_instance.search(query)))

        except Exception as e:
            # Log and continue with other engines
            logger.error(f"Error initializing engine '{engine_name}': {e}")
            continue

    if not search_tasks:
        msg = "No search engines could be initialized."
        raise SearchError(msg)

    # Run all searches concurrently
    engine_names = [name for name, _ in search_tasks]
    search_coroutines = [task for _, task in search_tasks]
    results = await asyncio.gather(*search_coroutines, return_exceptions=True)

    # Process results
    flattened_results: list[SearchResult] = []
    for engine_name, result in zip(engine_names, results, strict=False):
        if isinstance(result, Exception):
            logger.error(f"Search with engine '{engine_name}' failed: {result}")
        elif isinstance(result, list):  # Check if results exist and is a list
            logger.info(f"✅ Engine '{engine_name}' returned {len(result)} results")
            flattened_results.extend(result)
        else:
            logger.info(
                f"⚠️ Engine '{engine_name}' returned no results or unexpected type: {type(result)}"
            )

    return flattened_results
