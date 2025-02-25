# this_file: src/twat_search/web/engines/__init__.py

"""
Search engine implementations for the web search API.

This package contains implementations for various search engines,
each one providing a standard interface for searching and returning results.
"""

from .base import SearchEngine, register_engine, get_engine

# Import and register all engines
from .brave import BraveSearchEngine
from .google import GoogleSearchEngine
from .tavily import TavilySearchEngine
from .perplexity import PerplexitySearchEngine
from .youcom import YoucomSearchEngine

__all__ = [
    "BraveSearchEngine",
    "GoogleSearchEngine",
    "PerplexitySearchEngine",
    "SearchEngine",
    "TavilySearchEngine",
    "YoucomSearchEngine",
    "get_engine",
    "register_engine",
]
