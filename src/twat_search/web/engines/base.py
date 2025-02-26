# this_file: src/twat_search/web/engines/base.py
"""
Base class and factory functions for search engines.

This module defines the abstract base class that all search engines must
implement, as well as functions to register and instantiate engines.
"""
from __future__ import annotations

import abc
import asyncio
import random
from typing import Any, ClassVar

import httpx

from twat_search.web.config import EngineConfig
from twat_search.web.exceptions import SearchError
from twat_search.web.models import SearchResult

# List of user agents to rotate for scrapers to avoid blocking
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
]


class SearchEngine(abc.ABC):
    """
    Abstract base class for all search engines.

    All search engine implementations must subclass this and implement
    the search method.
    """

    engine_code: ClassVar[str] = ''  # Class attribute that must be defined by subclasses
    # User-friendly name for display purposes
    friendly_engine_name: ClassVar[str] = ''

    # Class attributes for environment variables
    # Override with engine-specific names
    env_api_key_names: ClassVar[list[str]] = []
    # Override with engine-specific names
    env_enabled_names: ClassVar[list[str]] = []
    # Override with engine-specific names
    env_params_names: ClassVar[list[str]] = []

    def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
        """
        Initialize the search engine with configuration and common parameters.

        Args:
            config: Engine configuration
            **kwargs: Additional engine-specific parameters
        """
        self.config = config
        self.kwargs = kwargs

        # Common parameters with default values
        self.num_results = kwargs.get('num_results', 5)
        self.country = kwargs.get('country', None)
        self.language = kwargs.get('language', None)
        self.safe_search = kwargs.get('safe_search', True)
        self.time_frame = kwargs.get('time_frame', None)

        # Settings for robust HTTP requests - can be overridden in kwargs
        self.timeout = kwargs.get('timeout', 10)
        self.retries = kwargs.get('retries', 2)
        self.retry_delay = kwargs.get('retry_delay', 1.0)
        self.use_random_user_agent = kwargs.get('use_random_user_agent', True)

        if not config.enabled:
            msg = f"Engine '{self.engine_code}' is disabled."
            raise SearchError(msg)

    def get_num_results(
        self,
        param_name: str = 'num_results',
        min_value: int = 1,
    ) -> int:
        """
        Get the standardized number of results to return, respecting user preference.

        This method should be used by all engine implementations to ensure
        the num_results parameter is consistently respected.

        Args:
            param_name: The engine-specific parameter name for number of results
                        (e.g., "count", "max_results", etc.)
            min_value: The minimum value that the engine accepts

        Returns:
            The number of results to request
        """
        # First try the engine-specific parameter name if provided in kwargs
        value = self.kwargs.get(param_name)
        if value is not None:
            return max(min_value, int(value))

        # Then try the standard num_results parameter
        if self.num_results is not None:
            return max(min_value, self.num_results)

        # Finally check config default params
        default = self.config.default_params.get(
            param_name,
        ) or self.config.default_params.get('num_results')
        if default is not None:
            return max(min_value, int(default))

        # Return a reasonable default
        return 5

    async def make_http_request(
        self,
        url: str,
        method: str = 'GET',
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json_data: Any = None,
        timeout: float | None = None,
        retries: int | None = None,
        retry_delay: float | None = None,
    ) -> httpx.Response:
        """
        Make a robust HTTP request with built-in retries and configurable settings.

        This method is designed to make HTTP requests more robust, especially for scrapers
        that might be blocked or rate-limited.

        Args:
            url: The URL to request
            method: HTTP method (GET, POST, etc.)
            headers: HTTP headers to include
            params: URL parameters
            json_data: JSON data for request body
            timeout: Request timeout in seconds
            retries: Number of retries on failure
            retry_delay: Delay between retries in seconds

        Returns:
            httpx.Response: The HTTP response

        Raises:
            SearchError: If all request attempts fail
        """
        # Set defaults if not provided
        actual_timeout = self.timeout if timeout is None else timeout
        actual_retries = self.retries if retries is None else retries
        actual_retry_delay = self.retry_delay if retry_delay is None else retry_delay

        # Build headers with random user agent if enabled
        if headers is None:
            headers = {}

        if self.use_random_user_agent and 'user-agent' not in {k.lower() for k in headers}:
            headers['User-Agent'] = random.choice(USER_AGENTS)

        attempt = 0
        last_error = None

        while attempt <= actual_retries:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params,
                        json=json_data,
                        timeout=actual_timeout,
                    )
                    response.raise_for_status()
                    return response
            except (httpx.RequestError, httpx.HTTPStatusError) as exc:
                last_error = exc
                attempt += 1
                if attempt <= actual_retries:
                    # Add jitter to retry delay to avoid thundering herd effect
                    jitter = random.uniform(0.5, 1.5)
                    await asyncio.sleep(actual_retry_delay * jitter)

        # If we got here, all attempts failed
        msg = f"Engine '{self.engine_code}': HTTP request failed after {actual_retries + 1} attempts: {last_error}"
        raise SearchError(msg)

    @abc.abstractmethod
    async def search(self, query: str) -> list[SearchResult]:
        """
        Search using this engine.

        Args:
            query: The search query

        Returns:
            List of search results
        """
        pass


# Registry of available search engines
_engine_registry: dict[str, type[SearchEngine]] = {}


def register_engine(engine_class: type[SearchEngine]) -> type[SearchEngine]:
    """
    Register a search engine class.

    Args:
        engine_class: The search engine class to register

    Returns:
        The registered search engine class
    """
    _engine_registry[engine_class.engine_code] = engine_class

    # Auto-generate environment variable names if not explicitly set
    if not hasattr(engine_class, 'env_api_key_names'):
        engine_class.env_api_key_names = [
            f"{engine_class.engine_code.upper()}_API_KEY",
        ]
    if not hasattr(engine_class, 'env_enabled_names'):
        engine_class.env_enabled_names = [
            f"{engine_class.engine_code.upper()}_ENABLED",
        ]
    if not hasattr(engine_class, 'env_params_names'):
        engine_class.env_params_names = [
            f"{engine_class.engine_code.upper()}_DEFAULT_PARAMS",
        ]

    # Set friendly_name if not defined but it exists in ENGINE_FRIENDLY_NAMES
    if not engine_class.friendly_engine_name:
        try:
            from twat_search.web.engines import ENGINE_FRIENDLY_NAMES

            engine_class.friendly_engine_name = ENGINE_FRIENDLY_NAMES.get(
                engine_class.engine_code,
                engine_class.engine_code,
            )
        except ImportError:
            engine_class.friendly_engine_name = engine_class.engine_code

    return engine_class


def get_engine(engine_name: str, config: EngineConfig, **kwargs: Any) -> SearchEngine:
    """
    Get a search engine instance by name.

    Args:
        engine_name: The name of the engine to get
        config: Engine configuration
        **kwargs: Additional engine-specific parameters

    Returns:
        An instance of the requested search engine
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
