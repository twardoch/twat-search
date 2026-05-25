#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_search1api.py
"""Unit tests for the Search1API engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.search1api import Search1ApiSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: Any) -> None:
        self.data = data

    def json(self) -> Any:
        """Return the fake JSON payload."""
        return self.data


def test_search1api_engine_is_registered() -> None:
    """Search1API is available through the shared engine registry."""
    engine = get_engine("search1api", EngineConfig(api_key="test-key"))

    assert isinstance(engine, Search1ApiSearchEngine)


def test_search1api_builds_single_search_payload() -> None:
    """Search1API payload follows the documented single-search request shape."""
    engine = Search1ApiSearchEngine(
        EngineConfig(api_key="test-key"),
        num_results=150,
        language="en",
        time_frame="year",
        search_service="github",
        crawl_results=12,
        include_sites=["github.com"],
        exclude_sites=["example.com"],
    )

    assert engine._build_payload("font engineering") == {
        "query": "font engineering",
        "search_service": "github",
        "max_results": 100,
        "crawl_results": 10,
        "image": False,
        "include_sites": ["github.com"],
        "exclude_sites": ["example.com"],
        "language": "en",
        "time_range": "year",
    }


@pytest.mark.asyncio
async def test_search1api_search_converts_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Search1API results become normalized SearchResult objects."""
    engine = Search1ApiSearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "searchParameters": {"query": "font engineering"},
                "results": [
                    {
                        "title": "Result One",
                        "link": "https://example.com/one",
                        "snippet": "First snippet",
                        "content": "First crawled content",
                    },
                    {
                        "title": "Result Two",
                        "link": "https://example.com/two",
                        "snippet": "Second snippet",
                    },
                    {
                        "title": "Result Three",
                        "link": "https://example.com/three",
                        "snippet": "Third snippet",
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://api.search1api.com/search"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["json_data"]["query"] == "font engineering"
    assert captured_request["json_data"]["search_service"] == "google"
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First crawled content", "Second snippet"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "search1api" for result in results)


@pytest.mark.asyncio
async def test_search1api_search_can_skip_content_snippets(monkeypatch: pytest.MonkeyPatch) -> None:
    """When content snippets are disabled, the provider snippet is preferred."""
    engine = Search1ApiSearchEngine(EngineConfig(api_key="test-key"), include_content=False)

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse(
            {
                "results": [
                    {
                        "title": "Result",
                        "link": "https://example.com/",
                        "snippet": "Short snippet",
                        "content": "Long content",
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert results[0].snippet == "Short snippet"


@pytest.mark.asyncio
async def test_search1api_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = Search1ApiSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"results": [{"title": "Bad", "link": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
