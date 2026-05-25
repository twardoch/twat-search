# this_file: src/twat_search/web/engines/__init__.py
"""
Package containing various search engine implementations for the twat_search.web API.

Each module in this package implements one or more search engines
that can be used with the API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from loguru import logger

from twat_search.web.engine_constants import (
    ALL_POSSIBLE_ENGINES,
    AOL_BROWSER,
    AISEARCH,
    APIFY,
    ASK_BROWSER,
    BING_BROWSER,
    BING_SCRAPER,
    BRAVE,
    BRAVE_NEWS,
    CRITIQUE,
    DATAFORSEO,
    DOGPILE_BROWSER,
    DUCKDUCKGO,
    DUCKDUCKGO_BROWSER,
    ENGINE_FRIENDLY_NAMES,
    EXA,
    FIRECRAWL,
    GIBIRU_BROWSER,
    GENSEE,
    GITHUB_SEARCH,
    GOOGLE_BROWSER,
    GOOGLE_CSE,
    GOOGLE_HASDATA,
    GOOGLE_HASDATA_FULL,
    GOOGLE_SCRAPER,
    GOOGLE_SERPAPI,
    JINA,
    LANGSEARCH,
    MAPLESERP,
    MOJEEK_BROWSER,
    PPLX,
    PLUGIN_SEARCH,
    QWANT_BROWSER,
    SEARCH1API,
    SEARCH_CANS,
    SERPER,
    TAVILY,
    YAHOO_BROWSER,
    YANDEX_BROWSER,
    YOU,
    YOU_NEWS,
    standardize_engine_name,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

    from twat_search.web.models import SearchResult

# Import engine constants from the dedicated module

# Initialize __all__ list with engine name constants
__all__ = [
    # Helper functions
    "AISEARCH",
    "ALL_POSSIBLE_ENGINES",
    "AOL_BROWSER",
    "APIFY",
    "ASK_BROWSER",
    "BING_BROWSER",
    # Engine name constants
    "BING_SCRAPER",
    "BRAVE",
    "BRAVE_NEWS",
    "CRITIQUE",
    "DATAFORSEO",
    "DOGPILE_BROWSER",
    "DUCKDUCKGO",
    "DUCKDUCKGO_BROWSER",
    "ENGINE_FRIENDLY_NAMES",
    "EXA",
    "FIRECRAWL",
    "GENSEE",
    "GIBIRU_BROWSER",
    "GITHUB_SEARCH",
    # Browser-engine providers backed by the bundled Playwright scraper adapter.
    "GOOGLE_BROWSER",
    "GOOGLE_CSE",
    "GOOGLE_HASDATA",
    "GOOGLE_HASDATA_FULL",
    "GOOGLE_SCRAPER",
    "GOOGLE_SERPAPI",
    "JINA",
    "LANGSEARCH",
    "MAPLESERP",
    "MOJEEK_BROWSER",
    "PLUGIN_SEARCH",
    "PPLX",
    "QWANT_BROWSER",
    "SEARCH1API",
    "SEARCH_CANS",
    "SERPER",
    "TAVILY",
    "YAHOO_BROWSER",
    "YANDEX_BROWSER",
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
    from twat_search.web.engines.base import (
        EngineRegistryEntry,
        SearchEngine,
        get_engine,
        get_engine_registry,
        get_registered_engines,
        register_engine,
    )

    __all__.extend(
        [
            "EngineRegistryEntry",
            "SearchEngine",
            "get_engine",
            "get_engine_registry",
            "get_registered_engines",
            "register_engine",
        ],
    )
except ImportError:
    pass

# Import each engine module and add its components to __all__ if successful
try:
    from twat_search.web.engines.aisearch import AISearchEngine, aisearch

    available_engine_functions["aisearch"] = aisearch
    __all__.extend(["AISearchEngine", "aisearch"])
except ImportError:
    pass

try:
    from twat_search.web.engines.apify import ApifySearchEngine, apify

    available_engine_functions["apify"] = apify
    __all__.extend(["ApifySearchEngine", "apify"])
except ImportError:
    pass

try:
    from twat_search.web.engines.brave import BraveNewsSearchEngine, BraveSearchEngine, brave, brave_news

    available_engine_functions["brave"] = brave
    available_engine_functions["brave_news"] = brave_news
    __all__.extend(
        ["BraveNewsSearchEngine", "BraveSearchEngine", "brave", "brave_news"],
    )
except ImportError:
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
    from twat_search.web.engines.serper import SerperSearchEngine, serper

    available_engine_functions["serper"] = serper
    __all__.extend(["SerperSearchEngine", "serper"])
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
    from twat_search.web.engines.dataforseo import DataForSeoSearchEngine, dataforseo

    available_engine_functions["dataforseo"] = dataforseo
    __all__.extend(["DataForSeoSearchEngine", "dataforseo"])
except ImportError:
    pass

try:
    from twat_search.web.engines.duckduckgo import DuckDuckGoSearchEngine, duckduckgo

    available_engine_functions["duckduckgo"] = duckduckgo
    __all__.extend(["DuckDuckGoSearchEngine", "duckduckgo"])
except ImportError:
    pass

try:
    from twat_search.web.engines.exa import ExaSearchEngine, exa

    available_engine_functions["exa"] = exa
    __all__.extend(["ExaSearchEngine", "exa"])
except ImportError:
    pass

try:
    from twat_search.web.engines.firecrawl import FirecrawlSearchEngine, firecrawl

    available_engine_functions["firecrawl"] = firecrawl
    __all__.extend(["FirecrawlSearchEngine", "firecrawl"])
except ImportError:
    pass

# Try to import bing_scraper engine
try:
    from twat_search.web.engines.bing_scraper import BingScraperSearchEngine, bing_scraper

    available_engine_functions["bing_scraper"] = bing_scraper
    __all__.extend(["BingScraperSearchEngine", "bing_scraper"])
except ImportError as e:
    logger.debug(f"Optional bing_scraper engine is unavailable: {e}")

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

try:
    from twat_search.web.engines.gensee import GenseeSearchEngine, gensee

    available_engine_functions["gensee"] = gensee
    __all__.extend(["GenseeSearchEngine", "gensee"])
except ImportError:
    pass

try:
    from twat_search.web.engines.github_search import GitHubSearchEngine, github_search

    available_engine_functions["github_search"] = github_search
    __all__.extend(["GitHubSearchEngine", "github_search"])
except ImportError:
    pass

try:
    from twat_search.web.engines.google_cse import GoogleCseSearchEngine, google_cse

    available_engine_functions["google_cse"] = google_cse
    __all__.extend(["GoogleCseSearchEngine", "google_cse"])
except ImportError:
    pass

try:
    from twat_search.web.engines.jina import JinaSearchEngine, jina

    available_engine_functions["jina"] = jina
    __all__.extend(["JinaSearchEngine", "jina"])
except ImportError:
    pass

try:
    from twat_search.web.engines.langsearch import LangSearchEngine, langsearch

    available_engine_functions["langsearch"] = langsearch
    __all__.extend(["LangSearchEngine", "langsearch"])
except ImportError:
    pass

try:
    from twat_search.web.engines.mapleserp import MapleSerpSearchEngine, mapleserp

    available_engine_functions["mapleserp"] = mapleserp
    __all__.extend(["MapleSerpSearchEngine", "mapleserp"])
except ImportError:
    pass

try:
    from twat_search.web.engines.search1api import Search1ApiSearchEngine, search1api

    available_engine_functions["search1api"] = search1api
    __all__.extend(["Search1ApiSearchEngine", "search1api"])
except ImportError:
    pass

try:
    from twat_search.web.engines.plugin_search import PluginSearchEngine, SearchPluginSpec, plugin_search

    available_engine_functions["plugin_search"] = plugin_search
    __all__.extend(["PluginSearchEngine", "SearchPluginSpec", "plugin_search"])
except ImportError:
    pass

try:
    from twat_search.web.engines.search_cans import SearchCansSearchEngine, search_cans

    available_engine_functions["search_cans"] = search_cans
    __all__.extend(["SearchCansSearchEngine", "search_cans"])
except ImportError:
    pass

# Import Google Scraper engine
try:
    from twat_search.web.engines.google_scraper import GoogleScraperEngine, google_scraper

    available_engine_functions["google_scraper"] = google_scraper
    __all__.extend(["GoogleScraperEngine", "google_scraper"])
except (ImportError, SyntaxError) as e:
    logger.warning(f"Failed to import google_scraper module: {e}")

# Try to import SerpAPI engine
try:
    from twat_search.web.engines.serpapi import SerpApiSearchEngine, google_serpapi

    available_engine_functions["google_serpapi"] = google_serpapi
    __all__.extend(["SerpApiSearchEngine", "google_serpapi"])
except (ImportError, AttributeError):
    pass


# Import bundled browser-backed engines.
try:
    from twat_search.web.engines.falla import (
        AolBrowserEngine,
        AskBrowserEngine,
        BingBrowserEngine,
        BrowserScraperSearchEngine,
        DogpileBrowserEngine,
        DuckDuckGoBrowserEngine,
        GibiruBrowserEngine,
        GoogleBrowserEngine,
        MojeekBrowserEngine,
        QwantBrowserEngine,
        YahooBrowserEngine,
        YandexBrowserEngine,
        aol_browser,
        are_browser_engines_available,
        ask_browser,
        bing_browser,
        dogpile_browser,
        duckduckgo_browser,
        gibiru_browser,
        google_browser,
        mojeek_browser,
        qwant_browser,
        yahoo_browser,
        yandex_browser,
    )

    # Register engine functions
    if are_browser_engines_available():
        available_engine_functions["google_browser"] = google_browser
        available_engine_functions["bing_browser"] = bing_browser
        available_engine_functions["duckduckgo_browser"] = duckduckgo_browser
        available_engine_functions["yahoo_browser"] = yahoo_browser
        available_engine_functions["ask_browser"] = ask_browser
        available_engine_functions["aol_browser"] = aol_browser
        available_engine_functions["dogpile_browser"] = dogpile_browser
        available_engine_functions["gibiru_browser"] = gibiru_browser
        available_engine_functions["mojeek_browser"] = mojeek_browser
        available_engine_functions["qwant_browser"] = qwant_browser
        available_engine_functions["yandex_browser"] = yandex_browser

    else:
        logger.warning("Browser search engines are not available")

    # Add to __all__
    __all__.extend(
        [
            "AolBrowserEngine",
            "AskBrowserEngine",
            "BingBrowserEngine",
            "BrowserScraperSearchEngine",
            "DogpileBrowserEngine",
            "DuckDuckGoBrowserEngine",
            "GibiruBrowserEngine",
            "GoogleBrowserEngine",
            "MojeekBrowserEngine",
            "QwantBrowserEngine",
            "YahooBrowserEngine",
            "YandexBrowserEngine",
            "aol_browser",
            "are_browser_engines_available",
            "ask_browser",
            "bing_browser",
            "dogpile_browser",
            "duckduckgo_browser",
            "gibiru_browser",
            "google_browser",
            "mojeek_browser",
            "qwant_browser",
            "yahoo_browser",
            "yandex_browser",
        ],
    )
except (ImportError, SyntaxError) as e:
    logger.debug(f"Optional browser engine module is unavailable: {e}")


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
    """Get a list of all available engines.

    Returns:
        List of available engine names
    """
    return list(available_engine_functions.keys())
