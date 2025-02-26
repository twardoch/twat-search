# this_file: src/twat_search/web/engine_constants.py

"""
Constants defining engine names and utility functions for standardization.

This module is separate to avoid circular dependencies between engines and config.
"""

# Engine name constants for use throughout the codebase
# These constants should be used instead of string literals
BING_ANYWS = "bing_anyws"
BING_SCRAPER = "bing_scraper"
BING_SEARCHIT = "bing_searchit"
BRAVE = "brave"
BRAVE_ANYWS = "brave_anyws"
BRAVE_NEWS = "brave_news"
CRITIQUE = "critique"
DUCKDUCKGO = "duckduckgo"
GOOGLE_ANYWS = "google_anyws"
GOOGLE_HASDATA = "google_hasdata"
GOOGLE_HASDATA_FULL = "google_hasdata_full"
GOOGLE_SCRAPER = "google_scraper"
GOOGLE_SEARCHIT = "google_searchit"
GOOGLE_SERPAPI = "google_serpapi"
PPLX = "pplx"
QWANT_ANYWS = "qwant_anyws"
QWANT_SEARCHIT = "qwant_searchit"
TAVILY = "tavily"
YANDEX_ANYWS = "yandex_anyws"
YANDEX_SEARCHIT = "yandex_searchit"
YOU = "you"
YOU_NEWS = "you_news"


# Complete list of all possible engines
ALL_POSSIBLE_ENGINES = [
    BING_ANYWS,
    BING_SCRAPER,
    BING_SEARCHIT,
    BRAVE_ANYWS,
    BRAVE_NEWS,
    BRAVE,
    CRITIQUE,
    DUCKDUCKGO,
    GOOGLE_ANYWS,
    GOOGLE_HASDATA_FULL,
    GOOGLE_HASDATA,
    GOOGLE_SCRAPER,
    GOOGLE_SEARCHIT,
    GOOGLE_SERPAPI,
    PPLX,
    QWANT_ANYWS,
    QWANT_SEARCHIT,
    TAVILY,
    YANDEX_ANYWS,
    YANDEX_SEARCHIT,
    YOU_NEWS,
    YOU,
]

# Dictionary of friendly names for engines
ENGINE_FRIENDLY_NAMES = {
    BING_ANYWS: "Bing via anywebsearch",
    BING_SCRAPER: "Bing scaper",
    BING_SEARCHIT: "Bing via searchit",
    BRAVE_ANYWS: "Brave via anywebsearch",
    BRAVE_NEWS: "Brave News with API key",
    BRAVE: "Brave with API key",
    CRITIQUE: "Critique Labs with API key",
    DUCKDUCKGO: "DuckDuckGo",
    GOOGLE_ANYWS: "Google via anywebsearch",
    GOOGLE_HASDATA_FULL: "Full Google scraper via HasData with API key",
    GOOGLE_HASDATA: "Light Google scraper via HasData with API key",
    GOOGLE_SCRAPER: "Google scraper",
    GOOGLE_SEARCHIT: "Google via searchit",
    GOOGLE_SERPAPI: "Google via SerpAPI with API key",
    PPLX: "Perplexity with API key",
    QWANT_ANYWS: "Qwant via anywebsearch",
    QWANT_SEARCHIT: "Qwant via searchit",
    TAVILY: "Tavily with API key",
    YANDEX_ANYWS: "Yandex via anywebsearch",
    YANDEX_SEARCHIT: "Yandex via searchit",
    YOU_NEWS: "You.com News with API key",
    YOU: "You.com with API key",
}


def standardize_engine_name(engine_name: str) -> str:
    """Standardize engine name by replacing hyphens with underscores.

    Args:
        engine_name: The engine name to standardize

    Returns:
        The standardized engine name
    """
    return engine_name.replace("-", "_")
