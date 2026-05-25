# this_file: src/twat_search/web/engine_constants.py
"""
Constants defining engine names and utility functions for standardization.

This module is separate to avoid circular dependencies between engines and config.
"""

# Engine name constants for use throughout the codebase
# These constants should be used instead of string literals
from __future__ import annotations

from twat_search.web.provider_catalog import canonical_provider_code, get_friendly_name, list_known_provider_codes

DEFAULT_NUM_RESULTS = 5

BING_SCRAPER = "bing_scraper"
AISEARCH = "aisearch"
APIFY = "apify"
BRAVE = "brave"
BRAVE_NEWS = "brave_news"
CRITIQUE = "critique"
DATAFORSEO = "dataforseo"
DUCKDUCKGO = "duckduckgo"
EXA = "exa"
FIRECRAWL = "firecrawl"
GOOGLE_HASDATA = "google_hasdata"
GOOGLE_HASDATA_FULL = "google_hasdata_full"
GOOGLE_CSE = "google_cse"
GITHUB_SEARCH = "github_search"
GENSEE = "gensee"
GOOGLE_SCRAPER = "google_scraper"
GOOGLE_SERPAPI = "google_serpapi"
JINA = "jina"
LANGSEARCH = "langsearch"
MAPLESERP = "mapleserp"
PPLX = "pplx"
PLUGIN_SEARCH = "plugin_search"
SEARCH1API = "search1api"
SEARCH_CANS = "search_cans"
SERPER = "serper"
TAVILY = "tavily"
YOU = "you"
YOU_NEWS = "you_news"

# Browser-engine providers backed by the bundled Playwright scraper adapter.
GOOGLE_BROWSER = "google_browser"
BING_BROWSER = "bing_browser"
DUCKDUCKGO_BROWSER = "duckduckgo_browser"
AOL_BROWSER = "aol_browser"
ASK_BROWSER = "ask_browser"
DOGPILE_BROWSER = "dogpile_browser"
GIBIRU_BROWSER = "gibiru_browser"
MOJEEK_BROWSER = "mojeek_browser"
QWANT_BROWSER = "qwant_browser"
YAHOO_BROWSER = "yahoo_browser"
YANDEX_BROWSER = "yandex_browser"


# Complete list of all known engines and planned 2.0 providers.
ALL_POSSIBLE_ENGINES = list_known_provider_codes(include_planned=True)

# Dictionary of friendly names for engines.
ENGINE_FRIENDLY_NAMES = {engine_code: get_friendly_name(engine_code) for engine_code in ALL_POSSIBLE_ENGINES}


def standardize_engine_name(engine_name: str) -> str:
    """Standardize engine name and resolve catalog aliases.

    Args:
        engine_name: The engine name to standardize

    Returns:
        The standardized engine name
    """
    return canonical_provider_code(engine_name)
