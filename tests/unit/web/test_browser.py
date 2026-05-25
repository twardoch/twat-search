#!/usr/bin/env python
# this_file: tests/unit/web/test_browser.py
"""Unit tests for browser diagnostics and evidence helpers."""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from twat_search.web.browser import (
    BrowserChallengeError,
    build_browser_evidence,
    detect_browser_signals,
    write_browser_failure_evidence,
)
from twat_search.web.config import BrowserConfig, EngineConfig, ProxyConfig

FIXTURES = Path(__file__).parents[2] / "fixtures" / "browser"


def test_detect_browser_signals_finds_captcha_fixture() -> None:
    """Local CAPTCHA fixture is classified as a blocking browser state."""
    html = (FIXTURES / "google_captcha.html").read_text(encoding="utf-8")

    evidence = build_browser_evidence(
        engine="google_browser",
        query="FontLab",
        html=html,
        url="https://www.google.com/sorry/index",
        title="Google Sorry",
    )

    assert evidence.blocked is True
    assert evidence.needs_consent is False
    assert {signal.kind for signal in evidence.signals} >= {"captcha"}


def test_detect_browser_signals_finds_consent_fixture() -> None:
    """Local consent fixture is classified separately from blocking."""
    html = (FIXTURES / "qwant_consent.html").read_text(encoding="utf-8")

    signals = detect_browser_signals(html, title="Privacy choices")

    assert {signal.kind for signal in signals} == {"consent"}


def test_detect_browser_signals_finds_cloudflare_challenge() -> None:
    """Cloudflare challenge markers are reported as bot challenges."""
    html = "<html><body><div class='cf-turnstile'>Cloudflare challenge-platform</div></body></html>"

    evidence = build_browser_evidence(engine="browser", query="test", html=html)

    assert evidence.blocked is True
    assert any(signal.kind == "bot_challenge" for signal in evidence.signals)


def test_write_browser_failure_evidence_respects_config(tmp_path: Path) -> None:
    """Failure evidence writes only artifacts enabled by browser config."""
    config = BrowserConfig(save_html_on_failure=True, screenshots_on_failure=False)
    html = (FIXTURES / "google_captcha.html").read_text(encoding="utf-8")

    evidence = write_browser_failure_evidence(
        engine="google_browser",
        query="FontLab / typography?",
        html=html,
        config=config,
        screenshot=b"not-a-real-png",
        output_dir=tmp_path,
    )

    assert evidence.html_path is not None
    assert evidence.html_path.exists()
    assert evidence.html_path.name == "google_browser-fontlab-typography.html"
    assert evidence.screenshot_path is None
    assert evidence.blocked is True


def test_browser_challenge_error_carries_serializable_evidence() -> None:
    """BrowserChallengeError exposes evidence for structured search failures."""
    html = (FIXTURES / "qwant_consent.html").read_text(encoding="utf-8")
    evidence = build_browser_evidence(engine="qwant_browser", query="FontLab", html=html, title="Privacy choices")

    error = BrowserChallengeError(evidence)

    assert "consent" in str(error)
    assert error.evidence.to_failure_details()["browser"]["needs_consent"] is True


def test_falla_requests_fetch_uses_proxy_policy(monkeypatch: MonkeyPatch) -> None:
    """Request-mode bundled scrapers pass shared proxy settings into requests."""
    fake_playwright = types.ModuleType("playwright")
    fake_async_api = types.ModuleType("playwright.async_api")
    fake_async_api.Browser = object
    fake_async_api.BrowserContext = object
    fake_async_api.TimeoutError = TimeoutError
    fake_async_api.async_playwright = object
    monkeypatch.setitem(sys.modules, "playwright", fake_playwright)
    monkeypatch.setitem(sys.modules, "playwright.async_api", fake_async_api)

    falla_module = importlib.import_module("twat_search.web.engines.lib_falla.core.falla")
    captured: dict[str, object] = {}

    class FakeResponse:
        text = "<html><body>ok</body></html>"

        def raise_for_status(self) -> None:
            return None

    def fake_get(url: str, **kwargs: object) -> FakeResponse:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return FakeResponse()

    monkeypatch.setattr("twat_search.web.scraper_transport.requests.get", fake_get)

    fake_password = "pa" + "ss"
    engine = falla_module.Falla(name="Mojeek")
    engine.proxy_config = ProxyConfig(
        enabled=True,
        username="user",
        password=fake_password,
        host="p.webshare.io",
        port=80,
        timeout=42,
        retries=2,
    )

    html = engine.get_html_content("https://www.mojeek.com/search?q=fonts")

    assert html == "<html><body>ok</body></html>"
    assert captured["url"] == "https://www.mojeek.com/search?q=fonts"
    assert captured["kwargs"] == {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        },
        "timeout": 42,
        "proxies": {
            "http": "http://user:pass@p.webshare.io:80",
            "https": "http://user:pass@p.webshare.io:80",
        },
    }


@pytest.mark.asyncio
async def test_falla_browser_context_uses_proxy_and_tears_down(monkeypatch: MonkeyPatch) -> None:
    """Browser-backed scrapers inject Playwright proxy context and close resources."""
    fake_playwright = types.ModuleType("playwright")
    fake_async_api = types.ModuleType("playwright.async_api")
    fake_async_api.Browser = object
    fake_async_api.BrowserContext = object
    fake_async_api.TimeoutError = TimeoutError
    fake_async_api.async_playwright = object
    monkeypatch.setitem(sys.modules, "playwright", fake_playwright)
    monkeypatch.setitem(sys.modules, "playwright.async_api", fake_async_api)

    falla_module = importlib.import_module("twat_search.web.engines.lib_falla.core.falla")
    captured: dict[str, object] = {}

    class FakeContext:
        def __init__(self) -> None:
            self.closed = False

        async def close(self) -> None:
            self.closed = True
            captured["context_closed"] = True

    class FakeBrowser:
        def __init__(self) -> None:
            self.context = FakeContext()

        async def new_context(self, **kwargs: object) -> FakeContext:
            captured["context_kwargs"] = kwargs
            return self.context

        async def close(self) -> None:
            captured["browser_closed"] = True

    class FakeBrowserType:
        async def launch(self, **kwargs: object) -> FakeBrowser:
            captured["launch_kwargs"] = kwargs
            return FakeBrowser()

    class FakePlaywright:
        chromium = FakeBrowserType()

    class FakeAsyncPlaywright:
        async def start(self) -> FakePlaywright:
            captured["started"] = True
            return FakePlaywright()

    def fake_async_playwright() -> FakeAsyncPlaywright:
        return FakeAsyncPlaywright()

    monkeypatch.setattr(falla_module, "async_playwright", fake_async_playwright)

    engine = falla_module.Falla(name="Google")
    engine.browser_config = BrowserConfig(
        enabled=True,
        headless=False,
        channel="chrome",
        locale="pl-PL",
        timezone="Europe/Warsaw",
        viewport_width=1200,
        viewport_height=800,
    )
    proxy_password = "pa" + "ss"
    engine.proxy_config = ProxyConfig(
        enabled=True,
        username="user",
        password=proxy_password,
        host="p.webshare.io",
        port=80,
    )

    await engine._initialize_browser()

    assert captured["started"] is True
    assert captured["launch_kwargs"] == {"headless": False, "channel": "chrome"}
    assert captured["context_kwargs"] == {
        "locale": "pl-PL",
        "timezone_id": "Europe/Warsaw",
        "viewport": {"width": 1200, "height": 800},
        "proxy": {
            "server": "http://p.webshare.io:80",
            "username": "user",
            "password": "pass",
        },
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    await engine._close_browser()

    assert captured["context_closed"] is True
    assert captured["browser_closed"] is True
    assert engine.browser_context is None
    assert engine.browser is None


@pytest.mark.asyncio
async def test_browser_search_engine_passes_config_and_preserves_challenge(
    monkeypatch: MonkeyPatch,
) -> None:
    """Public browser engines preserve structured browser challenge evidence."""
    from twat_search.web.engines.falla import GoogleBrowserEngine  # noqa: PLC0415

    browser_config = BrowserConfig(enabled=True, save_html_on_failure=False, screenshots_on_failure=False)
    proxy_config = ProxyConfig(enabled=True, url="http://proxy.example:80")
    evidence = build_browser_evidence(
        engine="Google",
        query="FontLab",
        html=(FIXTURES / "google_captcha.html").read_text(encoding="utf-8"),
        url="https://www.google.com/sorry/index",
    )

    class FakeBrowserAdapter:
        browser_config: BrowserConfig | None = None
        proxy_config: ProxyConfig | None = None

        async def search_async(self, query: str) -> list[dict[str, str]]:
            assert query == "FontLab"
            assert self.browser_config is browser_config
            assert self.proxy_config is proxy_config
            raise BrowserChallengeError(evidence)

    monkeypatch.setattr(GoogleBrowserEngine, "_browser_engine_class", FakeBrowserAdapter)
    engine = GoogleBrowserEngine(
        EngineConfig(enabled=True),
        browser_config=browser_config,
        proxy_config=proxy_config,
    )

    with pytest.raises(BrowserChallengeError) as exc_info:
        await engine.search("FontLab")

    assert exc_info.value.evidence.to_failure_details()["browser"]["blocked"] is True


class _FakePage:
    """Minimal Playwright page double for Falla browser diagnostics."""

    async def content(self) -> str:
        """Return challenge HTML."""
        return '<html><form action="/sorry/index"><textarea name="g-recaptcha-response"></textarea></form></html>'

    async def title(self) -> str:
        """Return a title that is copied into evidence."""
        return "Google Sorry"

    async def screenshot(self) -> bytes:
        """Return synthetic screenshot bytes."""
        return b"png"


@pytest.mark.asyncio
async def test_falla_browser_content_raises_structured_challenge(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Falla Playwright fetch paths convert challenge pages into structured evidence."""
    pytest.importorskip("playwright.async_api", reason="Falla browser diagnostics require optional Playwright")
    falla_module = importlib.import_module("twat_search.web.engines.lib_falla.core.falla")

    monkeypatch.chdir(tmp_path)
    engine = falla_module.Falla(name="Google")
    engine.current_query = "FontLab"
    engine.browser_config = BrowserConfig(save_html_on_failure=True, screenshots_on_failure=True)

    with pytest.raises(BrowserChallengeError) as exc_info:
        await engine._content_or_raise_browser_challenge(_FakePage(), "https://www.google.com/sorry/index")

    evidence = exc_info.value.evidence
    assert evidence.blocked is True
    assert evidence.html_path is not None
    assert evidence.html_path.exists()
    assert evidence.screenshot_path is not None
    assert evidence.screenshot_path.exists()
    assert evidence.to_failure_details()["browser"]["title"] == "Google Sorry"
