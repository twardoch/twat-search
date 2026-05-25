#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_langsearch.py
"""Unit tests for the LangSearch engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.langsearch import LangSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: Any) -> None:
        self.data = data

    def json(self) -> Any:
        """Return the fake JSON payload."""
        return self.data


def test_langsearch_engine_is_registered() -> None:
    """LangSearch is available through the shared engine registry."""
    engine = get_engine("langsearch", EngineConfig(api_key="test-key"))

    assert isinstance(engine, LangSearchEngine)


def test_langsearch_builds_documented_payload() -> None:
    """LangSearch payload follows the documented web-search request shape."""
    engine = LangSearchEngine(
        EngineConfig(api_key="test-key"),
        num_results=25,
        time_frame="week",
        summary=False,
    )

    assert engine._build_payload("font engineering") == {
        "query": "font engineering",
        "freshness": "oneWeek",
        "summary": False,
        "count": 10,
    }


@pytest.mark.asyncio
async def test_langsearch_search_converts_web_pages(monkeypatch: pytest.MonkeyPatch) -> None:
    """LangSearch webPages.value items become normalized SearchResult objects."""
    engine = LangSearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "code": 200,
                "msg": None,
                "data": {
                    "_type": "SearchResponse",
                    "queryContext": {"originalQuery": "font engineering"},
                    "webPages": {
                        "value": [
                            {
                                "name": "Result One",
                                "url": "https://example.com/one",
                                "displayUrl": "https://example.com/one",
                                "snippet": "First snippet",
                                "summary": "First summary",
                            },
                            {
                                "name": "Result Two",
                                "url": "https://example.com/two",
                                "snippet": "Second snippet",
                            },
                            {
                                "name": "Result Three",
                                "url": "https://example.com/three",
                                "snippet": "Third snippet",
                            },
                        ],
                    },
                },
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://api.langsearch.com/v1/web-search"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["json_data"] == {
        "query": "font engineering",
        "freshness": "noLimit",
        "summary": True,
        "count": 2,
    }
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First summary", "Second snippet"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "langsearch" for result in results)


@pytest.mark.asyncio
async def test_langsearch_search_reports_provider_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Non-200 LangSearch response codes raise a provider-specific EngineError."""
    engine = LangSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"code": 401, "msg": "invalid api key", "data": {}})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="invalid api key"):
        await engine.search("font engineering")


@pytest.mark.asyncio
async def test_langsearch_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = LangSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"code": 200, "data": {"webPages": {"value": [{"name": "Bad", "url": "not-a-url"}]}}})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
