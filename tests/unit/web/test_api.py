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

import twat_search.web.api as api_module
from twat_search.web.api import (
    build_engine_execution_context,
    build_engine_parameter_set,
    init_engine_task,
    search,
    search_detailed,
)
from twat_search.web.browser import BrowserChallengeError, build_browser_evidence
from twat_search.web.config import Config, EngineConfig, LLMConfig, ResultProcessingConfig
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


class DuplicateResultEngine(SearchEngine):
    """Mock engine that emits duplicate URLs for result-processing tests."""

    engine_code = "duplicate_result"

    async def search(self, query: str) -> list[SearchResult]:
        """Return duplicate and unique URLs."""
        return [
            SearchResult(title="First", url="https://example.com/item?b=2&a=1", snippet=query, source=self.engine_code),
            SearchResult(
                title="Duplicate",
                url="https://EXAMPLE.com/item?a=1&b=2#frag",
                snippet=query,
                source=self.engine_code,
            ),
            SearchResult(title="Second", url="https://example.com/second", snippet=query, source=self.engine_code),
        ]


register_engine(DuplicateResultEngine)


class BrowserBlockedEngine(SearchEngine):
    """Mock browser engine that raises structured browser evidence."""

    engine_code = "browser_blocked"

    async def search(self, query: str) -> list[SearchResult]:
        """Raise a browser challenge with CAPTCHA evidence."""
        evidence = build_browser_evidence(
            engine=self.engine_code,
            query=query,
            html='<form action="/sorry/index"><div class="g-recaptcha-response"></div></form>',
            url="https://www.google.com/sorry/index",
            title="Google Sorry",
        )
        raise BrowserChallengeError(evidence)


register_engine(BrowserBlockedEngine)


class FailureKindEngine(SearchEngine):
    """Mock engine that raises representative provider failures."""

    engine_code = "failure_kind"

    async def search(self, query: str) -> list[SearchResult]:
        """Raise the failure requested by the query text."""
        errors: dict[str, Exception] = {
            "auth": Exception("401 unauthorized API key"),
            "timeout": TimeoutError("provider timeout"),
            "block": Exception("captcha blocked by rate limit"),
            "parse": ValueError("json parse error"),
            "schema": Exception("schema field missing"),
            "generic": RuntimeError("upstream provider exploded"),
        }
        raise errors[query]


register_engine(FailureKindEngine)


class RawAliasEngine(SearchEngine):
    """Mock engine used to prove only canonical config keys are consumed."""

    engine_code = "raw_alias"

    async def search(self, query: str) -> list[SearchResult]:
        """Return a single result for the normalized engine alias."""
        return [
            SearchResult(
                title=f"Raw Alias Result for {query}",
                url=HttpUrl("https://example.com/raw-alias"),
                snippet=query,
                source=self.engine_code,
            ),
        ]


register_engine(RawAliasEngine)


@pytest.mark.asyncio
async def test_init_engine_task_ignores_raw_noncanonical_config_key(setup_teardown: None) -> None:
    """Engine initialization reads canonical provider config, not raw legacy spellings."""
    config = Config(engines={"raw-alias": EngineConfig(enabled=False)})

    task_result = init_engine_task("raw-alias", "font tooling", config, engines=["raw-alias"])

    assert isinstance(task_result, tuple)
    assert task_result[0] == "raw-alias"
    outcome = await task_result[1]
    assert outcome.status == "ok"
    assert outcome.request is not None
    assert outcome.request.engine == "raw_alias"


def test_build_engine_execution_context_records_param_sources() -> None:
    """Engine kwargs are parsed into final params with source provenance."""
    context = build_engine_execution_context(
        engine_name="brave",
        engines=["brave", "duckduckgo"],
        kwargs={
            "route": "best",
            "brave_freshness": "pd",
            "duckduckgo_region": "us-en",
            "timeout": 20,
            "engines": ["brave", "duckduckgo"],
        },
        common_params={"num_results": 5, "country": "US"},
    )

    assert context.engine == "brave"
    assert context.route == "best"
    assert context.params == {"num_results": 5, "country": "US", "freshness": "pd", "timeout": 20}
    assert context.param_sources == {
        "num_results": "common",
        "country": "common",
        "freshness": "engine_specific",
        "timeout": "passthrough",
    }
    assert context.engine_specific_prefixes == ("brave",)
    assert context.parameter_set is not None
    assert context.parameter_set.engine_specific_params == {"freshness": "pd"}
    assert context.parameter_set.passthrough_params == {"timeout": 20}
    assert context.parameter_set.common_params == {"num_results": 5, "country": "US"}


def test_build_engine_parameter_set_parses_param_groups() -> None:
    """Raw engine kwargs are parsed into typed parameter groups before execution."""
    parameter_set = build_engine_parameter_set(
        engine_name="brave",
        engines=["brave", "duckduckgo"],
        kwargs={
            "brave_freshness": "pd",
            "duckduckgo_region": "us-en",
            "timeout": 20,
            "route": "deep",
        },
        common_params={"num_results": 5},
    )

    assert parameter_set.engine == "brave"
    assert parameter_set.requested_engines == ("brave", "duckduckgo")
    assert parameter_set.common_params == {"num_results": 5}
    assert parameter_set.engine_specific_params == {"freshness": "pd"}
    assert parameter_set.passthrough_params == {"timeout": 20}
    assert parameter_set.params == {"num_results": 5, "freshness": "pd", "timeout": 20}
    assert parameter_set.param_sources == {
        "num_results": "common",
        "freshness": "engine_specific",
        "timeout": "passthrough",
    }


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
    assert response.request.route == "best"
    assert response.request.route_policy is not None
    assert response.request.route_policy.name == "best"
    assert response.results == response.engines[0].results
    assert response.engines[0].engine == "mock"
    assert response.engines[0].status == "ok"
    assert response.engines[0].request is not None
    assert response.engines[0].request.engine == "mock"
    assert response.engines[0].request.query == "test query"
    assert response.engines[0].request.params["num_results"] == 5
    assert response.engines[0].request.execution is not None
    assert response.engines[0].request.execution.request_policy is not None
    assert response.engines[0].request.execution.request_policy.timeout == 10.0
    assert response.engines[0].request.execution.param_sources["num_results"] == "common"
    assert response.engines[0].request.execution.param_sources["result_count"] == "passthrough"
    assert response.engines[0].request.execution.param_sources["timeout"] == "common"
    assert response.engines[0].request.execution.parameter_set is not None
    assert response.engines[0].request.execution.parameter_set.common_params["num_results"] == 5
    assert response.engines[0].request.execution.parameter_set.passthrough_params["result_count"] == 2
    assert response.engines[0].request.transport is None
    assert response.failures == []


@pytest.mark.asyncio
async def test_search_detailed_applies_result_processing_policy(setup_teardown: None) -> None:
    """Detailed search applies typed result-processing policy after fan-out."""
    config = Config(
        engines={"duplicate_result": EngineConfig(api_key="mock_key", enabled=True)},
        result_processing=ResultProcessingConfig(deduplicate=True, max_results=1),
    )

    response = await search_detailed("dedupe", engines=["duplicate_result"], config=config)

    assert [result.title for result in response.results] == ["First"]
    assert response.request.result_processing is not None
    assert response.request.result_processing.deduplicate is True
    assert response.request.params["result_processing"] == {
        "input_result_count": 3,
        "output_result_count": 1,
        "duplicate_result_count": 1,
        "truncated_result_count": 1,
        "deduplicate": True,
        "deduplicate_by": "url",
        "max_results": 1,
    }


@pytest.mark.asyncio
async def test_search_detailed_records_provider_transport_metadata(setup_teardown: None) -> None:
    """Detailed search outcomes expose transport facts for known providers."""
    config = Config(engines={"plugin_search": EngineConfig(enabled=True)})

    response = await search_detailed("font tools", engines=["plugin_search"], config=config)

    assert response.engines[0].status == "ok"
    assert response.engines[0].request is not None
    assert response.engines[0].request.transport == "plugin"
    assert response.engines[0].request.proxy_policy == "none"
    assert response.engines[0].request.proxy_transports == ()
    assert response.engines[0].request.browser_required is False
    assert response.engines[0].request.result_kinds == ("web", "code", "repository")


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
async def test_search_detailed_preserves_browser_failure_evidence(setup_teardown: None) -> None:
    """Browser challenge exceptions become structured failure details."""
    config = Config(
        engines={
            "browser_blocked": EngineConfig(enabled=True),
        },
    )

    response = await search_detailed("font tooling", engines=["browser_blocked"], config=config)

    failure = response.failures[0]
    assert response.results == []
    assert response.engines[0].status == "failed"
    assert failure.kind == "block"
    assert failure.retryable is True
    assert failure.exception_type == "BrowserChallengeError"
    assert failure.details["browser"]["blocked"] is True
    assert failure.details["browser"]["url"] == "https://www.google.com/sorry/index"
    assert {signal["kind"] for signal in failure.details["browser"]["signals"]} >= {"captcha"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("query", "expected_kind", "expected_retryable", "expected_exception_type"),
    [
        ("auth", "auth", False, "Exception"),
        ("timeout", "timeout", True, "TimeoutError"),
        ("block", "block", True, "Exception"),
        ("parse", "parse", False, "ValueError"),
        ("schema", "schema_drift", False, "Exception"),
        ("generic", "provider_error", True, "RuntimeError"),
    ],
)
async def test_search_detailed_classifies_provider_failure_kinds(
    query: str,
    expected_kind: str,
    expected_retryable: bool,
    expected_exception_type: str,
    setup_teardown: None,
) -> None:
    """Provider exceptions are mapped to stable first-class failure kinds."""
    config = Config(engines={"failure_kind": EngineConfig(enabled=True)})

    response = await search_detailed(query, engines=["failure_kind"], config=config)

    failure = response.failures[0]
    assert response.results == []
    assert response.engines[0].status == "failed"
    assert failure.engine == "failure_kind"
    assert failure.kind == expected_kind
    assert failure.retryable is expected_retryable
    assert failure.exception_type == expected_exception_type


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
    mock_config.result_processing = ResultProcessingConfig(deduplicate=False)

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
    assert [outcome.request.query for outcome in response.engines if outcome.request is not None] == [
        "test query",
        "focused query",
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


@pytest.mark.asyncio
async def test_search_detailed_does_not_fallback_outside_selected_route(
    monkeypatch: MonkeyPatch,
    setup_teardown: None,
) -> None:
    """Route execution fails loudly instead of broadening to unrelated registered engines."""
    config = Config(engines={"mock": EngineConfig(enabled=True)})
    attempted: list[str] = []

    def fake_select_route_engines(**_kwargs: Any) -> list[str]:
        return ["mock"]

    def fake_init_engine_task(engine_name: str, *_args: Any, **_kwargs: Any) -> None:
        attempted.append(engine_name)
        msg = "forced initialization breakage"
        raise RuntimeError(msg)

    monkeypatch.setattr(api_module, "select_route_engines", fake_select_route_engines)
    monkeypatch.setattr(api_module, "init_engine_task", fake_init_engine_task)

    with pytest.raises(SearchError, match="No search engines could be initialized from selected engines: mock"):
        await search_detailed("test query", config=config, strict_mode=False)

    assert attempted == ["mock"]
