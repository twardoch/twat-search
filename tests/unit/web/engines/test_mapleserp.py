#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_mapleserp.py
"""Unit tests for the MapleSERP engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.mapleserp import MapleSerpSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_mapleserp_engine_is_registered() -> None:
    """MapleSERP is available through the shared engine registry."""
    engine = get_engine("mapleserp", EngineConfig(api_key="test-key"))

    assert isinstance(engine, MapleSerpSearchEngine)


def test_mapleserp_requires_api_key() -> None:
    """MapleSERP fails at initialization when no API key is configured."""
    with pytest.raises(EngineError, match="API key is required"):
        MapleSerpSearchEngine(EngineConfig(api_key=None))


def test_mapleserp_builds_documented_params() -> None:
    """MapleSERP params follow the documented GET request shape."""
    engine = MapleSerpSearchEngine(
        EngineConfig(api_key="test-key", default_params={"engine": "google"}),
        num_results=7,
        country="us",
        language="en",
        safe_search=True,
        time_frame="qdr:y",
        search_type="images",
        device="mobile",
        location="New York,United States",
    )

    assert engine._build_params("font engineering") == {
        "query": "font engineering",
        "engine": "google",
        "num": 7,
        "gl": "us",
        "hl": "en",
        "search_type": "images",
        "device": "mobile",
        "location": "New York,United States",
        "safe": "active",
        "time_period": "qdr:y",
    }


@pytest.mark.asyncio
async def test_mapleserp_search_converts_organic_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Organic MapleSERP results become normalized SearchResult objects."""
    engine = MapleSerpSearchEngine(EngineConfig(api_key="test-key"), num_results=2, country="us", language="en")
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "organic_results": [
                    {
                        "title": "Result One",
                        "link": "https://example.com/one",
                        "snippet": "First snippet",
                        "position": 1,
                    },
                    {
                        "title": "Result Two",
                        "url": "https://example.com/two",
                        "description": "Second description",
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

    assert captured_request["url"] == "https://mapleserp.io/api/serp/search"
    assert captured_request["method"] == "GET"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["params"] == {
        "query": "font engineering",
        "engine": "google",
        "num": 2,
        "gl": "us",
        "hl": "en",
        "safe": "active",
    }
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First snippet", "Second description"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "mapleserp" for result in results)


@pytest.mark.asyncio
async def test_mapleserp_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = MapleSerpSearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"organic_results": [{"title": "Bad"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
