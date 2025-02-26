# this_file: src/twat_search/web/engines/__init__.py
"""
Package containing various search engine implementations for the twat_search.web API.

Each module in this package implements one or more search engines
that can be used with the API.
"""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

from loguru import logger

from twat_search.web.engine_constants import (
    ALL_POSSIBLE_ENGINES,
    BING_SCRAPER,
    BING_SEARCHIT,
    BRAVE,
    BRAVE_NEWS,
    CRITIQUE,
    DUCKDUCKGO,
    ENGINE_FRIENDLY_NAMES,
    GOOGLE_HASDATA,
    GOOGLE_HASDATA_FULL,
    GOOGLE_SCRAPER,
    GOOGLE_SEARCHIT,
    GOOGLE_SERPAPI,
    PPLX,
    QWANT_SEARCHIT,
    TAVILY,
    YANDEX_SEARCHIT,
    YOU,
    YOU_NEWS,
    standardize_engine_name,
)
from twat_search.web.models import SearchResult

# Import engine constants from the dedicated module

# Initialize __all__ list with engine name constants
__all__ = [
    # Helper functions
    "ALL_POSSIBLE_ENGINES",
    # Engine name constants
    "BING_SCRAPER",
    "BING_SEARCHIT",
    "BRAVE",
    "BRAVE_NEWS",
    "CRITIQUE",
    "DUCKDUCKGO",
    "ENGINE_FRIENDLY_NAMES",
    "GOOGLE_HASDATA",
    "GOOGLE_HASDATA_FULL",
    "GOOGLE_SCRAPER",
    "GOOGLE_SEARCHIT",
    "GOOGLE_SERPAPI",
    "PPLX",
    "QWANT_SEARCHIT",
    "TAVILY",
    "YANDEX_SEARCHIT",
    "YOU",
    "YOU_NEWS",
    "available_engine_functions",
    "get_available_engines",
    "get_engine_function",
    "is_engine_available",
    "standardize_engine_name",
]

# Dict to track available engine functions - using Any type to avoid signature incompatibilities
available_engine_functions: dict[str, Any] = {}

# Import base functionality first
try:
    from twat_search.web.engines.base import SearchEngine, get_engine, get_registered_engines, register_engine

    __all__.extend(
        ["SearchEngine", "get_engine", "get_registered_engines", "register_engine"],
    )
except ImportError:
    pass

# Import each engine module and add its components to __all__ if successful
try:
    from twat_search.web.engines.brave import BraveNewsSearchEngine, BraveSearchEngine, brave, brave_news

    available_engine_functions["brave"] = brave
    available_engine_functions["brave_news"] = brave_news
    __all__.extend(
        ["BraveNewsSearchEngine", "BraveSearchEngine", "brave", "brave_news"],
    )
except ImportError:
    pass

# Try to import SerpAPI engine
try:
    from twat_search.web.engines.serpapi import SerpApiSearchEngine, google_serpapi

    available_engine_functions["google_serpapi"] = google_serpapi
    __all__.extend(["SerpApiSearchEngine", "google_serpapi"])
except (ImportError, AttributeError):
    pass

try:
    from twat_search.web.engines.tavily import TavilySearchEngine, tavily

    available_engine_functions["tavily"] = tavily
    __all__.extend(["TavilySearchEngine", "tavily"])
except ImportError:
    pass

try:
    from twat_search.web.engines.pplx import PerplexitySearchEngine, pplx

    available_engine_functions["pplx"] = pplx
    __all__.extend(["PerplexitySearchEngine", "pplx"])
except ImportError:
    pass

try:
    from twat_search.web.engines.you import YouNewsSearchEngine, YouSearchEngine, you, you_news

    available_engine_functions["you"] = you
    available_engine_functions["you_news"] = you_news
    __all__.extend(
        ["YouNewsSearchEngine", "YouSearchEngine", "you", "you_news"],
    )
except ImportError:
    pass

try:
    from twat_search.web.engines.critique import CritiqueSearchEngine, critique

    available_engine_functions["critique"] = critique
    __all__.extend(["CritiqueSearchEngine", "critique"])
except ImportError:
    pass

try:
    from twat_search.web.engines.duckduckgo import DuckDuckGoSearchEngine, duckduckgo

    available_engine_functions["duckduckgo"] = duckduckgo
    __all__.extend(["DuckDuckGoSearchEngine", "duckduckgo"])
except ImportError:
    pass

# Try to import bing_scraper engine
try:
    from twat_search.web.engines.bing_scraper import BingScraperSearchEngine, bing_scraper

    available_engine_functions["bing_scraper"] = bing_scraper
    __all__.extend(["BingScraperSearchEngine", "bing_scraper"])
except ImportError as e:
    logger.warning(f"Failed to import bing_scraper: {e}")

# Import HasData engines
try:
    from twat_search.web.engines.hasdata import (
        HasDataGoogleEngine,
        HasDataGoogleLightEngine,
        hasdata_google,
        hasdata_google_full,
    )

    available_engine_functions["hasdata_google"] = hasdata_google
    available_engine_functions["hasdata_google_full"] = hasdata_google_full
    __all__.extend(
        [
            "HasDataGoogleEngine",
            "HasDataGoogleLightEngine",
            "hasdata_google",
            "hasdata_google_full",
        ],
    )
except ImportError:
    pass

# Import Google Scraper engine
try:
    from twat_search.web.engines.google_scraper import GoogleScraperEngine, google_scraper

    available_engine_functions["google_scraper"] = google_scraper
    __all__.extend(["GoogleScraperEngine", "google_scraper"])
except (ImportError, SyntaxError) as e:
    logger.warning(f"Failed to import google_scraper module: {e}")

# Import Searchit engines
try:
    from twat_search.web.engines.searchit import (
        BingSearchitEngine,
        GoogleSearchitEngine,
        QwantSearchitEngine,
        YandexSearchitEngine,
        bing_searchit,
        google_searchit,
        qwant_searchit,
        yandex_searchit,
    )

    available_engine_functions["bing_searchit"] = bing_searchit
    available_engine_functions["google_searchit"] = google_searchit
    available_engine_functions["qwant_searchit"] = qwant_searchit
    available_engine_functions["yandex_searchit"] = yandex_searchit
    __all__.extend(
        [
            "BingSearchitEngine",
            "GoogleSearchitEngine",
            "QwantSearchitEngine",
            "YandexSearchitEngine",
            "bing_searchit",
            "google_searchit",
            "qwant_searchit",
            "yandex_searchit",
        ],
    )
except (ImportError, SyntaxError) as e:
    logger.warning(f"Failed to import searchit module: {e}")


# Add helper functions
def is_engine_available(engine_name: str) -> bool:
    """Check if an engine is available (its dependencies are installed).

    Args:
        engine_name: Name of the engine to check

    Returns:
        True if the engine is available, False otherwise
    """
    standardized_name = standardize_engine_name(engine_name)
    return standardized_name in available_engine_functions


def get_engine_function(
    engine_name: str,
) -> Callable[..., Coroutine[Any, Any, list[SearchResult]]] | None:
    """Get the function for a specific engine.

    Args:
        engine_name: Name of the engine

    Returns:
        The engine function if available, None otherwise
    """
    standardized_name = standardize_engine_name(engine_name)
    return available_engine_functions.get(standardized_name)


def get_available_engines() -> list[str]:
    """Get a list of all available engine names.

    Returns:
        List of available engine names
    """
    return list(available_engine_functions.keys())
