#!/usr/bin/env python
# this_file: tests/unit/web/test_transports.py
"""Unit tests for provider transport context helpers."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.api_transport import execute_api_request
from twat_search.web.models import EngineRequest
from twat_search.web.transports import enrich_engine_request, get_transport_context


def test_transport_context_uses_catalog_metadata() -> None:
    """Known providers expose transport facts from the provider catalog."""
    context = get_transport_context("google-falla")

    assert context.engine == "google_browser"
    assert context.transport == "browser"
    assert context.proxy_supported is True
    assert context.proxy_policy == "optional"
    assert context.proxy_transports == ("playwright", "httpx")
    assert context.browser_required is True
    assert context.result_kinds == ("web",)


def test_transport_context_has_neutral_unknown_defaults() -> None:
    """Unknown test/local engines do not pretend to have catalog capabilities."""
    context = get_transport_context("mock")

    assert context.engine == "mock"
    assert context.transport is None
    assert context.proxy_supported is False
    assert context.proxy_policy == "none"
    assert context.proxy_transports == ()
    assert context.browser_required is False
    assert context.result_kinds == ()


def test_enrich_engine_request_preserves_params_and_adds_transport_metadata() -> None:
    """Request enrichment is provenance only; provider params stay untouched."""
    request = EngineRequest(
        engine="plugin_search",
        query="font tools",
        route="best",
        params={"num_results": 3},
    )

    enriched = enrich_engine_request(request)

    assert enriched.engine == "plugin_search"
    assert enriched.query == "font tools"
    assert enriched.route == "best"
    assert enriched.params == {"num_results": 3}
    assert enriched.transport == "plugin"
    assert enriched.proxy_policy == "none"
    assert enriched.proxy_transports == ()
    assert enriched.browser_required is False
    assert enriched.result_kinds == ("web", "code", "repository")


@pytest.mark.asyncio
async def test_execute_api_request_applies_proxy_delay_and_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    """HTTP transport execution owns shared proxy, pacing, timeout, and header policy."""
    captured: dict[str, Any] = {}
    sleep_calls: list[float] = []

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

    class FakeAsyncClient:
        def __init__(self, **kwargs: Any) -> None:
            captured["client_kwargs"] = kwargs

        async def __aenter__(self) -> FakeAsyncClient:
            return self

        async def __aexit__(self, *_args: Any) -> None:
            return None

        async def request(self, **kwargs: Any) -> FakeResponse:
            captured["request_kwargs"] = kwargs
            return FakeResponse()

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)

    monkeypatch.setattr("twat_search.web.api_transport.httpx.AsyncClient", FakeAsyncClient)
    monkeypatch.setattr("twat_search.web.api_transport.asyncio.sleep", fake_sleep)
    monkeypatch.setattr("twat_search.web.api_transport.random.choice", lambda values: values[0])
    monkeypatch.setattr("twat_search.web.api_transport.random.uniform", lambda _a, _b: 0.01)

    await execute_api_request(
        engine_code="demo",
        url="https://example.com/search",
        params={"q": "fonts"},
        timeout=30,
        retries=0,
        min_delay=0.1,
        proxy_url="http://proxy.example:80",
    )

    assert sleep_calls == [0.11]
    assert captured["client_kwargs"] == {
        "timeout": 30,
        "proxy": "http://proxy.example:80",
    }
    assert captured["request_kwargs"]["method"] == "GET"
    assert captured["request_kwargs"]["url"] == "https://example.com/search"
    assert captured["request_kwargs"]["params"] == {"q": "fonts"}
    assert captured["request_kwargs"]["json"] is None
    assert captured["request_kwargs"]["headers"]["User-Agent"].startswith("Mozilla/5.0")
