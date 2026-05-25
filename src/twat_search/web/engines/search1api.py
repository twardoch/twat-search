# this_file: src/twat_search/web/engines/search1api.py
"""Search1API web search engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, SEARCH1API
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class Search1ApiResult(BaseModel):
    """One result item returned by Search1API search."""

    title: str = ""
    link: HttpUrl
    snippet: str = ""
    content: str | None = None


class Search1ApiResponse(BaseModel):
    """Top-level Search1API search response."""

    search_parameters: dict[str, Any] = Field(default_factory=dict, alias="searchParameters")
    results: list[Search1ApiResult] = Field(default_factory=list)


@register_engine
class Search1ApiSearchEngine(SearchEngine):
    """Implementation of the Search1API search endpoint."""

    engine_code = SEARCH1API
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[SEARCH1API]
    env_api_key_names: ClassVar[list[str]] = ["SEARCH1API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        search_service: str | None = None,
        crawl_results: int | None = None,
        include_content: bool | None = None,
        image: bool | None = None,
        include_sites: list[str] | None = None,
        exclude_sites: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Search1API engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://api.search1api.com/search"
        self.search_service = search_service or self.config.default_params.get("search_service", "google")
        self.crawl_results = self._coalesce_int(crawl_results, "crawl_results", 0, min_value=0, max_value=10)
        self.include_content = self._coalesce_bool(include_content, "include_content", True)
        self.image = self._coalesce_bool(image, "image", False)
        self.include_sites = (
            include_sites if include_sites is not None else self.config.default_params.get("include_sites", [])
        )
        self.exclude_sites = (
            exclude_sites if exclude_sites is not None else self.config.default_params.get("exclude_sites", [])
        )

    def _coalesce_bool(self, explicit: bool | None, config_key: str, fallback: bool) -> bool:
        """Choose an explicit bool, config default, or fallback."""
        if explicit is not None:
            return explicit
        value = self.config.default_params.get(config_key)
        return fallback if value is None else bool(value)

    def _coalesce_int(
        self,
        explicit: int | None,
        config_key: str,
        fallback: int,
        *,
        min_value: int,
        max_value: int,
    ) -> int:
        """Choose and clamp an integer request parameter."""
        value = explicit if explicit is not None else self.config.default_params.get(config_key, fallback)
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            parsed = fallback
        return min(max(parsed, min_value), max_value)

    def _build_payload(self, query: str) -> dict[str, Any]:
        """Build a Search1API single-search payload."""
        payload: dict[str, Any] = {
            "query": query,
            "search_service": self.search_service,
            "max_results": min(self._get_num_results(min_value=1), 100),
            "crawl_results": self.crawl_results,
            "image": self.image,
            "include_sites": self.include_sites or [],
            "exclude_sites": self.exclude_sites or [],
        }
        if self.language:
            payload["language"] = self.language
        if self.time_frame:
            payload["time_range"] = self.time_frame
        return payload

    def _convert_result(self, item: Search1ApiResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one Search1API item into the normalized result model."""
        snippet = item.content if self.include_content and item.content else item.snippet
        snippet = textwrap.shorten(snippet.strip(), width=500, placeholder="...")
        return SearchResult(
            title=item.title,
            url=item.link,
            snippet=snippet,
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using Search1API."""
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
            parsed = Search1ApiResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        raw_results = data.get("results", []) if isinstance(data, dict) else []
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.results, raw_results, strict=False), start=1)
        ]
        return self.limit_results(results)


async def search1api(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    search_service: str | None = None,
    crawl_results: int | None = None,
    include_content: bool | None = None,
) -> list[SearchResult]:
    """Search using Search1API."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = Search1ApiSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        search_service=search_service,
        crawl_results=crawl_results,
        include_content=include_content,
    )
    return await engine.search(query)
