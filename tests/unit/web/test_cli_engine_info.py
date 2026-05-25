#!/usr/bin/env python
# this_file: tests/unit/web/test_cli_engine_info.py
"""Unit tests for CLI engine metadata helpers."""

from __future__ import annotations

from pytest import MonkeyPatch

from twat_search.web.cli import _build_explain_payload, _get_engine_info
from twat_search.web.config import Config, EngineConfig, ProxyConfig
from twat_search.web.models import EngineOutcome, SearchFailure, SearchRequest, SearchResponse, SearchResult


def test_engine_info_includes_provider_metadata() -> None:
    """Engine info exposes provider-catalog fields used by route planning."""
    info = _get_engine_info(
        "brave",
        EngineConfig(enabled=True),
        registered_engines={},
    )

    assert info["transport"] == "api"
    assert info["status"] == "implemented"
    assert info["api_key_required"] is True
    assert info["proxy_support"] is False
    assert info["proxy_policy"] == "none"
    assert info["cost_class"] == "metered"
    assert info["stability"] == "stable"
    assert info["planned"] is False


def test_engine_info_handles_browser_provider_metadata() -> None:
    """Browser engines expose browser and proxy capability metadata."""
    info = _get_engine_info(
        "google_falla",
        EngineConfig(enabled=True),
        registered_engines={},
    )

    assert info["transport"] == "browser"
    assert info["browser_required"] is True
    assert info["proxy_support"] is True
    assert info["proxy_policy"] == "optional"
    assert info["proxy_transports"] == ["playwright", "httpx"]
    assert info["api_key_required"] is False


def test_engine_info_marks_env_key_as_set(monkeypatch: MonkeyPatch) -> None:
    """Engine info checks provider env vars even without registered classes."""
    monkeypatch.setenv("GENSEE_SEARCH_API_KEY", "test-key")

    info = _get_engine_info(
        "gensee",
        EngineConfig(enabled=False),
        registered_engines={},
    )

    assert info["status"] == "implemented"
    assert info["planned"] is False
    assert info["api_key_required"] is True
    assert info["api_key_set"] is True
    assert info["env_vars"] == [{"name": "GENSEE_SEARCH_API_KEY", "set": True}]


def test_build_explain_payload_reports_route_proxy_errors_and_llm_steps() -> None:
    """CLI explain output summarizes selection, skips, proxy policy, failures, and LLM provenance."""
    config = Config(
        engines={
            "brave": EngineConfig(enabled=True, api_key="key"),
            "serper": EngineConfig(enabled=True, api_key=None),
            "duckduckgo": EngineConfig(enabled=False),
        },
        proxies=ProxyConfig(
            enabled=True,
            provider="webshare",
            username="user",
            password="test-redacted-password",
            host="proxy.example",
            port=8080,
            retries=4,
        ),
    )
    failure = SearchFailure(engine="serper", kind="auth", message="missing key", retryable=False)
    response = SearchResponse(
        request=SearchRequest(
            query="font search",
            route="best",
            params={
                "llm_search_queries": ["font search", "font crawler"],
                "llm_decomposition": {"model": "gpt-test", "query_count": 2},
                "llm_rerank_error": "not configured",
            },
        ),
        engines=[
            EngineOutcome(
                engine="brave",
                status="ok",
                results=[
                    SearchResult(
                        title="Result",
                        url="https://example.com",
                        snippet="snippet",
                        source="brave",
                    ),
                ],
            ),
            EngineOutcome(engine="serper", status="failed", failure=failure),
        ],
        results=[],
        failures=[failure],
    )

    payload = _build_explain_payload(response, ["brave", "serper"], config)

    assert payload["route"] == "best"
    assert payload["selected_engines"] == ["brave", "serper"]
    assert {"engine": "duckduckgo", "reason": "disabled"} in payload["skipped_engines"]
    assert payload["proxy"]["enabled"] is True
    assert payload["proxy"]["retries"] == 4
    assert "test-redacted-password" not in str(payload["proxy"]["url"])
    assert payload["errors"][0]["kind"] == "auth"
    assert payload["llm_steps"]["search_queries"] == ["font search", "font crawler"]
    assert payload["llm_steps"]["rerank"] == "not configured"
