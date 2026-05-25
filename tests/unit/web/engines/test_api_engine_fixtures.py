#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_api_engine_fixtures.py
"""Mocked response coverage for legacy/current API search engines."""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.brave import BraveNewsSearchEngine, BraveSearchEngine
from twat_search.web.engines.critique import CritiqueSearchEngine
from twat_search.web.engines.hasdata import HasDataGoogleEngine, HasDataGoogleLightEngine
from twat_search.web.engines.pplx import PerplexitySearchEngine
from twat_search.web.engines.serpapi import SerpApiSearchEngine
from twat_search.web.engines.tavily import TavilySearchEngine
from twat_search.web.engines.you import YouNewsSearchEngine, YouSearchEngine
from twat_search.web.provider_catalog import list_provider_metadata

critique_module = importlib.import_module("twat_search.web.engines.critique")
hasdata_module = importlib.import_module("twat_search.web.engines.hasdata")
tavily_module = importlib.import_module("twat_search.web.engines.tavily")

API_ENGINE_MOCK_COVERAGE = {
    "aisearch",
    "apify",
    "brave",
    "brave_news",
    "critique",
    "dataforseo",
    "exa",
    "firecrawl",
    "gensee",
    "github_search",
    "google_cse",
    "google_hasdata",
    "google_hasdata_full",
    "google_serpapi",
    "jina",
    "langsearch",
    "mapleserp",
    "pplx",
    "search1api",
    "search_cans",
    "serper",
    "tavily",
    "you",
    "you_news",
}


class FakeResponse:
    """Small response object matching the methods used by API engines."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        self.status_code = 200
        self.text = ""

    def json(self) -> dict[str, Any]:
        """Return the configured payload."""
        return self.payload

    def raise_for_status(self) -> None:
        """Pretend the response was successful."""


class FakeAsyncClient:
    """Async context manager that records one request and returns a payload."""

    def __init__(self, payload: dict[str, Any], capture: dict[str, Any]) -> None:
        self.payload = payload
        self.capture = capture

    async def __aenter__(self) -> FakeAsyncClient:
        """Enter the fake HTTP client context."""
        return self

    async def __aexit__(self, *_exc: object) -> None:
        """Exit the fake HTTP client context."""

    async def get(self, url: str | None = None, **kwargs: Any) -> FakeResponse:
        """Capture a GET request and return the fake payload."""
        if url is not None:
            kwargs["url"] = url
        self.capture.update({"method": "GET", **kwargs})
        return FakeResponse(self.payload)

    async def post(self, url: str | None = None, **kwargs: Any) -> FakeResponse:
        """Capture a POST request and return the fake payload."""
        if url is not None:
            kwargs["url"] = url
        self.capture.update({"method": "POST", **kwargs})
        return FakeResponse(self.payload)


def patch_async_client(monkeypatch: pytest.MonkeyPatch, module: Any, payload: dict[str, Any]) -> dict[str, Any]:
    """Patch a module's httpx.AsyncClient and return the request capture dict."""
    capture: dict[str, Any] = {}
    monkeypatch.setattr(module.httpx, "AsyncClient", lambda: FakeAsyncClient(payload, capture))
    return capture


def test_every_implemented_api_engine_has_mock_response_coverage() -> None:
    """Every implemented API engine must have explicit mocked response coverage."""
    implemented_api_engines = {
        provider.code
        for provider in list_provider_metadata(include_planned=False)
        if provider.transport == "api" and provider.status == "implemented"
    }

    assert implemented_api_engines <= API_ENGINE_MOCK_COVERAGE


@pytest.mark.asyncio
async def test_brave_web_search_converts_mocked_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Brave web API responses become normalized search results."""
    payload = {
        "web": {
            "results": [
                {
                    "title": "Font tooling",
                    "url": "https://example.com/font-tooling",
                    "description": "A web result from Brave.",
                },
            ],
        },
    }
    captured: dict[str, Any] = {}

    async def fake_make_api_call(self: BraveSearchEngine, query: str) -> dict[str, Any]:
        captured["query"] = query
        return payload

    monkeypatch.setattr(BraveSearchEngine, "_make_api_call", fake_make_api_call)

    engine = BraveSearchEngine(EngineConfig(api_key="test-key"), num_results=1)
    results = await engine.search("font engineering")

    assert captured["query"] == "font engineering"
    assert len(results) == 1
    assert results[0].source == "brave"
    assert str(results[0].url) == "https://example.com/font-tooling"


@pytest.mark.asyncio
async def test_brave_news_search_converts_mocked_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Brave news API responses preserve source and age metadata in snippets."""
    payload = {
        "results": [
            {
                "title": "Search news",
                "url": "https://example.com/news",
                "description": "A news result from Brave.",
                "source": {"name": "Example News"},
                "age": "2 hours ago",
            },
        ],
    }

    async def fake_make_api_call(self: BraveNewsSearchEngine, query: str) -> dict[str, Any]:
        return payload

    monkeypatch.setattr(BraveNewsSearchEngine, "_make_api_call", fake_make_api_call)

    engine = BraveNewsSearchEngine(EngineConfig(api_key="test-key"), num_results=1)
    results = await engine.search("font engineering")

    assert len(results) == 1
    assert results[0].source == "brave_news"
    assert "Example News" in results[0].snippet


@pytest.mark.asyncio
async def test_critique_search_converts_mocked_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Critique API responses become source-backed normalized results."""
    payload = {
        "results": [
            {
                "url": "https://example.com/critique",
                "title": "Critique result",
                "summary": "A critique-backed result.",
                "source": "example",
                "relevance_score": 0.9,
            },
        ],
    }
    captured = patch_async_client(monkeypatch, critique_module, payload)

    engine = CritiqueSearchEngine(EngineConfig(api_key="test-key"), num_results=1)
    results = await engine.search("font engineering")

    assert captured["method"] == "POST"
    assert captured["url"] == "https://api.critique-labs.ai/v1/search"
    assert captured["headers"]["X-API-Key"] == "test-key"
    assert captured["json"] == {"prompt": "font engineering"}
    assert results[0].source == "critique"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("engine_cls", "expected_source", "expected_url", "expected_params"),
    [
        (
            HasDataGoogleEngine,
            "google_hasdata_full",
            "https://api.hasdata.com/scrape/google/serp",
            {"q": "font engineering", "location": "Austin,Texas,United States", "deviceType": "mobile"},
        ),
        (
            HasDataGoogleLightEngine,
            "google_hasdata",
            "https://api.hasdata.com/scrape/google-light/serp",
            {"q": "font engineering", "location": "Austin,Texas,United States"},
        ),
    ],
)
async def test_hasdata_engines_convert_mocked_responses(
    monkeypatch: pytest.MonkeyPatch,
    engine_cls: type[HasDataGoogleEngine] | type[HasDataGoogleLightEngine],
    expected_source: str,
    expected_url: str,
    expected_params: dict[str, Any],
) -> None:
    """Both HasData API engines convert organic results through the same mocked path."""
    payload = {
        "organicResults": [
            {
                "title": "HasData result",
                "link": "https://example.com/hasdata",
                "snippet": "A HasData organic result.",
            },
        ],
    }
    captured = patch_async_client(monkeypatch, hasdata_module, payload)

    engine = engine_cls(
        EngineConfig(api_key="test-key"),
        num_results=1,
        location="Austin,Texas,United States",
        device_type="mobile",
    )
    results = await engine.search("font engineering")

    assert captured["method"] == "GET"
    assert captured["url"] == expected_url
    assert captured["headers"]["x-api-key"] == "test-key"
    assert captured["params"] == expected_params
    assert results[0].source == expected_source
    assert str(results[0].url) == "https://example.com/hasdata"


@pytest.mark.asyncio
async def test_serpapi_search_converts_mocked_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """SerpAPI organic results become normalized search results."""
    payload = {
        "organic_results": [
            {
                "title": "SerpAPI result",
                "link": "https://example.com/serpapi",
                "snippet": "A SerpAPI organic result.",
                "position": 1,
            },
        ],
        "search_metadata": {"id": "search-id"},
        "search_parameters": {"q": "font engineering"},
    }
    engine = SerpApiSearchEngine(EngineConfig(api_key="test-key"), num_results=1, country="us", language="en")

    async def fake_make_http_request(self: SerpApiSearchEngine, url: str, **kwargs: Any) -> FakeResponse:
        captured["url"] = url
        captured.update(kwargs)
        return FakeResponse(payload)

    captured: dict[str, Any] = {}
    monkeypatch.setattr(SerpApiSearchEngine, "make_http_request", fake_make_http_request)

    results = await engine.search("font engineering")

    assert captured["url"] == "https://serpapi.com/search"
    assert captured["timeout"] == 30
    assert captured["params"]["api_key"] == "test-key"
    assert captured["params"]["q"] == "font engineering"
    assert results[0].source == "google_serpapi"
    assert results[0].rank == 1


@pytest.mark.asyncio
async def test_perplexity_search_converts_mocked_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Perplexity chat completions become answer-style search results."""
    payload = {"choices": [{"message": {"content": "A concise answer with web context."}}]}
    captured: dict[str, Any] = {}

    async def fake_make_http_request(self: PerplexitySearchEngine, **kwargs: Any) -> FakeResponse:
        captured.update(kwargs)
        return FakeResponse(payload)

    monkeypatch.setattr(PerplexitySearchEngine, "make_http_request", fake_make_http_request)

    engine = PerplexitySearchEngine(EngineConfig(api_key="test-key"), num_results=1, model="sonar")
    results = await engine.search("font engineering")

    assert captured["url"] == "https://api.perplexity.ai/chat/completions"
    assert captured["method"] == "POST"
    assert captured["headers"]["authorization"] == "Bearer test-key"
    assert captured["json_data"]["model"] == "sonar"
    assert results[0].source == "pplx"
    assert "concise answer" in results[0].snippet


@pytest.mark.asyncio
async def test_tavily_search_converts_mocked_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tavily API results are shortened and normalized."""
    payload = {
        "query": "font engineering",
        "results": [
            {
                "title": "Tavily result",
                "url": "https://example.com/tavily",
                "content": "A Tavily content result.",
                "score": 0.8,
            },
        ],
    }
    captured = patch_async_client(monkeypatch, tavily_module, payload)

    engine = TavilySearchEngine(EngineConfig(api_key="test-key"), num_results=1, include_answer=True)
    results = await engine.search("font engineering")

    assert captured["method"] == "POST"
    assert captured["url"] == "https://api.tavily.com/search"
    assert captured["json"]["api_key"] == "test-key"
    assert captured["json"]["query"] == "font engineering"
    assert results[0].source == "tavily"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("engine_cls", "payload", "expected_source", "expected_url", "expected_param"),
    [
        (
            YouSearchEngine,
            {
                "hits": [
                    {
                        "title": "You result",
                        "url": "https://example.com/you",
                        "description": "A You.com web result.",
                    },
                ],
            },
            "you",
            "https://api.ydc-index.io/search",
            "num_web_results",
        ),
        (
            YouNewsSearchEngine,
            {
                "articles": [
                    {
                        "title": "You news",
                        "url": "https://example.com/you-news",
                        "description": "A You.com news result.",
                        "source": "Example News",
                        "published_date": "2026-05-25",
                    },
                ],
            },
            "you_news",
            "https://chat-api.you.com/news",
            "num_news_results",
        ),
    ],
)
async def test_you_engines_convert_mocked_responses(
    monkeypatch: pytest.MonkeyPatch,
    engine_cls: type[YouSearchEngine] | type[YouNewsSearchEngine],
    payload: dict[str, Any],
    expected_source: str,
    expected_url: str,
    expected_param: str,
) -> None:
    """You.com web and news API responses use the shared mocked request path."""
    captured: dict[str, Any] = {}

    async def fake_make_http_request(self: YouSearchEngine | YouNewsSearchEngine, **kwargs: Any) -> FakeResponse:
        captured.update(kwargs)
        return FakeResponse(payload)

    monkeypatch.setattr(engine_cls, "make_http_request", fake_make_http_request)

    engine = engine_cls(EngineConfig(api_key="test-key"), num_results=1, country="us")
    results = await engine.search("font engineering")

    assert captured["url"] == expected_url
    assert captured["method"] == "GET"
    assert captured["headers"]["X-API-Key"] == "test-key"
    assert captured["params"]["query"] == "font engineering"
    assert captured["params"][expected_param] == 1
    assert results[0].source == expected_source
