#!/usr/bin/env python3
# /// script
# dependencies = ["playwright", "lxml", "requests"]
# ///
# this_file: src/twat_search/web/engines/falla.py
"""
Browser search wrappers based on the bundled scraper library.

This module exposes provider-neutral browser engine codes while reusing the
embedded scraper implementation internally.
"""

import logging
from typing import Any, ClassVar

from pydantic import HttpUrl
from twat_cache import ucache

from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.engines.lib_falla.core import (
    Aol,
    Ask,
    Bing,
    DogPile,
    DuckDuckGo,
    Falla,
    Gibiru,
    Google,
    Mojeek,
    Qwant,
    Yahoo,
    Yandex,
)
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from twat_search.web.browser_transport import BrowserChallengeError

logger = logging.getLogger(__name__)

# List of bundled browser adapter names.
BROWSER_AVAILABLE_ENGINES = [
    "google",
    "bing",
    "duckduckgo",
    "yahoo",
    "ask",
    "aol",
    "dogpile",
    "gibiru",
    "mojeek",
    "qwant",
    "yandex",
]

# Track if bundled browser engines are available.
_browser_engines_available = False
# Flag set to True once the first bundled browser engine is initialized.
_browser_engines_initialized = False


def are_browser_engines_available() -> bool:
    """
    Check if bundled browser search engines are available.

    Returns:
        bool: True if browser engines are available, False otherwise
    """
    global _browser_engines_available  # noqa: PLW0603
    if not _browser_engines_initialized:
        # Check if the embedded scraper can be initialized without errors.
        try:
            # Basic check - create and validate a Google instance
            # Google constructor doesn't take a name parameter
            _check_engine = Google()
            _browser_engines_available = True
        except Exception as e:
            logger.warning(f"Browser engines are not available: {e}")
            _browser_engines_available = False

    return _browser_engines_available


class BrowserScraperSearchEngine(SearchEngine):
    """Base class for bundled browser-backed search engines."""

    # To be overridden by subclasses
    engine_code = "browser_scraper"
    friendly_engine_name = "Browser scraper search"
    env_api_key_names: ClassVar[list[str]] = []

    # Note: This is marked as a ClassVar for type-checking, but will be overridden
    # by subclasses with their specific engine classes (Google, Bing, etc.)
    # The actual implementation doesn't use Falla directly
    _browser_engine_class: Any = Google  # Use Google as a default callable

    def __init__(self, config: Any, **kwargs: Any) -> None:
        """Initialize the browser search engine."""
        super().__init__(config, **kwargs)

        # Create the bundled browser adapter instance.
        self._browser_engine = self._create_engine_instance()
        self._browser_engine.browser_config = kwargs.get("browser_config", self._browser_engine.browser_config)
        self._browser_engine.proxy_config = kwargs.get("proxy_config", self._browser_engine.proxy_config)

        # Set global flag
        global _browser_engines_initialized  # noqa: PLW0603
        _browser_engines_initialized = True

    def _create_engine_instance(self) -> Falla:
        """
        Create an instance of the browser engine.

        Returns:
            Falla: Instance of the embedded scraper engine class
        """
        # Create a new instance - each subclass of Falla has its own __init__
        # that handles initialization without explicit parameters
        return self._browser_engine_class()  # type: ignore[no-any-return]

    # @ucache(maxsize=500, ttl=3600)  # Cache 500 searches for 1 hour
    async def search(self, query: str, **_kwargs: Any) -> list[SearchResult]:
        """
        Perform a search using the bundled browser engine.

        Args:
            query: Search query
            **_kwargs: Additional search parameters ignored by browser engines

        Returns:
            list[SearchResult]: List of search results

        Raises:
            EngineError: If the search fails
        """
        try:
            # The bundled adapters return list[dict[str, str]] from search_async.
            # Cast return value to ensure type safety
            raw_results: list[dict[str, str]] = await self._browser_engine.search_async(query=query)

            # Convert to SearchResult objects
            results = []
            for i, item in enumerate(raw_results):
                # Validate URL
                url = item.get("link", "")
                if not url:
                    continue

                try:
                    # Create search result object - Pydantic will validate the URL
                    result = SearchResult(
                        title=item.get("title", ""),
                        url=HttpUrl(url),  # Convert to HttpUrl type
                        snippet=item.get("snippet", ""),
                        source=self.engine_code,
                        rank=i + 1,
                        raw=item,
                    )
                    results.append(result)
                except ValueError as url_err:
                    # Log invalid URL but continue processing other results
                    logger.warning(f"Invalid URL '{url}' in {self.engine_code} result: {url_err}")
                    continue

            return self.limit_results(results)
        except BrowserChallengeError:
            raise
        except Exception as e:
            logger.error(f"Search failed: {e!s}")
            msg = f"Search failed: {e!s}"
            raise EngineError(self.engine_code, msg) from e


# Define engine classes for specific browser engines.
@register_engine
class GoogleBrowserEngine(BrowserScraperSearchEngine):
    """Google browser search implementation."""

    engine_code = "google_browser"
    friendly_engine_name = "Google browser search"
    _browser_engine_class = Google


@register_engine
class BingBrowserEngine(BrowserScraperSearchEngine):
    """Bing browser search implementation."""

    engine_code = "bing_browser"
    friendly_engine_name = "Bing browser search"
    _browser_engine_class = Bing


@register_engine
class DuckDuckGoBrowserEngine(BrowserScraperSearchEngine):
    """DuckDuckGo browser search implementation."""

    engine_code = "duckduckgo_browser"
    friendly_engine_name = "DuckDuckGo browser search"
    _browser_engine_class = DuckDuckGo


@register_engine
class YahooBrowserEngine(BrowserScraperSearchEngine):
    """Yahoo browser search implementation."""

    engine_code = "yahoo_browser"
    friendly_engine_name = "Yahoo browser search"
    _browser_engine_class = Yahoo


@register_engine
class AskBrowserEngine(BrowserScraperSearchEngine):
    """Ask.com browser search implementation."""

    engine_code = "ask_browser"
    friendly_engine_name = "Ask.com browser search"
    _browser_engine_class = Ask


@register_engine
class AolBrowserEngine(BrowserScraperSearchEngine):
    """AOL browser search implementation."""

    engine_code = "aol_browser"
    friendly_engine_name = "AOL browser search"
    _browser_engine_class = Aol


@register_engine
class DogpileBrowserEngine(BrowserScraperSearchEngine):
    """Dogpile browser search implementation."""

    engine_code = "dogpile_browser"
    friendly_engine_name = "Dogpile browser search"
    _browser_engine_class = DogPile


@register_engine
class GibiruBrowserEngine(BrowserScraperSearchEngine):
    """Gibiru browser search implementation."""

    engine_code = "gibiru_browser"
    friendly_engine_name = "Gibiru browser search"
    _browser_engine_class = Gibiru


@register_engine
class MojeekBrowserEngine(BrowserScraperSearchEngine):
    """Mojeek browser search implementation."""

    engine_code = "mojeek_browser"
    friendly_engine_name = "Mojeek browser search"
    _browser_engine_class = Mojeek


@register_engine
class QwantBrowserEngine(BrowserScraperSearchEngine):
    """Qwant browser search implementation."""

    engine_code = "qwant_browser"
    friendly_engine_name = "Qwant browser search"
    _browser_engine_class = Qwant


@register_engine
class YandexBrowserEngine(BrowserScraperSearchEngine):
    """Yandex browser search implementation."""

    engine_code = "yandex_browser"
    friendly_engine_name = "Yandex browser search"
    _browser_engine_class = Yandex


# Convenience functions for direct API access
# These match the function naming convention used in the module


async def _search_browser_engine(query: str, engine: str, **kwargs: Any) -> list[SearchResult]:
    """Run a browser-engine search without importing the API at module load."""
    from twat_search.web.api import search  # noqa: PLC0415

    return await search(query, engines=[engine], **kwargs)


async def google_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Google search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "google_browser", **kwargs)


async def bing_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Bing search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "bing_browser", **kwargs)


async def duckduckgo_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a DuckDuckGo search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "duckduckgo_browser", **kwargs)


async def yahoo_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Yahoo search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "yahoo_browser", **kwargs)


async def ask_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform an Ask.com search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "ask_browser", **kwargs)


async def aol_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform an AOL search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "aol_browser", **kwargs)


async def dogpile_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Dogpile search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "dogpile_browser", **kwargs)


async def gibiru_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Gibiru search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "gibiru_browser", **kwargs)


async def mojeek_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Mojeek search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "mojeek_browser", **kwargs)


async def qwant_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Qwant search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "qwant_browser", **kwargs)


async def yandex_browser(query: str, **kwargs: Any) -> list[SearchResult]:
    """
    Perform a Yandex search using the browser engine.

    Args:
        query: Search query
        **kwargs: Additional parameters passed to the search function

    Returns:
        list[SearchResult]: Search results
    """
    return await _search_browser_engine(query, "yandex_browser", **kwargs)
