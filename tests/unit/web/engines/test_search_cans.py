#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_search_cans.py
"""Unit tests for the SearchCans engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.search_cans import SearchCansSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_search_cans_engine_is_registered() -> None:
    """SearchCans is available through the shared engine registry."""
    engine = get_engine("search_cans", EngineConfig(api_key="test-key"))

    assert isinstance(engine, SearchCansSearchEngine)


def test_search_cans_requires_api_key() -> None:
    """SearchCans fails at initialization when no API key is configured."""
    with pytest.raises(EngineError, match="API key is required"):
        SearchCansSearchEngine(EngineConfig(api_key=None))


def test_search_cans_builds_documented_payload() -> None:
    """SearchCans payload follows the documented SERP request shape."""
    engine = SearchCansSearchEngine(
        EngineConfig(api_key="test-key"),
        engine="bing",
        page=2,
        timeout_ms=500,
    )

    assert engine._build_payload("font engineering") == {
        "s": "font engineering",
        "t": "bing",
        "p": 2,
        "d": 1000,
    }


@pytest.mark.asyncio
async def test_search_cans_search_converts_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """SearchCans data items become normalized SearchResult objects."""
    engine = SearchCansSearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "code": 0,
                "msg": "Success",
                "data": [
                    {
                        "title": "Result One",
                        "url": "https://example.com/one",
                        "content": "First summary",
                    },
                    {
                        "title": "Result Two",
                        "url": "https://example.com/two",
                        "content": "Second summary",
                    },
                    {
                        "title": "Result Three",
                        "url": "https://example.com/three",
                        "content": "Third summary",
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://www.searchcans.com/api/search"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["json_data"] == {
        "s": "font engineering",
        "t": "google",
        "p": 1,
        "d": 20000,
    }
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First summary", "Second summary"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "search_cans" for result in results)


@pytest.mark.asyncio
async def test_search_cans_search_reports_provider_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Non-zero SearchCans application codes raise a provider-specific EngineError."""
    engine = SearchCansSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"code": 401, "msg": "invalid token", "data": []})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="invalid token"):
        await engine.search("font engineering")


@pytest.mark.asyncio
async def test_search_cans_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = SearchCansSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"code": 0, "data": [{"title": "Bad", "url": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
