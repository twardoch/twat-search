#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_base.py
"""
Unit tests for the twat_search.web.engines.base module.

This module tests the base search engine class and factory functions.
"""

from __future__ import annotations

import abc
from typing import Any

import pytest
from pydantic import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import (
    SearchEngine,
    get_engine,
    get_engine_registry,
    get_registered_engines,
    register_engine,
)
from twat_search.web.exceptions import SearchError
from twat_search.web.models import SearchResult


class TestSearchEngine(SearchEngine):
    """Test implementation of the SearchEngine abstract base class."""

    engine_code = "test_engine"

    async def search(self, query: str) -> list[SearchResult]:
        """Test implementation of the search method."""
        return [
            SearchResult(
                title=f"Test Result for {query}",
                url=HttpUrl("https://example.com/test"),
                snippet=f"This is a test result for {query}",
                source=self.engine_code,
            ),
        ]


# Register the test engine
register_engine(TestSearchEngine)


class DisabledTestSearchEngine(SearchEngine):
    """Test implementation with disabled status for testing."""

    engine_code = "disabled_engine"

    async def search(self, query: str) -> list[SearchResult]:
        """Search implementation that should never be called."""
        msg = "This should never be called because the engine is disabled"
        raise NotImplementedError(msg)


# Register the disabled test engine
register_engine(DisabledTestSearchEngine)


def test_search_engine_is_abstract() -> None:
    """Test that SearchEngine is an abstract base class."""
    assert abc.ABC in SearchEngine.__mro__
    assert hasattr(SearchEngine, "__abstractmethods__")
    assert "search" in SearchEngine.__abstractmethods__

    # Ensure we can't instantiate SearchEngine directly
    with pytest.raises(TypeError):
        SearchEngine(EngineConfig())  # type: ignore


def test_search_engine_name_class_var() -> None:
    """Test that engine_code is a required class variable."""
    # SearchEngine.engine_code should be defined as a class variable
    assert hasattr(SearchEngine, "engine_code")

    # The default value should be an empty string (not None)
    assert SearchEngine.engine_code == ""

    # Check that our test classes have set the engine_code
    assert TestSearchEngine.engine_code == "test_engine"
    assert DisabledTestSearchEngine.engine_code == "disabled_engine"


def test_engine_registration() -> None:
    """Test that engines are properly registered."""

    # Create a new engine class
    class NewEngine(SearchEngine):
        engine_code = "new_engine"

        async def search(self, query: str) -> list[SearchResult]:
            return []

    # Register it
    returned_class = register_engine(NewEngine)

    # Test that register_engine returns the class (for decorator use)
    assert returned_class is NewEngine

    # Test that we can get the engine from the registry
    engine_instance = get_engine("new_engine", EngineConfig())
    assert isinstance(engine_instance, NewEngine)


def test_get_engine_accepts_normalized_cli_alias() -> None:
    """Hyphenated CLI aliases resolve through canonical provider codes."""
    engine_instance = get_engine("test-engine", EngineConfig())

    assert isinstance(engine_instance, TestSearchEngine)


def test_engine_registry_returns_typed_entries() -> None:
    """Engine registry exposes typed records while preserving class lookup compatibility."""
    registry = get_engine_registry()
    registered_classes = get_registered_engines()

    assert registry["test_engine"].code == "test_engine"
    assert registry["test_engine"].engine_class is TestSearchEngine
    assert registry["test_engine"].friendly_name == "test_engine"
    assert registry["test_engine"].catalog_status == "uncataloged"
    assert registry["test_engine"].transport == "unknown"
    assert registry["test_engine"].result_kinds == ("web",)
    assert registered_classes["test_engine"] is TestSearchEngine


def test_get_engine_with_invalid_name() -> None:
    """Test that get_engine raises an error for invalid engine names."""
    with pytest.raises(SearchError, match="Unknown search engine"):
        get_engine("nonexistent_engine", EngineConfig())


def test_get_engine_with_disabled_engine() -> None:
    """Test that get_engine raises an error when engine is disabled."""
    config = EngineConfig(enabled=False)
    with pytest.raises(SearchError, match="is disabled"):
        get_engine("disabled_engine", config)


def test_get_engine_with_config() -> None:
    """Test that get_engine passes config to the engine."""
    config = EngineConfig(
        api_key="test_key",
        enabled=True,
        default_params={"count": 10},
    )

    engine = get_engine("test_engine", config)

    assert engine.config is config
    assert engine.config.api_key == "test_key"
    assert engine.config.default_params == {"count": 10}


def test_get_engine_with_kwargs() -> None:
    """Test that get_engine passes kwargs to the engine."""
    kwargs = {"timeout": 30, "country": "US"}
    engine = get_engine("test_engine", EngineConfig(), **kwargs)

    # Check that kwargs were stored by the engine
    assert engine.kwargs == kwargs
    assert engine.kwargs["timeout"] == 30
    assert engine.kwargs["country"] == "US"


@pytest.mark.asyncio
async def test_make_http_request_uses_proxy_request_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    """Shared HTTP requests honor proxy URL, timeout, and pacing settings."""
    captured: dict[str, Any] = {}
    sleep_calls: list[float] = []

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

    class FakeAsyncClient:
        def __init__(self, **kwargs: Any) -> None:
            captured["client_kwargs"] = kwargs

        async def __aenter__(self) -> FakeAsyncClient:
            return self

        async def __aexit__(self, *_args: Any) -> None:
            return None

        async def request(self, **kwargs: Any) -> FakeResponse:
            captured["request_kwargs"] = kwargs
            return FakeResponse()

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)

    monkeypatch.setattr("twat_search.web.api_transport.httpx.AsyncClient", FakeAsyncClient)
    monkeypatch.setattr("twat_search.web.api_transport.asyncio.sleep", fake_sleep)
    monkeypatch.setattr("twat_search.web.api_transport.random.uniform", lambda _a, _b: 0.01)

    engine = TestSearchEngine(
        EngineConfig(),
        proxy_url="http://proxy.example:80",
        timeout=30,
        retries=0,
        min_delay=0.1,
        use_random_user_agent=False,
    )

    await engine.make_http_request("https://example.com/search", params={"q": "fonts"})

    assert sleep_calls == [0.11]
    assert captured["client_kwargs"] == {
        "timeout": 30,
        "proxy": "http://proxy.example:80",
    }
    assert captured["request_kwargs"] == {
        "method": "GET",
        "url": "https://example.com/search",
        "headers": {},
        "params": {"q": "fonts"},
        "json": None,
    }
