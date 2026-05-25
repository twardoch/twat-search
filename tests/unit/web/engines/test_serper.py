#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_serper.py
"""Unit tests for the Serper search engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.serper import SerperSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_serper_engine_is_registered() -> None:
    """Serper is available through the shared engine registry."""
    engine = get_engine("serper", EngineConfig(api_key="test-key"))

    assert isinstance(engine, SerperSearchEngine)


def test_serper_requires_api_key() -> None:
    """Serper fails at initialization when no API key is configured."""
    with pytest.raises(EngineError, match="API key is required"):
        SerperSearchEngine(EngineConfig(api_key=None))


def test_serper_payload_uses_google_serp_parameters() -> None:
    """The payload maps unified search options onto Serper's q/num/gl/hl shape."""
    engine = SerperSearchEngine(
        EngineConfig(api_key="test-key", default_params={"gl": "pl", "hl": "pl"}),
        num_results=7,
    )

    assert engine._build_payload("font search") == {
        "q": "font search",
        "num": 7,
        "gl": "pl",
        "hl": "pl",
    }


@pytest.mark.asyncio
async def test_serper_search_converts_organic_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Organic Serper results become normalized SearchResult objects."""
    engine = SerperSearchEngine(EngineConfig(api_key="test-key"), num_results=2, country="us", language="en")
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "organic": [
                    {
                        "title": "Result One",
                        "link": "https://example.com/one",
                        "snippet": "First snippet",
                        "position": 1,
                    },
                    {
                        "title": "Result Two",
                        "link": "https://example.com/two",
                        "snippet": "Second snippet",
                        "position": 2,
                    },
                    {
                        "title": "Result Three",
                        "link": "https://example.com/three",
                        "snippet": "Third snippet",
                        "position": 3,
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://google.serper.dev/search"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["X-API-KEY"] == "test-key"
    assert captured_request["json_data"] == {"q": "font engineering", "num": 2, "gl": "us", "hl": "en"}
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "serper" for result in results)


@pytest.mark.asyncio
async def test_serper_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = SerperSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"organic": [{"title": "Bad", "link": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
