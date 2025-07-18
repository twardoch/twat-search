#!/usr/bin/env python
# this_file: tests/conftest.py
"""
Pytest configuration for twat_search tests.

This module provides fixtures and configuration for pytest.
"""

from __future__ import annotations

# Configure twat-cache to use DummyCache for tests to avoid AioCacheEngine instantiation errors
# and to ensure tests are isolated from caching effects.
try:
    from aiocache import Cache  # type: ignore[attr-defined]
    from twat_cache import settings as cache_settings

    # Check if already configured to avoid re-configuration issues if src/__init__.py runs first
    # in some contexts (though for pytest collection, conftest is usually early).
    # Using .get("default", {}) to avoid KeyError if "default" is not present.
    current_cache_type = cache_settings.CACHE_CONFIG.get("default", {}).get("cache")

    if current_cache_type != Cache.DUMMY:
        cache_settings.configure_cache(
            {
                "default": {
                    "cache": Cache.DUMMY,  # Use aiocache.DummyCache
                },
            },
        )
    else:
        pass

except ImportError:
    pass

import os
import sys
from pathlib import Path

import pytest
from pytest import MonkeyPatch


@pytest.fixture(autouse=True)
def isolate_env_vars(monkeypatch: MonkeyPatch) -> None:
    """
    Automatically isolate environment variables for all tests.

    This fixture ensures each test runs with a clean environment,
    preventing real API keys or config from affecting test results.
    """
    # Clear all environment variables that might affect tests
    for env_var in list(os.environ.keys()):
        if any(env_var.endswith(suffix) for suffix in ["_API_KEY", "_ENABLED", "_DEFAULT_PARAMS"]):
            monkeypatch.delenv(env_var, raising=False)

    # Add special marker for test environment to bypass auto-loading in Config
    monkeypatch.setenv("_TEST_ENGINE", "true")


@pytest.fixture
def env_vars_for_brave(monkeypatch: MonkeyPatch) -> None:
    """
    Set environment variables for the brave search engine.

    This fixture sets up environment variables for tests that need
    to verify the Config class can correctly read from environment.
    """
    # Register fake engine in the SearchEngine registry
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from twat_search.web.engines.base import SearchEngine, register_engine

        class MockBraveEngine(SearchEngine):
            name = "brave"

        register_engine(MockBraveEngine)
    except ImportError:
        # If we can't import yet, that's OK - the test will handle it
        pass

    # Set environment variables
    monkeypatch.setenv("BRAVE_API_KEY", "test_brave_key")
    monkeypatch.setenv("BRAVE_ENABLED", "true")
    monkeypatch.setenv("BRAVE_DEFAULT_PARAMS", '{"count": 10}')

    # Unset the test marker to allow loading env variables
    monkeypatch.delenv("_TEST_ENGINE", raising=False)
