#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_google_cse.py
"""Unit tests for the Google Custom Search JSON API engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.google_cse import GoogleCseSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def json(self) -> dict[str, Any]:
        """Return the fake JSON payload."""
        return self.data


def test_google_cse_engine_is_registered(monkeypatch: pytest.MonkeyPatch) -> None:
    """Google CSE is available through the shared engine registry."""
    monkeypatch.setenv("GOOGLE_CSE_ID", "cx-id")

    engine = get_engine("google_cse", EngineConfig(api_key="test-key"))

    assert isinstance(engine, GoogleCseSearchEngine)


def test_google_cse_requires_search_engine_id(monkeypatch: pytest.MonkeyPatch) -> None:
    """Google CSE fails when no search engine ID is configured."""
    monkeypatch.delenv("GOOGLE_CSE_ID", raising=False)
    monkeypatch.delenv("GOOGLE_CSE_CX", raising=False)

    with pytest.raises(EngineError, match="search engine ID is required"):
        GoogleCseSearchEngine(EngineConfig(api_key="test-key"))


def test_google_cse_params_use_custom_search_shape() -> None:
    """The request maps unified options onto Google's key/cx/q/num parameters."""
    engine = GoogleCseSearchEngine(
        EngineConfig(api_key="test-key", default_params={"gl": "pl", "hl": "pl"}),
        num_results=12,
        cx="cx-id",
        safe_search=False,
    )

    assert engine._build_params("font search") == {
        "key": "test-key",
        "cx": "cx-id",
        "q": "font search",
        "num": 10,
        "gl": "pl",
        "hl": "pl",
        "safe": "off",
    }


@pytest.mark.asyncio
async def test_google_cse_search_converts_items(monkeypatch: pytest.MonkeyPatch) -> None:
    """Google CSE items become normalized SearchResult objects."""
    engine = GoogleCseSearchEngine(EngineConfig(api_key="test-key"), num_results=2, cx="cx-id")
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "items": [
                    {
                        "title": "Result One",
                        "link": "https://example.com/one",
                        "snippet": "First snippet",
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

    assert captured_request["url"] == "https://www.googleapis.com/customsearch/v1"
    assert captured_request["method"] == "GET"
    assert captured_request["params"]["key"] == "test-key"
    assert captured_request["params"]["cx"] == "cx-id"
    assert captured_request["params"]["q"] == "font engineering"
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "google_cse" for result in results)


@pytest.mark.asyncio
async def test_google_cse_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = GoogleCseSearchEngine(EngineConfig(api_key="test-key"), cx="cx-id")

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"items": [{"title": "Bad", "link": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
