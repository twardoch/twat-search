#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_firecrawl.py
"""Unit tests for the Firecrawl search engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.firecrawl import FirecrawlSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_firecrawl_engine_is_registered() -> None:
    """Firecrawl is available through the shared engine registry."""
    engine = get_engine("firecrawl", EngineConfig(api_key="test-key"))

    assert isinstance(engine, FirecrawlSearchEngine)


def test_firecrawl_payload_uses_v2_search_shape() -> None:
    """Payload uses Firecrawl's query/limit/sources/search options shape."""
    engine = FirecrawlSearchEngine(
        EngineConfig(api_key="test-key"),
        num_results=7,
        country="DE",
        categories=["github", "research"],
        include_domains=["example.com"],
        include_markdown=True,
        timeout_ms=60000,
    )

    assert engine._build_payload("font search") == {
        "query": "font search",
        "limit": 7,
        "sources": ["web"],
        "categories": [{"type": "github"}, {"type": "research"}],
        "includeDomains": ["example.com"],
        "country": "DE",
        "timeout": 60000,
        "scrapeOptions": {"formats": [{"type": "markdown"}]},
    }


@pytest.mark.asyncio
async def test_firecrawl_search_converts_web_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Firecrawl web results become normalized SearchResult objects."""
    engine = FirecrawlSearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "success": True,
                "id": "search-1",
                "creditsUsed": 2,
                "data": {
                    "web": [
                        {
                            "title": "Result One",
                            "description": "First description",
                            "url": "https://example.com/one",
                        },
                        {
                            "title": "Result Two",
                            "description": "Second description",
                            "url": "https://example.com/two",
                        },
                        {
                            "title": "Result Three",
                            "description": "Third description",
                            "url": "https://example.com/three",
                        },
                    ],
                },
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://api.firecrawl.dev/v2/search"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["json_data"] == {
        "query": "font engineering",
        "limit": 2,
        "sources": ["web"],
    }
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.rank for result in results] == [1, 2]
    assert [result.snippet for result in results] == ["First description", "Second description"]
    assert all(result.source == "firecrawl" for result in results)


@pytest.mark.asyncio
async def test_firecrawl_search_can_use_markdown_snippets(monkeypatch: pytest.MonkeyPatch) -> None:
    """When markdown is requested, markdown becomes the normalized snippet source."""
    engine = FirecrawlSearchEngine(EngineConfig(api_key="test-key"), include_markdown=True)

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse(
            {
                "success": True,
                "data": {
                    "web": [
                        {
                            "title": "Result",
                            "description": "Description",
                            "url": "https://example.com/",
                            "markdown": "# Heading\n\nUseful markdown content.",
                        },
                    ],
                },
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert results[0].snippet == "# Heading Useful markdown content."


@pytest.mark.asyncio
async def test_firecrawl_search_reports_provider_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unsuccessful Firecrawl responses become EngineError."""
    engine = FirecrawlSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"success": False, "warning": "search failed"})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="search failed"):
        await engine.search("font engineering")
