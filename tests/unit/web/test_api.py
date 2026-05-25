#!/usr/bin/env python
# this_file: tests/unit/web/test_api.py
"""
Unit tests for the twat_search.web.api module.

This module tests the main search function, which is the primary entry point
for the web search functionality.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import AsyncGenerator, Awaitable, Callable
from typing import Any, TypeVar

import pytest
from pydantic import HttpUrl
from pytest import MonkeyPatch

from twat_search.web.api import search, search_detailed
from twat_search.web.config import Config, EngineConfig, LLMConfig
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import SearchError
from twat_search.web.models import SearchAnswer, SearchFailure, SearchResult

# Setup logging for tests
logging.basicConfig(level=logging.DEBUG)


# Fixture type for clarity
T = TypeVar("T")
AsyncFixture = Callable[..., Awaitable[T]]


class MockSearchEngine(SearchEngine):
    """Mock search engine for testing."""

    engine_code = "mock"

    def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
        """Initialize mock engine."""
        super().__init__(config, **kwargs)
        self.query_count = 0
        self.should_fail = kwargs.get("should_fail", False)

    async def search(self, query: str) -> list[SearchResult]:
        """Mock search implementation."""
        self.query_count += 1
        if self.should_fail:
            msg = "Mock search failure"
            raise Exception(msg)

        # Use kwargs to control the number of results
        result_count = self.kwargs.get("result_count", 1)
        return [
            SearchResult(
                title=f"Mock Result {i + 1} for {query}",
                url=HttpUrl(f"https://example.com/{i + 1}"),
                snippet=f"This is mock result {i + 1} for query: {query}",
                source=self.engine_code,
            )
            for i in range(result_count)
        ]


# Register the mock engine
register_engine(MockSearchEngine)


@pytest.fixture
def mock_config() -> Config:
    """Create a Config with a registered mock engine."""
    config = Config()
    config.engines = {
        "mock": EngineConfig(
            api_key="mock_key",
            enabled=True,
            default_params={"result_count": 2},
        ),
    }
    return config


@pytest.fixture
async def setup_teardown() -> AsyncGenerator[None]:
    """Setup and teardown for tests."""
    # Setup code
    yield
    # Teardown code - allow any pending tasks to complete
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    with contextlib.suppress(asyncio.CancelledError):
        await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_search_with_mock_engine(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Test search with a mock engine."""
    results = await search("test query", engines=["mock"], config=mock_config)

    assert len(results) == 2
    assert all(isinstance(result, SearchResult) for result in results)
    assert all(result.source == "mock" for result in results)
    assert "test query" in results[0].title


@pytest.mark.asyncio
async def test_search_with_additional_params(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Test search with additional parameters."""
    results = await search(
        "test query",
        engines=["mock"],
        config=mock_config,
        result_count=3,
    )

    assert len(results) == 3


@pytest.mark.asyncio
async def test_search_with_engine_specific_params(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Test search with engine-specific parameters."""
    results = await search(
        "test query",
        engines=["mock"],
        config=mock_config,
        mock_result_count=4,
    )

    assert len(results) == 4


@pytest.mark.asyncio
async def test_search_with_no_engines(setup_teardown: None) -> None:
    """Test search with no engines specified raises SearchError."""
    with pytest.raises(SearchError, match="No search engines configured"):
        await search("test query", engines=[])


@pytest.mark.asyncio
async def test_search_with_failing_engine(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Test search with a failing engine returns empty results."""
    results = await search(
        "test query",
        engines=["mock"],
        config=mock_config,
        should_fail=True,
    )

    assert len(results) == 0


@pytest.mark.asyncio
async def test_search_detailed_returns_engine_outcomes(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Detailed search keeps flat results and per-engine outcome data."""
    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert response.request.query == "test query"
    assert response.results == response.engines[0].results
    assert response.engines[0].engine == "mock"
    assert response.engines[0].status == "ok"
    assert response.failures == []


@pytest.mark.asyncio
async def test_search_detailed_records_provider_failure(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Provider search exceptions become structured failure data."""
    response = await search_detailed(
        "test query",
        engines=["mock"],
        config=mock_config,
        should_fail=True,
    )

    assert response.results == []
    assert response.engines[0].status == "failed"
    assert response.failures[0].engine == "mock"
    assert response.failures[0].kind == "provider_error"
    assert response.failures[0].exception_type == "Exception"


@pytest.mark.asyncio
async def test_search_detailed_uses_llm_rewritten_query(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """LLM query rewriting happens before provider fan-out and keeps provenance."""
    mock_config.llm = LLMConfig(
        enabled=True,
        query_rewrite=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_rewrite(query: str, config: LLMConfig) -> str:
        assert query == "test query"
        assert config.model == "gpt-test"
        return "rewritten query"

    monkeypatch.setattr("twat_search.web.api.rewrite_search_query", fake_rewrite)

    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert response.request.query == "test query"
    assert response.request.params["llm_rewritten_query"] == "rewritten query"
    assert all("rewritten query" in result.title for result in response.results)


@pytest.mark.asyncio
async def test_search_detailed_uses_llm_decomposed_queries(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """LLM query decomposition fans providers out across subqueries with provenance."""
    mock_config.llm = LLMConfig(
        enabled=True,
        query_decomposition=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_decompose(query: str, config: LLMConfig) -> list[str]:
        assert query == "test query"
        assert config.model == "gpt-test"
        return ["test query", "focused query"]

    monkeypatch.setattr("twat_search.web.api.decompose_search_query", fake_decompose)

    response = await search_detailed("test query", engines=["mock"], config=mock_config, result_count=1)

    assert response.request.params["llm_search_queries"] == ["test query", "focused query"]
    assert response.request.params["llm_decomposition"] == {
        "model": "gpt-test",
        "prompt_version": "twat-search-decomposition-v1",
        "query_count": 2,
    }
    assert [result.title for result in response.results] == [
        "Mock Result 1 for test query",
        "Mock Result 1 for focused query",
    ]
    assert response.results[1].raw is not None
    assert response.results[1].raw["query_fanout"] == {
        "query": "focused query",
        "query_index": 1,
        "query_count": 2,
    }


@pytest.mark.asyncio
async def test_search_detailed_records_decomposition_error_and_uses_single_query(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Decomposition failures are provenance, not whole-search failures."""
    mock_config.llm = LLMConfig(enabled=True, query_decomposition=True, model="gpt-test", api_key="key")

    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert "base_url" in response.request.params["llm_decomposition_error"]
    assert all("test query" in result.title for result in response.results)


@pytest.mark.asyncio
async def test_search_detailed_decompose_query_override_disables_configured_decomposition(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Call-level decompose_query=False prevents configured query fan-out."""
    mock_config.llm = LLMConfig(
        enabled=True,
        query_decomposition=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_decompose(query: str, config: LLMConfig) -> list[str]:
        msg = "decompose should not be called"
        raise AssertionError(msg)

    monkeypatch.setattr("twat_search.web.api.decompose_search_query", fake_decompose)

    response = await search_detailed(
        "test query",
        engines=["mock"],
        config=mock_config,
        decompose_query=False,
    )

    assert response.request.params["decompose_query"] is False
    assert "llm_search_queries" not in response.request.params
    assert all("test query" in result.title for result in response.results)


@pytest.mark.asyncio
async def test_search_detailed_rewrite_query_override_disables_configured_rewrite(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Call-level rewrite_query=False prevents LLM rewrite kwargs leaking to engines."""
    mock_config.llm = LLMConfig(
        enabled=True,
        query_rewrite=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_rewrite(query: str, config: LLMConfig) -> str:
        msg = "rewrite should not be called"
        raise AssertionError(msg)

    monkeypatch.setattr("twat_search.web.api.rewrite_search_query", fake_rewrite)

    response = await search_detailed(
        "test query",
        engines=["mock"],
        config=mock_config,
        rewrite_query=False,
    )

    assert response.request.params["rewrite_query"] is False
    assert "llm_rewritten_query" not in response.request.params
    assert all("test query" in result.title for result in response.results)


@pytest.mark.asyncio
async def test_search_detailed_rewrite_query_override_enables_configured_client(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Call-level rewrite_query=True enables an otherwise disabled rewrite flag."""
    mock_config.llm = LLMConfig(
        enabled=True,
        query_rewrite=False,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_rewrite(query: str, config: LLMConfig) -> str:
        assert query == "test query"
        assert config.query_rewrite is True
        return "forced rewrite"

    monkeypatch.setattr("twat_search.web.api.rewrite_search_query", fake_rewrite)

    response = await search_detailed(
        "test query",
        engines=["mock"],
        config=mock_config,
        rewrite_query=True,
    )

    assert response.request.params["rewrite_query"] is True
    assert response.request.params["llm_rewritten_query"] == "forced rewrite"
    assert all("forced rewrite" in result.title for result in response.results)


@pytest.mark.asyncio
async def test_search_detailed_records_rewrite_error_and_uses_original_query(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Rewrite failures are provenance, not whole-search failures."""
    mock_config.llm = LLMConfig(enabled=True, query_rewrite=True, model="gpt-test", api_key="key")

    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert "base_url" in response.request.params["llm_rewrite_error"]
    assert all("test query" in result.title for result in response.results)


@pytest.mark.asyncio
async def test_search_detailed_uses_llm_reranked_results(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """LLM reranking happens after fan-out and keeps provenance."""
    mock_config.llm = LLMConfig(
        enabled=True,
        result_rerank=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_rerank(query: str, results: list[SearchResult], config: LLMConfig) -> list[SearchResult]:
        assert query == "test query"
        assert config.model == "gpt-test"
        return list(reversed(results))

    monkeypatch.setattr("twat_search.web.api.rerank_search_results", fake_rerank)

    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert response.request.params["llm_rerank"] == {"model": "gpt-test", "result_count": 2}
    assert response.results[0].title == "Mock Result 2 for test query"
    assert response.results[1].title == "Mock Result 1 for test query"


@pytest.mark.asyncio
async def test_search_detailed_rerank_results_override_disables_configured_rerank(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Call-level rerank_results=False prevents configured result reranking."""
    mock_config.llm = LLMConfig(
        enabled=True,
        result_rerank=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_rerank(query: str, results: list[SearchResult], config: LLMConfig) -> list[SearchResult]:
        msg = "rerank should not be called"
        raise AssertionError(msg)

    monkeypatch.setattr("twat_search.web.api.rerank_search_results", fake_rerank)

    response = await search_detailed(
        "test query",
        engines=["mock"],
        config=mock_config,
        rerank_results=False,
    )

    assert response.request.params["rerank_results"] is False
    assert "llm_rerank" not in response.request.params
    assert response.results[0].title == "Mock Result 1 for test query"


@pytest.mark.asyncio
async def test_search_detailed_records_rerank_error_and_uses_provider_order(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Rerank failures are provenance, not whole-search failures."""
    mock_config.llm = LLMConfig(enabled=True, result_rerank=True, model="gpt-test", api_key="key")

    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert "base_url" in response.request.params["llm_rerank_error"]
    assert response.results[0].title == "Mock Result 1 for test query"


@pytest.mark.asyncio
async def test_search_detailed_uses_llm_answer_synthesis(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """LLM answer synthesis runs after fan-out and records answer provenance."""
    mock_config.llm = LLMConfig(
        enabled=True,
        answer_synthesis=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_synthesis(
        query: str,
        results: list[SearchResult],
        failures: list[SearchFailure],
        config: LLMConfig,
    ) -> SearchAnswer:
        assert query == "test query"
        assert len(results) == 2
        assert failures == []
        assert config.model == "gpt-test"
        return SearchAnswer(
            text="Synthesized answer.",
            cited_urls=[str(results[0].url)],
            model="gpt-test",
            prompt_version="twat-search-synthesis-v1",
            input_result_count=len(results),
            source_failures=failures,
        )

    monkeypatch.setattr("twat_search.web.api.synthesize_search_answer", fake_synthesis)

    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert response.answer is not None
    assert response.answer.text == "Synthesized answer."
    assert response.request.params["llm_answer"] == {
        "model": "gpt-test",
        "cited_url_count": 1,
        "source_failure_count": 0,
    }


@pytest.mark.asyncio
async def test_search_detailed_answer_synthesis_preserves_failures(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Synthesis receives and returns provider failures instead of hiding them."""
    mock_config.llm = LLMConfig(
        enabled=True,
        answer_synthesis=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_synthesis(
        query: str,
        results: list[SearchResult],
        failures: list[SearchFailure],
        config: LLMConfig,
    ) -> SearchAnswer:
        assert failures
        return SearchAnswer(
            text="Partial answer; one source failed.",
            cited_urls=[str(results[0].url)],
            model=str(config.model),
            prompt_version="twat-search-synthesis-v1",
            input_result_count=len(results),
            source_failures=failures,
        )

    monkeypatch.setattr("twat_search.web.api.synthesize_search_answer", fake_synthesis)

    response = await search_detailed("test query", engines=["mock", "nonexistent"], config=mock_config)

    assert response.failures
    assert response.answer is not None
    assert response.answer.source_failures == response.failures
    assert response.request.params["llm_answer"]["source_failure_count"] == len(response.failures)


@pytest.mark.asyncio
async def test_search_detailed_synthesize_answer_override_disables_configured_synthesis(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Call-level synthesize_answer=False prevents configured answer synthesis."""
    mock_config.llm = LLMConfig(
        enabled=True,
        answer_synthesis=True,
        model="gpt-test",
        api_key="key",
        base_url="https://llm.example/v1",
    )

    async def fake_synthesis(
        query: str,
        results: list[SearchResult],
        failures: list[SearchFailure],
        config: LLMConfig,
    ) -> SearchAnswer:
        msg = "synthesis should not be called"
        raise AssertionError(msg)

    monkeypatch.setattr("twat_search.web.api.synthesize_search_answer", fake_synthesis)

    response = await search_detailed(
        "test query",
        engines=["mock"],
        config=mock_config,
        synthesize_answer=False,
    )

    assert response.answer is None
    assert response.request.params["synthesize_answer"] is False
    assert "llm_answer" not in response.request.params


@pytest.mark.asyncio
async def test_search_detailed_records_answer_synthesis_error(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Synthesis failures are provenance, not whole-search failures."""
    mock_config.llm = LLMConfig(enabled=True, answer_synthesis=True, model="gpt-test", api_key="key")

    response = await search_detailed("test query", engines=["mock"], config=mock_config)

    assert response.answer is None
    assert "base_url" in response.request.params["llm_answer_error"]
    assert response.results


@pytest.mark.asyncio
async def test_search_detailed_records_initialization_failure(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Initialization failures are visible without flattening away context."""
    response = await search_detailed("test query", engines=["nonexistent"], config=mock_config)

    assert response.results == []
    assert response.engines[0].engine == "nonexistent"
    assert response.engines[0].status == "failed"
    assert response.failures[0].kind == "initialization"


@pytest.mark.asyncio
async def test_search_with_nonexistent_engine(
    mock_config: Config,
    setup_teardown: None,
) -> None:
    """Test search with a non-existent engine raises SearchError."""
    with pytest.raises(SearchError, match="No search engines could be initialized"):
        await search("test query", engines=["nonexistent"], config=mock_config)


@pytest.mark.asyncio
async def test_search_with_disabled_engine(
    mock_config: Config,
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Test search with a disabled engine raises SearchError."""
    # Disable the mock engine
    mock_config.engines["mock"].enabled = False

    with pytest.raises(SearchError, match="No search engines could be initialized"):
        await search("test query", engines=["mock"], config=mock_config)


@pytest.mark.asyncio
async def test_search_without_engines_uses_catalog_route(setup_teardown: None) -> None:
    """Search with engines=None selects configured catalog-backed route engines."""
    config = Config(
        engines={
            "mock": EngineConfig(enabled=True, default_params={"result_count": 1}),
            "duckduckgo": EngineConfig(enabled=False),
            "brave": EngineConfig(enabled=True, api_key=None),
        },
    )

    with pytest.raises(SearchError, match="No search engines configured for route 'best'"):
        await search("test query", config=config)
