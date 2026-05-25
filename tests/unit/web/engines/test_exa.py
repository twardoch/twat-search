#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_exa.py
"""Unit tests for the Exa search engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.exa import ExaSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_exa_engine_is_registered() -> None:
    """Exa is available through the shared engine registry."""
    engine = get_engine("exa", EngineConfig(api_key="test-key"))

    assert isinstance(engine, ExaSearchEngine)


def test_exa_payload_uses_search_api_shape() -> None:
    """Payload uses Exa's query/numResults/type/contents shape."""
    engine = ExaSearchEngine(
        EngineConfig(api_key="test-key"),
        num_results=120,
        country="US",
        search_type="fast",
        category="research paper",
        include_text=True,
        include_highlights=True,
        moderation=True,
    )

    assert engine._build_payload("font search") == {
        "query": "font search",
        "numResults": 100,
        "type": "fast",
        "category": "research paper",
        "userLocation": "US",
        "moderation": True,
        "contents": {"text": True, "highlights": True},
    }


@pytest.mark.asyncio
async def test_exa_search_converts_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Exa results become normalized SearchResult objects."""
    engine = ExaSearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "requestId": "req-1",
                "searchType": "auto",
                "results": [
                    {
                        "title": "Result One",
                        "url": "https://example.com/one",
                        "author": "A. Writer",
                        "publishedDate": "2026-01-01",
                        "highlights": ["First highlight"],
                    },
                    {
                        "title": "Result Two",
                        "url": "https://example.com/two",
                        "text": "Second text snippet",
                    },
                    {
                        "title": "Result Three",
                        "url": "https://example.com/three",
                        "highlights": ["Third highlight"],
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://api.exa.ai/search"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["x-api-key"] == "test-key"
    assert captured_request["json_data"] == {
        "query": "font engineering",
        "numResults": 2,
        "type": "auto",
        "contents": {"highlights": True},
    }
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First highlight", "Second text snippet"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "exa" for result in results)


@pytest.mark.asyncio
async def test_exa_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = ExaSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"results": [{"title": "Bad", "url": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
