#!/usr/bin/env python
# this_file: tests/unit/web/test_cli_engine_info.py
"""Unit tests for CLI engine metadata helpers."""

from __future__ import annotations

from pytest import MonkeyPatch

from twat_search.web.cli import (
    _build_explain_payload,
    _doctor_payload,
    _fetch_url_payload,
    _get_engine_info,
    _provider_records,
    _response_jsonl_records,
    _route_records,
)
from twat_search.web.config import Config, EngineConfig, ProxyConfig, ResultProcessingConfig
from twat_search.web.engines.base import get_engine_registry
from twat_search.web.models import (
    EngineExecutionContext,
    EngineOutcome,
    EngineParameterSet,
    EngineRequest,
    SearchFailure,
    SearchRequest,
    SearchResponse,
    SearchResult,
)


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
    assert info["route_priority"] == 10
    assert info["planned"] is False


def test_engine_info_can_use_typed_registry_records(monkeypatch: MonkeyPatch) -> None:
    """Engine info accepts typed registry records, not only raw class maps."""
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)

    info = _get_engine_info(
        "brave",
        EngineConfig(enabled=True),
        get_engine_registry(),
    )

    assert info["registered"] is True
    assert info["registry_catalog_status"] == "cataloged"
    assert info["engine_class"] == "BraveSearchEngine"
    assert info["env_vars"] == [{"name": "BRAVE_API_KEY", "set": False}]


def test_engine_info_handles_browser_provider_metadata() -> None:
    """Browser engines expose browser and proxy capability metadata."""
    info = _get_engine_info(
        "google_browser",
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
    proxy_password = "test-" + "redacted-password"
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
            password=proxy_password,
            host="proxy.example",
            port=8080,
            retries=4,
        ),
        result_processing=ResultProcessingConfig(deduplicate=True, max_results=12),
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
                "result_processing": {
                    "input_result_count": 4,
                    "output_result_count": 3,
                    "duplicate_result_count": 1,
                    "truncated_result_count": 0,
                    "deduplicate": True,
                    "deduplicate_by": "url",
                    "max_results": 12,
                },
            },
        ),
        engines=[
            EngineOutcome(
                engine="brave",
                status="ok",
                request=EngineRequest(
                    engine="brave",
                    query="font search",
                    execution=EngineExecutionContext(
                        engine="brave",
                        parameter_set=EngineParameterSet(
                            engine="brave",
                            requested_engines=("brave", "serper"),
                            common_params={"num_results": 5},
                            engine_specific_params={"freshness": "pd"},
                            passthrough_params={},
                            params={"num_results": 5, "freshness": "pd"},
                            param_sources={"num_results": "common", "freshness": "engine_specific"},
                        ),
                    ),
                ),
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
    assert payload["route_policy"]["name"] == "best"
    assert payload["route_policy"]["max_engines"] == 3
    assert payload["selected_engines"] == ["brave", "serper"]
    assert {"engine": "duckduckgo", "reason": "disabled"} in payload["skipped_engines"]
    assert payload["request_policy"]["proxy_enabled"] is True
    assert payload["request_policy"]["timeout"] == 30.0
    assert proxy_password not in str(payload["request_policy"]["redacted_proxy_url"])
    assert payload["result_processing"] == {
        "deduplicate": True,
        "deduplicate_by": "url",
        "max_results": 12,
    }
    assert payload["result_processing_stats"]["duplicate_result_count"] == 1
    assert payload["outcomes"][0]["parameter_set"]["engine_specific_params"] == {"freshness": "pd"}
    assert payload["proxy"]["enabled"] is True
    assert payload["proxy"]["retries"] == 4
    assert proxy_password not in str(payload["proxy"]["url"])
    assert payload["errors"][0]["kind"] == "auth"
    assert payload["llm_steps"]["search_queries"] == ["font search", "font crawler"]
    assert payload["llm_steps"]["rerank"] == "not configured"


def test_response_jsonl_records_include_failures_and_results() -> None:
    """JSONL output preserves request, engine, result, failure, and explain records."""
    result = SearchResult(
        title="Example",
        url="https://example.com",
        snippet="Snippet",
        source="brave",
        rank=1,
    )
    failure = SearchFailure(
        engine="serper",
        kind="auth",
        message="missing key",
        exception_type="EngineError",
    )
    response = SearchResponse(
        request=SearchRequest(query="query", engines=["brave", "serper"], route=None),
        engines=[
            EngineOutcome(engine="brave", status="ok", results=[result]),
            EngineOutcome(engine="serper", status="failed", failure=failure),
        ],
        results=[result],
        failures=[failure],
    )

    records = _response_jsonl_records(response, explain={"selected_engines": ["brave", "serper"]})

    assert [record["type"] for record in records] == ["request", "engine", "result", "engine", "failure", "explain"]
    assert records[2]["result"]["url"] == "https://example.com/"
    assert records[4]["failure"]["kind"] == "auth"
    assert records[5]["explain"]["selected_engines"] == ["brave", "serper"]


def test_provider_route_and_doctor_helpers_are_machine_readable() -> None:
    """Provider, route, and doctor helpers expose the explicit 2.0 CLI surface."""
    config = Config(
        engines={
            "plugin_search": EngineConfig(enabled=True),
            "brave": EngineConfig(enabled=True, api_key=None),
        },
    )

    api_providers = _provider_records(transport="api", status="implemented")
    route_records = _route_records(config, route="plugins")
    doctor = _doctor_payload(config)

    assert any(provider["code"] == "brave" for provider in api_providers)
    assert route_records[0]["name"] == "plugins"
    assert route_records[0]["policy"]["name"] == "plugins"
    assert route_records[0]["transports"] == ["plugin"]
    assert route_records[0]["include_unkeyed"] is True
    assert isinstance(route_records[0]["selected_engines"], list)
    assert isinstance(route_records[0]["skipped_engines"], list)
    assert all("reason" in skipped for skipped in route_records[0]["skipped_engines"])
    assert doctor["counts"]["implemented_providers"] > 0
    assert "plugins" in doctor["routes"]
    assert isinstance(doctor["issues"], list)


def test_fetch_url_payload_rejects_invalid_url_without_network() -> None:
    """Fetch diagnostics parse invalid URLs before making a request."""
    payload = _fetch_url_payload("not-a-url", config=Config())

    assert payload["ok"] is False
    assert payload["exception_type"] == "ValueError"
    assert payload["status_code"] is None
