#!/usr/bin/env python
# this_file: tests/unit/web/test_models.py
"""
Unit tests for the twat_search.web.models module.

This module tests the data models used in the web search API,
particularly the SearchResult model and its validation.
"""

from __future__ import annotations

import pytest
from pydantic import HttpUrl, ValidationError

from twat_search.web.models import (
    EngineExecutionContext,
    EngineOutcome,
    EngineParameterSet,
    EngineRequest,
    ResultProcessingPolicy,
    RoutePolicy,
    SearchAnswer,
    SearchFailure,
    SearchRequest,
    SearchResponse,
    SearchResult,
)


def test_search_result_valid_data() -> None:
    """Test creating a SearchResult with valid data."""
    # Convert string to HttpUrl using Pydantic's model validation
    url = HttpUrl("https://example.com")
    result = SearchResult(
        title="Test Result",
        url=url,
        snippet="This is a test result",
        source="test_engine",
    )

    assert result.title == "Test Result"
    assert str(result.url) == "https://example.com/"
    assert result.snippet == "This is a test result"
    assert result.source == "test_engine"
    assert result.rank is None
    assert result.raw is None


def test_search_result_with_optional_fields() -> None:
    """Test creating a SearchResult with all fields."""
    raw_data = {"key": "value"}
    url = HttpUrl("https://example.com")
    result = SearchResult(
        title="Test Result",
        url=url,
        snippet="This is a test result",
        source="test_engine",
        rank=1,
        raw=raw_data,
    )

    assert result.rank == 1
    assert result.raw == raw_data


def test_search_result_invalid_url() -> None:
    """Test that invalid URLs raise validation errors."""
    with pytest.raises(ValidationError):
        # This will fail at validation inside SearchResult model
        SearchResult.model_validate(
            {
                "title": "Test Result",
                "url": "not-a-valid-url",  # Invalid URL as string
                "snippet": "This is a test result",
                "source": "test_engine",
            },
        )


def test_search_result_empty_fields() -> None:
    """Test that empty source field raises validation error, but empty title and snippet are allowed."""
    url = HttpUrl("https://example.com")

    # Test empty source (should still raise error)
    with pytest.raises(ValidationError):
        SearchResult(
            title="Test Title",
            url=url,
            snippet="Test snippet",
            source="",  # Empty source should raise error
        )

    # Test empty title and snippet (should be allowed now)
    result = SearchResult(
        title="",
        url=url,
        snippet="",
        source="test_source",
    )
    assert result.title == ""
    assert result.snippet == ""
    assert result.source == "test_source"


def test_search_result_serialization() -> None:
    """Test that SearchResult can be serialized to dict and json."""
    url = HttpUrl("https://example.com")
    result = SearchResult(
        title="Test Result",
        url=url,
        snippet="This is a test result",
        source="test_engine",
        rank=1,
    )

    # Test dict serialization
    result_dict = result.model_dump()
    assert result_dict["title"] == "Test Result"
    # In Pydantic v2, the URL is serialized as a HttpUrl object
    assert str(result_dict["url"]) == "https://example.com/"
    assert result_dict["snippet"] == "This is a test result"
    assert result_dict["source"] == "test_engine"
    assert result_dict["rank"] == 1

    # Test JSON serialization
    result_json = result.model_dump_json()
    assert isinstance(result_json, str)
    assert "Test Result" in result_json
    assert "https://example.com/" in result_json


def test_search_result_deserialization() -> None:
    """Test that SearchResult can be deserialized from dict."""
    data = {
        "title": "Test Result",
        "url": "https://example.com",  # String URL is OK for deserialization
        "snippet": "This is a test result",
        "source": "test_engine",
        "rank": 1,
    }

    result = SearchResult.model_validate(data)
    assert result.title == "Test Result"
    assert str(result.url) == "https://example.com/"
    assert result.snippet == "This is a test result"
    assert result.source == "test_engine"
    assert result.rank == 1


def test_result_processing_policy_deduplicates_and_limits_results() -> None:
    """Result processing deduplicates normalized URLs and records provenance."""
    policy = ResultProcessingPolicy(deduplicate=True, max_results=1)
    results = [
        SearchResult(title="One", url="https://Example.com/path/?b=2&a=1#frag", snippet="", source="a"),
        SearchResult(title="Duplicate", url="https://example.com/path?a=1&b=2", snippet="", source="b"),
        SearchResult(title="Two", url="https://example.com/other", snippet="", source="c"),
    ]

    processed, metadata = policy.process_results(results)

    assert [result.title for result in processed] == ["One"]
    assert metadata == {
        "input_result_count": 3,
        "output_result_count": 1,
        "duplicate_result_count": 1,
        "truncated_result_count": 1,
        "deduplicate": True,
        "deduplicate_by": "url",
        "max_results": 1,
    }


def test_search_request_rejects_empty_query() -> None:
    """SearchRequest parses and rejects invalid user input at the boundary."""
    with pytest.raises(ValidationError):
        SearchRequest(query="   ")


def test_search_request_serializes_route_policy() -> None:
    """SearchRequest can carry a parsed route policy at the API boundary."""
    request = SearchRequest(
        query="font tools",
        route="browser",
        route_policy=RoutePolicy(
            name="browser",
            transports=("browser",),
            require_proxy_support=True,
        ),
    )

    data = request.model_dump()

    assert data["route"] == "browser"
    assert data["route_policy"]["name"] == "browser"
    assert data["route_policy"]["transports"] == ("browser",)
    assert data["route_policy"]["require_proxy_support"] is True


def test_engine_request_serializes_execution_context() -> None:
    """EngineRequest can carry parsed provider parameter provenance."""
    parameter_set = EngineParameterSet(
        engine="brave",
        requested_engines=("brave", "duckduckgo"),
        common_params={"num_results": 5, "country": "US"},
        engine_specific_params={"freshness": "pd"},
        passthrough_params={},
        params={"num_results": 5, "country": "US", "freshness": "pd"},
        param_sources={
            "num_results": "common",
            "country": "common",
            "freshness": "engine_specific",
        },
        engine_specific_prefixes=("brave",),
    )
    execution = EngineExecutionContext(
        engine="brave",
        route="best",
        parameter_set=parameter_set,
        params={"num_results": 5, "country": "US", "freshness": "pd"},
        param_sources={
            "num_results": "common",
            "country": "common",
            "freshness": "engine_specific",
        },
        engine_specific_prefixes=("brave",),
    )
    request = EngineRequest(
        engine="brave",
        query="font tools",
        params=execution.params,
        execution=execution,
        route="best",
    )

    data = request.model_dump()

    assert data["execution"]["engine"] == "brave"
    assert data["execution"]["route"] == "best"
    assert data["execution"]["params"]["freshness"] == "pd"
    assert data["execution"]["param_sources"]["freshness"] == "engine_specific"
    assert data["execution"]["parameter_set"]["engine_specific_params"] == {"freshness": "pd"}
    assert data["execution"]["parameter_set"]["requested_engines"] == ("brave", "duckduckgo")


def test_search_response_serializes_engine_failures() -> None:
    """Detailed responses carry results and first-class provider failures."""
    engine_request = EngineRequest(
        engine="mock",
        query="test",
        params={"num_results": 2},
        route="best",
        transport="plugin",
        proxy_policy="optional",
        proxy_transports=("httpx",),
        browser_required=False,
        result_kinds=("web", "code"),
    )
    failure = SearchFailure(
        engine="mock",
        kind="timeout",
        message="request timed out",
        exception_type="TimeoutError",
        retryable=True,
        details={"attempts": 3},
    )
    response = SearchResponse(
        request=SearchRequest(query="test"),
        engines=[EngineOutcome(engine="mock", status="failed", request=engine_request, failure=failure)],
        failures=[failure],
    )

    data = response.model_dump()
    assert data["request"]["query"] == "test"
    assert data["engines"][0]["request"]["params"] == {"num_results": 2}
    assert data["engines"][0]["request"]["transport"] == "plugin"
    assert data["engines"][0]["request"]["proxy_policy"] == "optional"
    assert data["engines"][0]["request"]["proxy_transports"] == ("httpx",)
    assert data["engines"][0]["request"]["result_kinds"] == ("web", "code")
    assert data["engines"][0]["status"] == "failed"
    assert data["failures"][0]["kind"] == "timeout"
    assert data["failures"][0]["retryable"] is True
    assert data["failures"][0]["details"] == {"attempts": 3}


def test_search_response_serializes_answer_with_failures() -> None:
    """Detailed responses can carry synthesized answers without hiding failures."""
    failure = SearchFailure(engine="mock", kind="empty", message="no results")
    response = SearchResponse(
        request=SearchRequest(query="test"),
        engines=[EngineOutcome(engine="mock", status="empty", failure=failure)],
        failures=[failure],
        answer=SearchAnswer(
            text="A cited answer.",
            cited_urls=["https://example.com/source"],
            model="gpt-test",
            prompt_version="twat-search-synthesis-v1",
            input_result_count=1,
            source_failures=[failure],
        ),
    )

    data = response.model_dump()
    assert data["answer"]["text"] == "A cited answer."
    assert str(data["answer"]["cited_urls"][0]) == "https://example.com/source"
    assert data["answer"]["source_failures"][0]["kind"] == "empty"
