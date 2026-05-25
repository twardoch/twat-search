#!/usr/bin/env python
# this_file: tests/unit/web/test_llm.py
"""Tests for OpenAI-compatible LLM helpers."""

from __future__ import annotations

from typing import Any, ClassVar

import pytest
from pytest import MonkeyPatch

from twat_search.web.config import LLMConfig
from twat_search.web.llm import (
    LLMError,
    OpenAICompatibleLLMClient,
    decompose_search_query,
    normalize_rewritten_query,
    rerank_search_results,
    rewrite_search_query,
    synthesize_search_answer,
)
from twat_search.web.models import SearchFailure, SearchResult


class FakeResponse:
    """Small HTTPX response stand-in."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    def raise_for_status(self) -> None:
        """Pretend the response was successful."""

    def json(self) -> dict[str, Any]:
        """Return fake JSON payload."""
        return self.data


class FakeAsyncClient:
    """Capture chat completion calls made by OpenAICompatibleLLMClient."""

    calls: ClassVar[list[dict[str, Any]]] = []
    response_data: ClassVar[dict[str, Any]] = {
        "choices": [{"message": {"content": "rewritten search query"}}],
    }

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def __aenter__(self) -> FakeAsyncClient:
        return self

    async def __aexit__(self, exc_type: object, exc: object, traceback: object) -> None:
        return None

    async def post(self, url: str, *, headers: dict[str, str], json: dict[str, Any]) -> FakeResponse:
        self.calls.append({"url": url, "headers": headers, "json": json, "client_kwargs": self.kwargs})
        return FakeResponse(self.response_data)


class InjectedFakeLLMClient:
    """Fake LLM client injected directly into helper functions."""

    def __init__(self, *responses: str) -> None:
        self.responses = list(responses)
        self.calls: list[list[dict[str, str]]] = []

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Capture messages and return the next configured response."""
        self.calls.append(messages)
        if not self.responses:
            return ""
        return self.responses.pop(0)


@pytest.fixture(autouse=True)
def reset_fake_client() -> None:
    """Reset shared fake state between tests."""
    FakeAsyncClient.calls = []
    FakeAsyncClient.response_data = {"choices": [{"message": {"content": "rewritten search query"}}]}


def configured_llm(**overrides: Any) -> LLMConfig:
    """Build a fully configured LLMConfig for tests."""
    data: dict[str, Any] = {
        "enabled": True,
        "query_rewrite": True,
        "query_decomposition": True,
        "result_rerank": True,
        "answer_synthesis": True,
        "model": "gpt-test",
        "api_key": "secret",
        "base_url": "https://llm.example/v1/",
    }
    data.update(overrides)
    return LLMConfig(**data)


@pytest.mark.asyncio
async def test_openai_compatible_client_posts_chat_completion(monkeypatch: MonkeyPatch) -> None:
    """Client sends the documented chat completion shape and parses first message content."""
    monkeypatch.setattr("twat_search.web.llm_transport.httpx.AsyncClient", FakeAsyncClient)
    client = OpenAICompatibleLLMClient(configured_llm(timeout=12.5, temperature=0.2, max_tokens=64))

    result = await client.chat([{"role": "user", "content": "query"}])

    assert result == "rewritten search query"
    assert FakeAsyncClient.calls == [
        {
            "url": "https://llm.example/v1/chat/completions",
            "headers": {
                "Accept": "application/json",
                "Authorization": "Bearer secret",
                "Content-Type": "application/json",
            },
            "json": {
                "model": "gpt-test",
                "messages": [{"role": "user", "content": "query"}],
                "temperature": 0.2,
                "max_tokens": 64,
            },
            "client_kwargs": {"timeout": 12.5},
        },
    ]


@pytest.mark.asyncio
async def test_rewrite_search_query_uses_system_and_user_messages(monkeypatch: MonkeyPatch) -> None:
    """Query rewriting sends a concise rewrite prompt and strips wrapping quotes."""
    monkeypatch.setattr("twat_search.web.llm_transport.httpx.AsyncClient", FakeAsyncClient)
    FakeAsyncClient.response_data = {"choices": [{"message": {"content": '"python httpx retry"'}}]}

    rewritten = await rewrite_search_query("python request retries", configured_llm())

    assert rewritten == "python httpx retry"
    messages = FakeAsyncClient.calls[0]["json"]["messages"]
    assert messages[0]["role"] == "system"
    assert messages[1] == {"role": "user", "content": "python request retries"}


@pytest.mark.asyncio
async def test_rewrite_search_query_falls_back_when_disabled_or_empty(monkeypatch: MonkeyPatch) -> None:
    """Disabled or empty rewrites preserve the original query."""
    monkeypatch.setattr("twat_search.web.llm_transport.httpx.AsyncClient", FakeAsyncClient)

    assert await rewrite_search_query("original", configured_llm(query_rewrite=False)) == "original"

    FakeAsyncClient.response_data = {"choices": [{"message": {"content": "   "}}]}
    assert await rewrite_search_query("original", configured_llm()) == "original"


@pytest.mark.asyncio
async def test_rewrite_search_query_rejects_incomplete_config() -> None:
    """Requested rewrites fail visibly when endpoint configuration is incomplete."""
    config = LLMConfig(enabled=True, query_rewrite=True, model="gpt-test", api_key="key")

    with pytest.raises(LLMError, match="base_url"):
        await rewrite_search_query("original", config)


def test_client_rejects_incomplete_config() -> None:
    """Client fails loudly when a rewrite was requested without endpoint config."""
    with pytest.raises(LLMError, match="base_url"):
        OpenAICompatibleLLMClient(LLMConfig(enabled=True, query_rewrite=True, model="gpt-test", api_key="key"))


def test_normalize_rewritten_query_preserves_unwrapped_queries() -> None:
    """Normalization only strips whitespace and one pair of wrapping quotes."""
    assert normalize_rewritten_query("  site:example.com docs  ") == "site:example.com docs"
    assert normalize_rewritten_query("'exact phrase search'") == "exact phrase search"


@pytest.mark.asyncio
async def test_llm_helpers_accept_injected_fake_client_without_httpx() -> None:
    """LLM steps can be tested offline by injecting a small fake chat client."""
    client = InjectedFakeLLMClient(
        '"site:example.com font tools"',
        '```json\n{"queries": ["font tools", "site:github.com font tools"]}\n```',
    )
    config = configured_llm(decomposition_max_queries=3)

    rewritten = await rewrite_search_query("font tools", config, client=client)  # type: ignore[arg-type]
    decomposed = await decompose_search_query("font tools", config, client=client)  # type: ignore[arg-type]

    assert rewritten == "site:example.com font tools"
    assert decomposed == ["font tools", "site:github.com font tools"]
    assert len(client.calls) == 2
    assert client.calls[0][0]["content"].startswith("Rewrite")
    assert client.calls[1][0]["content"].startswith("Decompose")


@pytest.mark.asyncio
async def test_decompose_search_query_returns_deduplicated_capped_queries(monkeypatch: MonkeyPatch) -> None:
    """Query decomposition parses model JSON and keeps the base query first."""
    monkeypatch.setattr("twat_search.web.llm_transport.httpx.AsyncClient", FakeAsyncClient)
    FakeAsyncClient.response_data = {
        "choices": [
            {
                "message": {
                    "content": '["site:example.com docs", "original query", "python httpx retry"]',
                },
            },
        ],
    }

    queries = await decompose_search_query("original query", configured_llm(decomposition_max_queries=2))

    assert queries == ["original query", "site:example.com docs"]
    messages = FakeAsyncClient.calls[0]["json"]["messages"]
    assert messages[0]["role"] == "system"
    assert messages[1] == {"role": "user", "content": "original query"}


@pytest.mark.asyncio
async def test_decompose_search_query_falls_back_when_disabled() -> None:
    """Disabled query decomposition preserves a single search query."""
    assert await decompose_search_query("original", configured_llm(query_decomposition=False)) == ["original"]


@pytest.mark.asyncio
async def test_decompose_search_query_rejects_incomplete_config() -> None:
    """Requested decomposition fails visibly when endpoint configuration is incomplete."""
    config = LLMConfig(enabled=True, query_decomposition=True, model="gpt-test", api_key="key")

    with pytest.raises(LLMError, match="base_url"):
        await decompose_search_query("original", config)


@pytest.mark.asyncio
async def test_rerank_search_results_orders_by_model_score_and_adds_provenance(monkeypatch: MonkeyPatch) -> None:
    """Reranking sorts scored candidates and stores model provenance on each result."""
    monkeypatch.setattr("twat_search.web.llm_transport.httpx.AsyncClient", FakeAsyncClient)
    FakeAsyncClient.response_data = {
        "choices": [
            {
                "message": {
                    "content": (
                        '[{"result_id": 1, "score": 0.9, "rationale": "more specific"}, '
                        '{"result_id": 0, "score": 0.2, "rationale": "less specific"}]'
                    ),
                },
            },
        ],
    }
    results = [
        SearchResult(title="General", url="https://example.com/a", snippet="broad", source="mock", rank=1),
        SearchResult(title="Specific", url="https://example.com/b", snippet="focused", source="mock", rank=2),
    ]

    reranked = await rerank_search_results("query", results, configured_llm(rerank_top_n=2))

    assert [result.title for result in reranked] == ["Specific", "General"]
    assert [result.rank for result in reranked] == [1, 2]
    assert reranked[0].raw is not None
    assert reranked[0].raw["llm_rerank"] == {
        "model": "gpt-test",
        "prompt_version": "twat-search-rerank-v1",
        "input_result_id": 1,
        "original_rank": 2,
        "score": 0.9,
        "rationale": "more specific",
    }
    messages = FakeAsyncClient.calls[0]["json"]["messages"]
    assert messages[0]["role"] == "system"
    assert '"result_id": 0' in messages[1]["content"]


@pytest.mark.asyncio
async def test_rerank_search_results_falls_back_when_disabled_or_empty() -> None:
    """Disabled reranking and empty result sets preserve provider order."""
    results = [SearchResult(title="A", url="https://example.com/a", snippet="", source="mock")]

    assert await rerank_search_results("query", results, configured_llm(result_rerank=False)) == results
    assert await rerank_search_results("query", [], configured_llm()) == []


@pytest.mark.asyncio
async def test_synthesize_search_answer_cites_known_urls_and_preserves_failures(monkeypatch: MonkeyPatch) -> None:
    """Answer synthesis filters citations to input results and carries source failures."""
    monkeypatch.setattr("twat_search.web.llm_transport.httpx.AsyncClient", FakeAsyncClient)
    FakeAsyncClient.response_data = {
        "choices": [
            {
                "message": {
                    "content": (
                        '{"answer": "Specific answer with a failure note.", '
                        '"cited_urls": ["https://example.com/a", "https://not-from-results.test"]}'
                    ),
                },
            },
        ],
    }
    results = [SearchResult(title="A", url="https://example.com/a", snippet="evidence", source="mock", rank=1)]
    failures = [SearchFailure(engine="other", kind="timeout", message="timed out", retryable=True)]

    answer = await synthesize_search_answer("query", results, failures, configured_llm(synthesis_top_n=1))

    assert answer is not None
    assert answer.text == "Specific answer with a failure note."
    assert [str(url) for url in answer.cited_urls] == ["https://example.com/a"]
    assert answer.model == "gpt-test"
    assert answer.prompt_version == "twat-search-synthesis-v1"
    assert answer.input_result_count == 1
    assert answer.source_failures == failures
    messages = FakeAsyncClient.calls[0]["json"]["messages"]
    assert messages[0]["role"] == "system"
    assert '"source_failures"' in messages[1]["content"]


@pytest.mark.asyncio
async def test_synthesize_search_answer_falls_back_when_disabled_or_empty() -> None:
    """Disabled synthesis and empty result sets do not produce answers."""
    results = [SearchResult(title="A", url="https://example.com/a", snippet="", source="mock")]

    assert await synthesize_search_answer("query", results, [], configured_llm(answer_synthesis=False)) is None
    assert await synthesize_search_answer("query", [], [], configured_llm()) is None
