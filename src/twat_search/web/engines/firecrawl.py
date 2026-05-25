# this_file: src/twat_search/web/engines/firecrawl.py
"""Firecrawl Search API engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, FIRECRAWL
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class FirecrawlWebResult(BaseModel):
    """Web result returned by Firecrawl search."""

    title: str = ""
    description: str = ""
    url: HttpUrl
    markdown: str | None = None


class FirecrawlData(BaseModel):
    """Firecrawl search data wrapper."""

    web: list[FirecrawlWebResult] = Field(default_factory=list)


class FirecrawlSearchResponse(BaseModel):
    """Top-level Firecrawl search response."""

    success: bool = False
    data: FirecrawlData = Field(default_factory=FirecrawlData)
    warning: str | None = None
    id: str | None = None
    credits_used: int | None = Field(default=None, alias="creditsUsed")


@register_engine
class FirecrawlSearchEngine(SearchEngine):
    """Implementation of Firecrawl's v2 search endpoint."""

    engine_code = FIRECRAWL
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[FIRECRAWL]
    env_api_key_names: ClassVar[list[str]] = ["FIRECRAWL_API_KEY", "FIRECRAWL_API_KEY_2"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        sources: list[str] | None = None,
        categories: list[str] | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_markdown: bool | None = None,
        location: str | None = None,
        tbs: str | None = None,
        timeout_ms: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Firecrawl engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://api.firecrawl.dev/v2/search"
        self.sources = sources or self.config.default_params.get("sources", ["web"])
        self.categories = categories or self.config.default_params.get("categories")
        self.include_domains = include_domains or self.config.default_params.get("include_domains")
        self.exclude_domains = exclude_domains or self.config.default_params.get("exclude_domains")
        self.include_markdown = self._coalesce_bool(include_markdown, "include_markdown", False)
        self.location = location or self.config.default_params.get("location")
        self.country = country or self.config.default_params.get("country")
        self.tbs = tbs or time_frame or self.config.default_params.get("tbs")
        self.timeout_ms = timeout_ms or self.config.default_params.get("timeout")

    def _coalesce_bool(self, explicit: bool | None, config_key: str, fallback: bool) -> bool:
        """Choose an explicit bool, config default, or fallback."""
        if explicit is not None:
            return explicit
        value = self.config.default_params.get(config_key)
        return fallback if value is None else bool(value)

    def _build_payload(self, query: str) -> dict[str, Any]:
        """Build Firecrawl v2 search payload."""
        payload: dict[str, Any] = {
            "query": query,
            "limit": self._get_num_results(min_value=1),
            "sources": self.sources,
        }
        if self.categories:
            payload["categories"] = [
                {"type": category} if isinstance(category, str) else category for category in self.categories
            ]
        if self.include_domains:
            payload["includeDomains"] = self.include_domains
        if self.exclude_domains:
            payload["excludeDomains"] = self.exclude_domains
        if self.location:
            payload["location"] = self.location
        if self.country:
            payload["country"] = self.country
        if self.tbs:
            payload["tbs"] = self.tbs
        if self.timeout_ms:
            payload["timeout"] = self.timeout_ms
        if self.include_markdown:
            payload["scrapeOptions"] = {"formats": [{"type": "markdown"}]}
        return payload

    def _convert_result(self, item: FirecrawlWebResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one Firecrawl web result into the normalized result model."""
        snippet = item.markdown if self.include_markdown and item.markdown else item.description
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
        """Perform a web search using Firecrawl."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self.base_url,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key or ''}",
            },
            json_data=self._build_payload(query),
        )

        try:
            data = response.json()
            parsed = FirecrawlSearchResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        if not parsed.success:
            raise EngineError(self.engine_code, parsed.warning or "Firecrawl search failed")

        raw_results = data.get("data", {}).get("web", [])
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.data.web, raw_results, strict=False), start=1)
        ]
        return self.limit_results(results)


async def firecrawl(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    include_markdown: bool | None = None,
    categories: list[str] | None = None,
) -> list[SearchResult]:
    """Search using Firecrawl."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = FirecrawlSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        include_markdown=include_markdown,
        categories=categories,
    )
    return await engine.search(query)
