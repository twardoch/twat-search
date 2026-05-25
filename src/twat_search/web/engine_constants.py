# this_file: src/twat_search/web/engine_constants.py
"""
Constants defining engine names and utility functions for standardization.

This module is separate to avoid circular dependencies between engines and config.
"""

# Engine name constants for use throughout the codebase
# These constants should be used instead of string literals
from __future__ import annotations

from twat_search.web.provider_catalog import get_friendly_name, list_known_provider_codes

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
GOOGLE_SCRAPER = "google_scraper"
GOOGLE_SERPAPI = "google_serpapi"
JINA = "jina"
PPLX = "pplx"
SEARCH1API = "search1api"
SERPER = "serper"
TAVILY = "tavily"
YOU = "you"
YOU_NEWS = "you_news"

# Falla-based engines
GOOGLE_FALLA = "google_falla"
BING_FALLA = "bing_falla"
DUCKDUCKGO_FALLA = "duckduckgo_falla"
AOL_FALLA = "aol_falla"
ASK_FALLA = "ask_falla"
DOGPILE_FALLA = "dogpile_falla"
GIBIRU_FALLA = "gibiru_falla"
MOJEEK_FALLA = "mojeek_falla"
QWANT_FALLA = "qwant_falla"
YAHOO_FALLA = "yahoo_falla"
YANDEX_FALLA = "yandex_falla"


# Complete list of all known engines and planned 2.0 providers.
ALL_POSSIBLE_ENGINES = list_known_provider_codes(include_planned=True)

# Dictionary of friendly names for engines.
ENGINE_FRIENDLY_NAMES = {engine_code: get_friendly_name(engine_code) for engine_code in ALL_POSSIBLE_ENGINES}


def standardize_engine_name(engine_name: str) -> str:
    """Standardize engine name by replacing hyphens with underscores.

    Args:
        engine_name: The engine name to standardize

    Returns:
        The standardized engine name
    """
    return engine_name.replace("-", "_")
