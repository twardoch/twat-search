#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_dataforseo.py
"""Unit tests for the DataForSEO live SERP engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.dataforseo import DataForSeoSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_dataforseo_engine_is_registered() -> None:
    """DataForSEO is available through the shared engine registry."""
    engine = get_engine("dataforseo", EngineConfig(api_key="login:password"))

    assert isinstance(engine, DataForSeoSearchEngine)


def test_dataforseo_payload_uses_live_serp_shape() -> None:
    """Payload uses DataForSEO's one-task live SERP JSON array."""
    engine = DataForSeoSearchEngine(
        EngineConfig(api_key="login:password"),
        num_results=12,
        location_code=2840,
        language_code="en",
        device="desktop",
    )

    assert engine._build_payload("font search") == [
        {
            "keyword": "font search",
            "depth": 12,
            "location_code": 2840,
            "language_code": "en",
            "device": "desktop",
        },
    ]


def test_dataforseo_auth_header_is_basic_token() -> None:
    """DataForSEO credentials are sent as a Basic auth token."""
    engine = DataForSeoSearchEngine(EngineConfig(api_key="login:password"))

    assert engine._auth_header() == "Basic bG9naW46cGFzc3dvcmQ="


@pytest.mark.asyncio
async def test_dataforseo_search_converts_organic_items(monkeypatch: pytest.MonkeyPatch) -> None:
    """Nested DataForSEO organic items become normalized SearchResult objects."""
    engine = DataForSeoSearchEngine(EngineConfig(api_key="login:password"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "status_code": 20000,
                "tasks": [
                    {
                        "status_code": 20000,
                        "result": [
                            {
                                "items": [
                                    {
                                        "type": "organic",
                                        "title": "Result One",
                                        "url": "https://example.com/one",
                                        "description": "First snippet",
                                        "rank_absolute": 1,
                                    },
                                    {
                                        "type": "people_also_ask",
                                        "title": "Skipped",
                                        "url": "https://example.com/skip",
                                        "description": "Not organic",
                                        "rank_absolute": 2,
                                    },
                                    {
                                        "type": "organic",
                                        "title": "Result Two",
                                        "url": "https://example.com/two",
                                        "description": "Second snippet",
                                        "rank_absolute": 3,
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["Authorization"] == "Basic bG9naW46cGFzc3dvcmQ="
    assert captured_request["json_data"][0]["keyword"] == "font engineering"
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.rank for result in results] == [1, 3]
    assert all(result.source == "dataforseo" for result in results)


@pytest.mark.asyncio
async def test_dataforseo_search_reports_task_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Task-level DataForSEO failures become EngineError."""
    engine = DataForSeoSearchEngine(EngineConfig(api_key="login:password"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"tasks": [{"status_code": 40501, "status_message": "Invalid field"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Invalid field"):
        await engine.search("font engineering")
