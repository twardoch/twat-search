# this_file: src/twat_search/web/engines/__init__.py

"""
Search engine implementations.

This package contains the implementations of various search engines that
can be used with the twat_search.web API.
"""

from .base import register_engine, get_engine, get_registered_engines, SearchEngine
from .brave import BraveSearchEngine, BraveNewsSearchEngine, brave, brave_news
from .serpapi import SerpApiSearchEngine, serpapi
from .tavily import TavilySearchEngine, tavily
from .pplx import PerplexitySearchEngine, pplx
from .you import YouSearchEngine, YouNewsSearchEngine, you, you_news
from .critique import CritiqueSearchEngine, critique
from .duckduckgo import DuckDuckGoSearchEngine, duckduckgo
from .webscout import WebScoutEngine, webscout
from .bing_scraper import BingScraperSearchEngine, bing_scraper

__all__ = [
    # Engine classes
    "BingScraperSearchEngine",
    "BraveNewsSearchEngine",
    "BraveSearchEngine",
    "CritiqueSearchEngine",
    "DuckDuckGoSearchEngine",
    "PerplexitySearchEngine",
    # Base classes and functions
    "SearchEngine",
    "SerpApiSearchEngine",
    "TavilySearchEngine",
    "WebScoutEngine",
    "YouNewsSearchEngine",
    "YouSearchEngine",
    # Convenience functions
    "bing_scraper",
    "brave",
    "brave_news",
    "critique",
    "duckduckgo",
    "get_engine",
    "get_registered_engines",
    "pplx",
    "register_engine",
    "serpapi",
    "tavily",
    "webscout",
    "you",
    "you_news",
]
