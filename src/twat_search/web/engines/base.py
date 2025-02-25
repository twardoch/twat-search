# this_file: src/twat_search/web/engines/base.py

"""
Base class and factory functions for search engines.

This module defines the abstract base class that all search engines must
implement, as well as functions to register and instantiate engines.
"""

import abc
from typing import Any, ClassVar

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from twat_search.web.exceptions import SearchError


class SearchEngine(abc.ABC):
    """
    Abstract base class for all search engines.

    All search engine implementations must subclass this and implement
    the search method.
    """

    name: ClassVar[str] = ""  # Class attribute that must be defined by subclasses

    # Class attributes for environment variables
    env_api_key_names: ClassVar[list[str]] = []  # Override with engine-specific names
    env_enabled_names: ClassVar[list[str]] = []  # Override with engine-specific names
    env_params_names: ClassVar[list[str]] = []  # Override with engine-specific names

    def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
        """
        Initialize the search engine with its configuration.

        Args:
            config: Configuration for this search engine
            **kwargs: Additional engine-specific parameters

        Raises:
            SearchError: If the engine is disabled
        """
        self.config = config
        self.kwargs = kwargs  # Store for later use

        if not self.config.enabled:
            msg = f"Engine '{self.name}' is disabled."
            raise SearchError(msg)

    @abc.abstractmethod
    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search and return a list of SearchResult objects.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        ...


# Registry of available search engines
_engine_registry: dict[str, type[SearchEngine]] = {}


def register_engine(engine_class: type[SearchEngine]) -> type[SearchEngine]:
    """
    Register a search engine class.

    This is typically used as a decorator on search engine classes.

    Args:
        engine_class: The search engine class to register

    Returns:
        The same search engine class (for decorator use)
    """
    # Set default environment variable names if not explicitly defined
    if not engine_class.env_api_key_names:
        engine_class.env_api_key_names = [f"{engine_class.name.upper()}_API_KEY"]

    if not engine_class.env_enabled_names:
        engine_class.env_enabled_names = [f"{engine_class.name.upper()}_ENABLED"]

    if not engine_class.env_params_names:
        engine_class.env_params_names = [f"{engine_class.name.upper()}_DEFAULT_PARAMS"]

    _engine_registry[engine_class.name] = engine_class
    return engine_class


def get_engine(engine_name: str, config: EngineConfig, **kwargs: Any) -> SearchEngine:
    """
    Factory function to get an instance of a search engine.

    Args:
        engine_name: The name of the engine (e.g., "brave", "google")
        config: The EngineConfig object for this engine
        **kwargs: Additional parameters to pass to the engine constructor

    Returns:
        An instance of the SearchEngine subclass

    Raises:
        SearchError: If the engine is not found
    """
    engine_class = _engine_registry.get(engine_name)
    if engine_class is None:
        msg = f"Unknown search engine: {engine_name}"
        raise SearchError(msg)

    return engine_class(config, **kwargs)


def get_registered_engines() -> dict[str, type[SearchEngine]]:
    """
    Get a dictionary of all registered search engines.

    Returns:
        Dictionary mapping engine names to engine classes
    """
    return _engine_registry.copy()
