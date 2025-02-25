# this_file: src/twat_search/web/engines/__init__.py

"""
Search engine implementations for the web search API.

This package contains implementations for various search engines,
each one providing a standard interface for searching and returning results.
"""

from .base import SearchEngine, register_engine, get_engine

# Import and register all engines
from .brave import BraveSearchEngine, BraveNewsSearchEngine
from .serpapi import SerpApiSearchEngine
from .tavily import TavilySearchEngine
from .you import YouSearchEngine, YouNewsSearchEngine

# Optional imports for backwards compatibility
try:
    from .pplx import PerplexitySearchEngine
except ImportError:
    # PerplexitySearchEngine not available
    pass

__all__ = [
    "BraveNewsSearchEngine",
    "BraveSearchEngine",
    "PerplexitySearchEngine",
    "SearchEngine",
    "SerpApiSearchEngine",
    "TavilySearchEngine",
    "YouNewsSearchEngine",
    "YouSearchEngine",
    "get_engine",
    "register_engine",
]
