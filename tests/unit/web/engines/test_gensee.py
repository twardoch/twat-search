#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_gensee.py
"""Unit tests for the Gensee engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.gensee import GenseeSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_gensee_engine_is_registered() -> None:
    """Gensee is available through the shared engine registry."""
    engine = get_engine("gensee", EngineConfig(api_key="test-key"))

    assert isinstance(engine, GenseeSearchEngine)


def test_gensee_requires_api_key() -> None:
    """Gensee fails at initialization when no API key is configured."""
    with pytest.raises(EngineError, match="API key is required"):
        GenseeSearchEngine(EngineConfig(api_key=None))


def test_gensee_builds_documented_params() -> None:
    """Gensee params follow the documented Search Agent request shape."""
    engine = GenseeSearchEngine(EngineConfig(api_key="test-key"), num_results=3, multilingual=True)

    assert engine._build_params("font engineering") == {
        "query": "font engineering",
        "max_results": 3,
        "multilingual": "true",
    }


@pytest.mark.asyncio
async def test_gensee_search_converts_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Gensee search_response items become normalized SearchResult objects."""
    engine = GenseeSearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "search_response": [
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
                "elapsed_time": 450,
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://platform.gensee.ai/tool/search"
    assert captured_request["method"] == "GET"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["params"] == {
        "query": "font engineering",
        "max_results": 2,
        "multilingual": "false",
    }
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First summary", "Second summary"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "gensee" for result in results)


@pytest.mark.asyncio
async def test_gensee_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = GenseeSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"search_response": [{"title": "Bad", "url": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
