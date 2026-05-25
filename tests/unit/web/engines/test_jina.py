#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_jina.py
"""Unit tests for the Jina search engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.jina import JinaSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: Any) -> None:
        self.data = data

    def json(self) -> Any:
        """Return the fake JSON payload."""
        return self.data


def test_jina_engine_is_registered() -> None:
    """Jina is available through the shared engine registry."""
    engine = get_engine("jina", EngineConfig(api_key="test-key"))

    assert isinstance(engine, JinaSearchEngine)


def test_jina_builds_encoded_search_url() -> None:
    """Jina search query is encoded into the s.jina.ai URL path."""
    engine = JinaSearchEngine(EngineConfig(api_key="test-key"))

    assert engine._build_url("font engineering news") == "https://s.jina.ai/font%20engineering%20news"


@pytest.mark.asyncio
async def test_jina_search_converts_data_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Jina data-array responses become normalized SearchResult objects."""
    engine = JinaSearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "data": [
                    {
                        "title": "Result One",
                        "url": "https://example.com/one",
                        "content": "First content",
                        "timestamp": "2026-01-01T00:00:00Z",
                    },
                    {
                        "title": "Result Two",
                        "url": "https://example.com/two",
                        "description": "Second description",
                    },
                    {
                        "title": "Result Three",
                        "url": "https://example.com/three",
                        "content": "Third content",
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://s.jina.ai/font%20engineering"
    assert captured_request["method"] == "GET"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["headers"]["Accept"] == "application/json"
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First content", "Second description"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "jina" for result in results)


@pytest.mark.asyncio
async def test_jina_search_can_skip_content_snippets(monkeypatch: pytest.MonkeyPatch) -> None:
    """When content is disabled, description/snippet fields are preferred."""
    engine = JinaSearchEngine(EngineConfig(api_key="test-key"), include_content=False)

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse(
            [
                {
                    "title": "Result",
                    "url": "https://example.com/",
                    "content": "Long content",
                    "snippet": "Short snippet",
                },
            ],
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert results[0].snippet == "Short snippet"


@pytest.mark.asyncio
async def test_jina_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = JinaSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"data": [{"title": "Bad", "url": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
