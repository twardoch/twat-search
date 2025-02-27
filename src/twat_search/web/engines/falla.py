#!/usr/bin/env python3
# /// script
# dependencies = ["selenium", "lxml", "requests"]
# ///
# this_file: src/twat_search/web/engines/falla.py
"""
Search engine wrappers based on the Falla scraping library.

This module provides search engine implementations that use the embedded
Falla library for scraping search engine results.
"""

import logging

from pydantic import HttpUrl

from twat_search.web.engines.base import SearchEngine
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

logger = logging.getLogger(__name__)

# List of available Falla engine names
FALLA_AVAILABLE_ENGINES = [
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

# Track if Falla engines are available
_falla_available = False
# Flag set to True once the first Falla-based engine is initialized
_falla_initialized = False


def is_falla_available() -> bool:
    """
    Check if Falla search engines are available.

    Returns:
        bool: True if Falla engines are available, False otherwise
    """
    global _falla_available
    if not _falla_initialized:
        # Check if Falla can be initialized without errors
        try:
            # Basic check - create and validate a Google instance
            _check_engine = Google()
            _falla_available = True
        except Exception as e:
            logger.warning(f"Falla engines are not available: {e}")
            _falla_available = False

    return _falla_available


class FallaSearchEngine(SearchEngine):
    """Base class for all Falla-based search engines."""

    # To be overridden by subclasses
    engine_code = "falla"
    friendly_engine_name = "Falla Search"
    _falla_engine_class = Falla  # Base engine class

    def __init__(self, config, **kwargs):
        """Initialize the Falla search engine."""
        super().__init__(config, **kwargs)

        # Create the Falla engine instance
        self._falla_engine = self._create_engine_instance()

        # Set global flag
        global _falla_initialized
        _falla_initialized = True

    def _create_engine_instance(self):
        """
        Create an instance of the Falla engine.

        Returns:
            Falla: Instance of the Falla engine class
        """
        # Create a new instance - passing name parameter for most engines
        # Falla engines require a name parameter
        return self._falla_engine_class(name=self.engine_code)

    async def search(self, query: str, **_kwargs) -> list[SearchResult]:
        """
        Perform a search using the Falla engine.

        Args:
            query: Search query
            **_kwargs: Additional search parameters (ignored for Falla engines)

        Returns:
            list[SearchResult]: List of search results

        Raises:
            EngineError: If the search fails
        """
        try:
            # Perform the search
            raw_results = self._falla_engine.search(query=query)

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
        except Exception as e:
            logger.error(f"Search failed: {e!s}")
            msg = f"Search failed: {e!s}"
            raise EngineError(self.engine_code, msg) from e


# Define engine classes for specific Falla engines
class GoogleFallaEngine(FallaSearchEngine):
    """Google search implementation using Falla."""

    engine_code = "google_falla"
    friendly_engine_name = "Google (Falla)"
    _falla_engine_class = Google


class BingFallaEngine(FallaSearchEngine):
    """Bing search implementation using Falla."""

    engine_code = "bing_falla"
    friendly_engine_name = "Bing (Falla)"
    _falla_engine_class = Bing


class DuckDuckGoFallaEngine(FallaSearchEngine):
    """DuckDuckGo search implementation using Falla."""

    engine_code = "duckduckgo_falla"
    friendly_engine_name = "DuckDuckGo (Falla)"
    _falla_engine_class = DuckDuckGo


class YahooFallaEngine(FallaSearchEngine):
    """Yahoo search implementation using Falla."""

    engine_code = "yahoo_falla"
    friendly_engine_name = "Yahoo (Falla)"
    _falla_engine_class = Yahoo


class AskFallaEngine(FallaSearchEngine):
    """Ask.com search implementation using Falla."""

    engine_code = "ask_falla"
    friendly_engine_name = "Ask.com (Falla)"
    _falla_engine_class = Ask


class AolFallaEngine(FallaSearchEngine):
    """AOL search implementation using Falla."""

    engine_code = "aol_falla"
    friendly_engine_name = "AOL (Falla)"
    _falla_engine_class = Aol


class DogpileFallaEngine(FallaSearchEngine):
    """Dogpile search implementation using Falla."""

    engine_code = "dogpile_falla"
    friendly_engine_name = "Dogpile (Falla)"
    _falla_engine_class = DogPile


class GibiruFallaEngine(FallaSearchEngine):
    """Gibiru search implementation using Falla."""

    engine_code = "gibiru_falla"
    friendly_engine_name = "Gibiru (Falla)"
    _falla_engine_class = Gibiru


class MojeekFallaEngine(FallaSearchEngine):
    """Mojeek search implementation using Falla."""

    engine_code = "mojeek_falla"
    friendly_engine_name = "Mojeek (Falla)"
    _falla_engine_class = Mojeek


class QwantFallaEngine(FallaSearchEngine):
    """Qwant search implementation using Falla."""

    engine_code = "qwant_falla"
    friendly_engine_name = "Qwant (Falla)"
    _falla_engine_class = Qwant


class YandexFallaEngine(FallaSearchEngine):
    """Yandex search implementation using Falla."""

    engine_code = "yandex_falla"
    friendly_engine_name = "Yandex (Falla)"
    _falla_engine_class = Yandex
