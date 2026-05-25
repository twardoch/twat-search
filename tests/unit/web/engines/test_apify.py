#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_apify.py
"""Unit tests for the Apify search engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.apify import ApifySearchEngine
from twat_search.web.engines.base import get_engine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: Any) -> None:
        self.data = data

    def json(self) -> Any:
        """Return the fake JSON payload."""
        return self.data


def test_apify_engine_is_registered() -> None:
    """Apify is available through the shared engine registry."""
    engine = get_engine("apify", EngineConfig(api_key="test-key"))

    assert isinstance(engine, ApifySearchEngine)


def test_apify_builds_sync_actor_url() -> None:
    """Apify actor IDs are encoded for the documented sync dataset endpoint."""
    engine = ApifySearchEngine(EngineConfig(api_key="test-key"), actor_id="apify/google-search-scraper")

    assert (
        engine._build_url()
        == "https://api.apify.com/v2/acts/apify~google-search-scraper/run-sync-get-dataset-items"
    )


def test_apify_builds_google_search_scraper_payload() -> None:
    """Default Apify payload stays conservative for Google Search Scraper."""
    engine = ApifySearchEngine(
        EngineConfig(api_key="test-key"),
        num_results=25,
        country="de",
        language="de",
        time_frame="lastYear",
    )

    assert engine._build_payload("font engineering") == {
        "queries": "font engineering",
        "maxPagesPerQuery": 1,
        "resultsPerPage": 10,
        "countryCode": "de",
        "languageCode": "de",
        "timeRange": "lastYear",
    }


@pytest.mark.asyncio
async def test_apify_search_converts_nested_organic_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Apify dataset items with nested organicResults become SearchResult objects."""
    engine = ApifySearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            [
                {
                    "searchQuery": "font engineering",
                    "organicResults": [
                        {
                            "title": "Result One",
                            "url": "https://example.com/one",
                            "description": "First description",
                        },
                        {
                            "title": "Result Two",
                            "link": "https://example.com/two",
                            "snippet": "Second snippet",
                        },
                        {
                            "title": "Result Three",
                            "url": "https://example.com/three",
                            "description": "Third description",
                        },
                    ],
                },
            ],
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert captured_request["url"] == "https://api.apify.com/v2/acts/apify~google-search-scraper/run-sync-get-dataset-items"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["json_data"]["queries"] == "font engineering"
    assert [result.title for result in results] == ["Result One", "Result Two"]
    assert [result.snippet for result in results] == ["First description", "Second snippet"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "apify" for result in results)


@pytest.mark.asyncio
async def test_apify_search_converts_flat_dataset_items(monkeypatch: pytest.MonkeyPatch) -> None:
    """Some Apify actors return one result per dataset item."""
    engine = ApifySearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse(
            [
                {
                    "title": "Flat Result",
                    "url": "https://example.com/",
                    "description": "Flat description",
                },
            ],
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font engineering")

    assert results[0].title == "Flat Result"
    assert results[0].snippet == "Flat description"


@pytest.mark.asyncio
async def test_apify_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = ApifySearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"not": "a dataset"})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font engineering")
