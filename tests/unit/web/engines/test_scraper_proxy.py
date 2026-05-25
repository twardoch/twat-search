#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_scraper_proxy.py
"""Proxy-policy tests for standalone scraper engines."""

from __future__ import annotations

import sys
import types
from importlib import import_module
from types import SimpleNamespace
from typing import Any

import pytest

from twat_search.web.config import EngineConfig


@pytest.mark.asyncio
async def test_duckduckgo_uses_shared_proxy_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """DuckDuckGo scraper accepts the shared request-policy proxy URL."""
    captured: dict[str, Any] = {}

    class FakeDDGS:
        def __init__(self, **kwargs: Any) -> None:
            captured["client_kwargs"] = kwargs

        def text(self, **kwargs: Any) -> list[dict[str, str]]:
            captured["search_kwargs"] = kwargs
            return [
                {
                    "title": "Font tools",
                    "href": "https://example.com/font-tools",
                    "body": "Result body",
                },
            ]

    fake_module = types.ModuleType("duckduckgo_search")
    fake_module.DDGS = FakeDDGS
    monkeypatch.setitem(sys.modules, "duckduckgo_search", fake_module)

    from twat_search.web.engines.duckduckgo import DuckDuckGoSearchEngine  # noqa: PLC0415

    monkeypatch.setattr("twat_search.web.engines.duckduckgo.DDGS", FakeDDGS)

    engine = DuckDuckGoSearchEngine(
        EngineConfig(enabled=True),
        num_results=1,
        proxy_url="http://user:pass@p.webshare.io:80",
        timeout=42,
    )

    results = await engine.search("font tools")

    assert len(results) == 1
    assert captured["client_kwargs"] == {
        "proxy": "http://user:pass@p.webshare.io:80",
        "timeout": 42,
    }
    assert captured["search_kwargs"]["keywords"] == "font tools"


@pytest.mark.asyncio
async def test_google_scraper_uses_shared_proxy_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """Google scraper passes the shared request-policy proxy URL to googlesearch."""
    captured: dict[str, Any] = {}

    class FakeGoogleResult:
        url = "https://example.com/google-result"
        title = "Google result"
        description = "Result description"

    def fake_google_search(*args: Any, **kwargs: Any) -> list[FakeGoogleResult]:
        captured["args"] = args
        captured["kwargs"] = kwargs
        return [FakeGoogleResult()]

    google_scraper_module = import_module("twat_search.web.engines.google_scraper")
    google_scraper_engine = google_scraper_module.GoogleScraperEngine

    monkeypatch.setattr(google_scraper_module, "google_search", fake_google_search)

    engine = google_scraper_engine(
        EngineConfig(enabled=True),
        num_results=1,
        proxy_url="http://user:pass@p.webshare.io:80",
    )

    results = await engine.search("font tools")

    assert len(results) == 1
    assert captured["args"] == ("font tools",)
    assert captured["kwargs"]["proxy"] == "http://user:pass@p.webshare.io:80"
    assert captured["kwargs"]["advanced"] is True


@pytest.mark.asyncio
async def test_bing_scraper_uses_shared_proxy_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    """Bing scraper fetches HTML through the shared proxy-aware scraper transport."""
    captured: dict[str, Any] = {}

    class FakeBingScraper:
        def __init__(self, **kwargs: Any) -> None:
            captured["scraper_kwargs"] = kwargs

        def _get_random_user_agent(self) -> str:
            return "fake-bing-user-agent"

        def _extract_search_results(self, soup: Any) -> list[Any]:
            captured["soup_text"] = soup.get_text(" ", strip=True)
            return [
                SimpleNamespace(
                    title="Bing result",
                    url="https://example.com/bing-result",
                    description="Result description",
                ),
            ]

        def search(self, query: str, num_results: int = 10) -> list[Any]:
            captured["direct_search"] = (query, num_results)
            return []

    def fake_fetch_scraper_html(*args: Any, **kwargs: Any) -> str:
        captured["fetch_args"] = args
        captured["fetch_kwargs"] = kwargs
        return "<html><body>Bing HTML</body></html>"

    bing_scraper_module = import_module("twat_search.web.engines.bing_scraper")
    bing_scraper_engine = bing_scraper_module.BingScraperSearchEngine

    monkeypatch.setattr(bing_scraper_module, "BingScraper", FakeBingScraper)
    monkeypatch.setattr(bing_scraper_module, "fetch_scraper_html", fake_fetch_scraper_html)

    engine = bing_scraper_engine(
        EngineConfig(enabled=True),
        num_results=1,
        proxy_url="http://user:pass@p.webshare.io:80",
        timeout=42,
        retries=4,
        retry_delay=0.25,
    )

    results = await engine.search("font tools")

    assert len(results) == 1
    assert "direct_search" not in captured
    assert captured["scraper_kwargs"] == {
        "max_retries": 3,
        "delay_between_requests": 1.0,
    }
    assert captured["fetch_args"] == ("https://www.bing.com/search?q=font+tools&n=1",)
    assert captured["fetch_kwargs"]["user_agent"] == "fake-bing-user-agent"
    assert captured["fetch_kwargs"]["default_timeout"] == 42
    proxy_config = captured["fetch_kwargs"]["proxy_config"]
    assert proxy_config.httpx_proxy_url() == "http://user:pass@p.webshare.io:80"
    assert proxy_config.timeout == 42
    assert proxy_config.retries == 4
    assert proxy_config.retry_delay == 0.25
