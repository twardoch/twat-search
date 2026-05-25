# this_file: src/twat_search/web/engines/jina.py
"""Jina AI web search engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar
from urllib.parse import quote

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, JINA
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class JinaSearchItem(BaseModel):
    """Search item returned by Jina search JSON output."""

    title: str = ""
    url: HttpUrl
    content: str | None = None
    description: str | None = None
    snippet: str | None = None
    timestamp: str | None = None


class JinaSearchResponse(BaseModel):
    """Flexible Jina search response wrapper."""

    data: list[JinaSearchItem] = Field(default_factory=list)
    results: list[JinaSearchItem] = Field(default_factory=list)


@register_engine
class JinaSearchEngine(SearchEngine):
    """Implementation of Jina's web search endpoint."""

    engine_code = JINA
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[JINA]
    env_api_key_names: ClassVar[list[str]] = ["JINA_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        include_content: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Jina search engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://s.jina.ai"
        self.include_content = self._coalesce_bool(include_content, "include_content", True)

    def _coalesce_bool(self, explicit: bool | None, config_key: str, fallback: bool) -> bool:
        """Choose an explicit bool, config default, or fallback."""
        if explicit is not None:
            return explicit
        value = self.config.default_params.get(config_key)
        return fallback if value is None else bool(value)

    def _build_url(self, query: str) -> str:
        """Build Jina search URL."""
        return f"{self.base_url}/{quote(query.strip(), safe='')}"

    def _extract_items(self, data: Any) -> list[JinaSearchItem]:
        """Parse Jina response variants into search items."""
        if isinstance(data, list):
            return [JinaSearchItem.model_validate(item) for item in data]
        if isinstance(data, dict):
            parsed = JinaSearchResponse.model_validate(data)
            return parsed.data or parsed.results
        msg = f"Unexpected Jina response type: {type(data).__name__}"
        raise ValueError(msg)

    def _convert_result(self, item: JinaSearchItem, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one Jina result into the normalized result model."""
        snippet = item.content if self.include_content and item.content else item.description or item.snippet or ""
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
        """Perform a web search using Jina."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self._build_url(query),
            method="GET",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.config.api_key or ''}",
            },
        )

        try:
            data = response.json()
            items = self._extract_items(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        raw_items: list[dict[str, Any]]
        if isinstance(data, list):
            raw_items = data
        elif isinstance(data, dict):
            raw_items = data.get("data") or data.get("results") or []
        else:
            raw_items = []

        results = [
            self._convert_result(item, rank, raw if isinstance(raw, dict) else {})
            for rank, (item, raw) in enumerate(zip(items, raw_items, strict=False), start=1)
        ]
        return self.limit_results(results)


async def jina(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    include_content: bool | None = None,
) -> list[SearchResult]:
    """Search using Jina AI search."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = JinaSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        include_content=include_content,
    )
    return await engine.search(query)
