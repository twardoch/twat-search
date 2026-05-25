# this_file: src/twat_search/web/engines/exa.py
"""Exa Search API engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, EXA
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class ExaResult(BaseModel):
    """Result item returned by Exa search."""

    title: str = ""
    url: HttpUrl
    id: str | None = None
    published_date: str | None = Field(default=None, alias="publishedDate")
    author: str | None = None
    text: str | None = None
    highlights: list[str] = Field(default_factory=list)


class ExaSearchResponse(BaseModel):
    """Top-level Exa search response."""

    request_id: str | None = Field(default=None, alias="requestId")
    search_type: str | None = Field(default=None, alias="searchType")
    results: list[ExaResult] = Field(default_factory=list)


@register_engine
class ExaSearchEngine(SearchEngine):
    """Implementation of Exa's web search API."""

    engine_code = EXA
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[EXA]
    env_api_key_names: ClassVar[list[str]] = ["EXAAI_API_KEY", "EXA_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        search_type: str | None = None,
        category: str | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_text: bool | None = None,
        include_highlights: bool | None = None,
        moderation: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Exa engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://api.exa.ai/search"
        self.search_type = search_type or self.config.default_params.get("search_type", "auto")
        self.category = category or self.config.default_params.get("category")
        self.include_domains = include_domains or self.config.default_params.get("include_domains")
        self.exclude_domains = exclude_domains or self.config.default_params.get("exclude_domains")
        self.include_text = self._coalesce_bool(include_text, "include_text", False)
        self.include_highlights = self._coalesce_bool(include_highlights, "include_highlights", True)
        self.moderation = self._coalesce_bool(moderation, "moderation", False)
        self.user_location = country or self.config.default_params.get("user_location")

    def _coalesce_bool(self, explicit: bool | None, config_key: str, fallback: bool) -> bool:
        """Choose an explicit bool, config default, or fallback."""
        if explicit is not None:
            return explicit
        value = self.config.default_params.get(config_key)
        return fallback if value is None else bool(value)

    def _build_payload(self, query: str) -> dict[str, Any]:
        """Build the Exa search request payload."""
        payload: dict[str, Any] = {
            "query": query,
            "numResults": min(self._get_num_results(min_value=1), 100),
            "type": self.search_type,
        }
        if self.category:
            payload["category"] = self.category
        if self.include_domains:
            payload["includeDomains"] = self.include_domains
        if self.exclude_domains:
            payload["excludeDomains"] = self.exclude_domains
        if self.user_location:
            payload["userLocation"] = self.user_location
        if self.moderation:
            payload["moderation"] = True

        contents: dict[str, Any] = {}
        if self.include_text:
            contents["text"] = True
        if self.include_highlights:
            contents["highlights"] = True
        if contents:
            payload["contents"] = contents
        return payload

    def _convert_result(self, item: ExaResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert an Exa result into the normalized result model."""
        snippet = ""
        if item.highlights:
            snippet = " ".join(item.highlights)
        elif item.text:
            snippet = item.text
        snippet = textwrap.shorten(snippet.strip(), width=500, placeholder="...")
        return SearchResult(
            title=item.title,
            url=item.url,
            snippet=snippet,
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using Exa."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self.base_url,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "x-api-key": self.config.api_key or "",
            },
            json_data=self._build_payload(query),
        )

        try:
            data = response.json()
            parsed = ExaSearchResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        raw_results = data.get("results", [])
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.results, raw_results, strict=False), start=1)
        ]
        return self.limit_results(results)


async def exa(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    search_type: str | None = None,
    category: str | None = None,
    include_text: bool | None = None,
    include_highlights: bool | None = None,
) -> list[SearchResult]:
    """Search using Exa."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = ExaSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        search_type=search_type,
        category=category,
        include_text=include_text,
        include_highlights=include_highlights,
    )
    return await engine.search(query)
