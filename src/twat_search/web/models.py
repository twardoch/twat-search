# this_file: src/twat_search/web/models.py
"""
Pydantic models for the web search API.

This module defines the data models used for inputs and outputs
in the web search API.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

FailureKind = Literal[
    "initialization",
    "auth",
    "timeout",
    "block",
    "empty",
    "parse",
    "schema_drift",
    "provider_error",
    "unexpected",
]
OutcomeStatus = Literal["ok", "empty", "failed"]


class SearchResult(BaseModel):
    """
    Represents a single search result from any search engine.

    Attributes:
        title: The title of the search result.
        url: The URL of the search result.
        snippet: A short excerpt or description of the search result.
        source: The name of the search engine that produced this result.
        rank: Optional ranking position (for future ranking functionality).
        raw: The raw, unparsed response from the search engine (for debugging).
    """

    title: str
    url: HttpUrl  # Use Pydantic's HttpUrl for URL validation
    snippet: str
    source: str
    rank: int | None = None  # For future ranking functionality
    raw: dict[str, Any] | None = None  # Store the raw API response

    @field_validator("source")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        """Validate that source field is not empty."""
        if not v or not v.strip():
            msg = "Source field cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("title", "snippet")
    @classmethod
    def ensure_string(cls, v: str) -> str:
        """Ensure string fields are not None and convert to empty string if None."""
        return v.strip() if v and v.strip() else ""


class SearchRequest(BaseModel):
    """Parsed user search request shared by API, CLI, and future transports."""

    query: str
    engines: list[str] | None = None
    route: str | None = "best"
    num_results: int = 5
    country: str | None = None
    language: str | None = None
    safe_search: bool = True
    time_frame: str | None = None
    strict_mode: bool = True
    params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Require a non-empty query at the request boundary."""
        query = v.strip()
        if not query:
            msg = "Query cannot be empty"
            raise ValueError(msg)
        return query


class EngineRequest(BaseModel):
    """Concrete request sent to a single provider."""

    engine: str
    query: str
    params: dict[str, Any] = Field(default_factory=dict)
    route: str | None = None


class SearchFailure(BaseModel):
    """Structured failure for a provider attempt."""

    engine: str
    kind: FailureKind
    message: str
    exception_type: str | None = None
    retryable: bool = False


class EngineOutcome(BaseModel):
    """Result or failure from one engine attempt."""

    engine: str
    status: OutcomeStatus
    results: list[SearchResult] = Field(default_factory=list)
    failure: SearchFailure | None = None


class SearchAnswer(BaseModel):
    """Optional synthesized answer with citations and visible source failures."""

    text: str
    cited_urls: list[HttpUrl] = Field(default_factory=list)
    model: str
    prompt_version: str
    input_result_count: int = 0
    source_failures: list[SearchFailure] = Field(default_factory=list)


class SearchResponse(BaseModel):
    """Detailed multi-engine response with results and per-engine outcomes."""

    request: SearchRequest
    engines: list[EngineOutcome]
    results: list[SearchResult] = Field(default_factory=list)
    failures: list[SearchFailure] = Field(default_factory=list)
    answer: SearchAnswer | None = None
