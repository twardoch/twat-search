# this_file: src/twat_search/web/models.py
"""
Pydantic models for the web search API.

This module defines the data models used for inputs and outputs
in the web search API.
"""

from __future__ import annotations

from typing import Any, Literal
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

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
RouteName = Literal["best", "fast", "cheap", "resilient", "deep", "browser", "api-only", "plugins", "all"]
ParamSource = Literal["common", "engine_specific", "passthrough"]
ResultDeduplicationKey = Literal["url", "url_and_title"]


class RoutePolicy(BaseModel):
    """Parsed route policy used to select provider engines."""

    model_config = ConfigDict(frozen=True)

    name: RouteName
    transports: tuple[str, ...] = ()
    cost_classes: tuple[str, ...] = ()
    require_proxy_support: bool | None = None
    include_unkeyed: bool = True
    include_keyed: bool = True
    max_engines: int | None = None
    stability: tuple[str, ...] = ("stable", "beta", "experimental", "fragile")


class RequestPolicy(BaseModel):
    """Parsed network request policy for provider calls."""

    timeout: float = 10.0
    retries: int = 2
    retry_delay: float = 1.0
    min_delay: float = 0.0
    max_parallelism: int = 1
    use_random_user_agent: bool = True
    proxy_enabled: bool = False
    proxy_configured: bool = False
    proxy_provider: str | None = None
    proxy_url: str | None = None
    redacted_proxy_url: str | None = None

    def engine_kwargs(self) -> dict[str, Any]:
        """Return kwargs consumed by shared search engine request helpers."""
        kwargs: dict[str, Any] = {
            "timeout": self.timeout,
            "retries": self.retries,
            "retry_delay": self.retry_delay,
            "min_delay": self.min_delay,
            "use_random_user_agent": self.use_random_user_agent,
        }
        if self.proxy_url:
            kwargs["proxy_url"] = self.proxy_url
        return kwargs


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


class ResultProcessingPolicy(BaseModel):
    """Parsed post-provider result normalization policy."""

    deduplicate: bool = True
    deduplicate_by: ResultDeduplicationKey = "url"
    max_results: int | None = None

    @field_validator("max_results")
    @classmethod
    def validate_max_results(cls, v: int | None) -> int | None:
        """Require positive aggregate result limits when configured."""
        if v is not None and v < 1:
            msg = "max_results must be greater than zero"
            raise ValueError(msg)
        return v

    @staticmethod
    def normalize_url(url: HttpUrl | str) -> str:
        """Normalize a result URL for duplicate detection."""
        parts = urlsplit(str(url))
        query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
        return urlunsplit(
            (
                parts.scheme.lower(),
                parts.netloc.lower(),
                parts.path.rstrip("/") or "/",
                query,
                "",
            ),
        )

    def duplicate_key(self, result: SearchResult) -> str:
        """Return the configured duplicate key for a search result."""
        url_key = self.normalize_url(result.url)
        if self.deduplicate_by == "url_and_title":
            return f"{url_key}\n{result.title.strip().casefold()}"
        return url_key

    def process_results(self, results: list[SearchResult]) -> tuple[list[SearchResult], dict[str, Any]]:
        """Apply aggregate result processing and return provenance metadata."""
        seen: set[str] = set()
        processed: list[SearchResult] = []
        duplicate_count = 0

        for result in results:
            if self.deduplicate:
                key = self.duplicate_key(result)
                if key in seen:
                    duplicate_count += 1
                    continue
                seen.add(key)
            processed.append(result)

        deduped_count = len(processed)
        if self.max_results is not None:
            processed = processed[: self.max_results]

        metadata = {
            "input_result_count": len(results),
            "output_result_count": len(processed),
            "duplicate_result_count": duplicate_count,
            "truncated_result_count": max(deduped_count - len(processed), 0),
            "deduplicate": self.deduplicate,
            "deduplicate_by": self.deduplicate_by,
            "max_results": self.max_results,
        }
        return processed, metadata


class SearchRequest(BaseModel):
    """Parsed user search request shared by API, CLI, and future transports."""

    query: str
    engines: list[str] | None = None
    route: str | None = "best"
    route_policy: RoutePolicy | None = None
    num_results: int = 5
    country: str | None = None
    language: str | None = None
    safe_search: bool = True
    time_frame: str | None = None
    strict_mode: bool = True
    result_processing: ResultProcessingPolicy | None = None
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


class EngineParameterSet(BaseModel):
    """Parsed parameter groups for one provider attempt."""

    engine: str
    requested_engines: tuple[str, ...] = ()
    common_params: dict[str, Any] = Field(default_factory=dict)
    engine_specific_params: dict[str, Any] = Field(default_factory=dict)
    passthrough_params: dict[str, Any] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)
    param_sources: dict[str, ParamSource] = Field(default_factory=dict)
    engine_specific_prefixes: tuple[str, ...] = ()


class EngineExecutionContext(BaseModel):
    """Parsed execution context for one provider attempt."""

    engine: str
    route: str | None = None
    request_policy: RequestPolicy | None = None
    parameter_set: EngineParameterSet | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    param_sources: dict[str, ParamSource] = Field(default_factory=dict)
    engine_specific_prefixes: tuple[str, ...] = ()


class EngineRequest(BaseModel):
    """Concrete request sent to a single provider."""

    engine: str
    query: str
    params: dict[str, Any] = Field(default_factory=dict)
    execution: EngineExecutionContext | None = None
    route: str | None = None
    transport: str | None = None
    proxy_policy: str = "none"
    proxy_transports: tuple[str, ...] = ()
    browser_required: bool = False
    result_kinds: tuple[str, ...] = ()


class SearchFailure(BaseModel):
    """Structured failure for a provider attempt."""

    engine: str
    kind: FailureKind
    message: str
    exception_type: str | None = None
    retryable: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


class EngineOutcome(BaseModel):
    """Result or failure from one engine attempt."""

    engine: str
    status: OutcomeStatus
    request: EngineRequest | None = None
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
