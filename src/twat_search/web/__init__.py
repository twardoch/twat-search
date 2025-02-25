#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["httpx", "pydantic"]
# ///
# this_file: src/twat_search/web/__init__.py

"""
Unified web search API across multiple search engines.

This package provides a single interface for searching across
multiple search engines, handling the differences between APIs
and providing a consistent result format.
"""

from .api import search
from .models import SearchResult
from .config import Config, EngineConfig

__all__ = ["Config", "EngineConfig", "SearchResult", "search"]
