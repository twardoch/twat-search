#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_aisearch.py
"""Unit tests for the AI Search API engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.aisearch import AISearchEngine
from twat_search.web.engines.base import get_engine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: Any) -> None:
        self.data = data

    def json(self) -> Any:
        """Return the fake JSON payload."""
        return self.data


def test_aisearch_engine_is_registered() -> None:
    """AISearch is available through the shared engine registry."""
    engine = get_engine("aisearch", EngineConfig(api_key="test-key"))

    assert isinstance(engine, AISearchEngine)


def test_aisearch_builds_documented_payload() -> None:
    """AISearch payload follows the documented prompt/context shape."""
    engine = AISearchEngine(
        EngineConfig(api_key="test-key"),
        response_type="text",
        context=[{"role": "user", "content": "Prefer current security sources."}],
    )

    assert engine._build_payload("node security risks") == {
        "prompt": "node security risks",
        "response_type": "text",
        "context": [{"role": "user", "content": "Prefer current security sources."}],
    }


def test_aisearch_rejects_invalid_context() -> None:
    """Invalid context is rejected at the engine boundary."""
    with pytest.raises(EngineError, match="Invalid AISearch context"):
        AISearchEngine(
            EngineConfig(api_key="test-key"),
            context=[{"role": "assistant", "content": "bad"}],
        )


@pytest.mark.asyncio
async def test_aisearch_search_converts_source_backed_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    """AISearch summary responses become one normalized result per source."""
    engine = AISearchEngine(EngineConfig(api_key="test-key"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "answer": "Node.js security risks include dependency drift, XSS, and weak session handling.",
                "response_type": "markdown",
                "sources": [
                    "https://owasp.org/www-project-nodejs-goat/",
                    "https://nodejs.org/en/docs/guides/security/",
                    "https://aws.amazon.com/security/security-learning/",
                ],
                "response_time": 2847,
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("node security risks")

    assert captured_request["url"] == "https://api.aisearchapi.io/v1/search"
    assert captured_request["method"] == "POST"
    assert captured_request["headers"]["Authorization"] == "Bearer test-key"
    assert captured_request["json_data"] == {
        "prompt": "node security risks",
        "response_type": "markdown",
    }
    assert [str(result.url) for result in results] == [
        "https://owasp.org/www-project-nodejs-goat/",
        "https://nodejs.org/en/docs/guides/security/",
    ]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "aisearch" for result in results)
    assert "dependency drift" in results[0].snippet
    assert results[0].raw is not None
    assert results[0].raw["response_time"] == 2847


@pytest.mark.asyncio
async def test_aisearch_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = AISearchEngine(EngineConfig(api_key="test-key"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"answer": "Missing sources", "response_type": "markdown", "response_time": 10})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("node security risks")
