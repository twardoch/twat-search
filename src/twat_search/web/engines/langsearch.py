# this_file: src/twat_search/web/engines/langsearch.py
"""LangSearch web search API engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, LANGSEARCH
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class LangSearchResult(BaseModel):
    """One web page returned by LangSearch."""

    name: str = ""
    url: HttpUrl
    snippet: str = ""
    summary: str | None = None
    display_url: str | None = Field(default=None, alias="displayUrl")
    date_published: str | None = Field(default=None, alias="datePublished")
    date_last_crawled: str | None = Field(default=None, alias="dateLastCrawled")


class LangSearchWebPages(BaseModel):
    """LangSearch webPages wrapper."""

    value: list[LangSearchResult] = Field(default_factory=list)


class LangSearchData(BaseModel):
    """LangSearch data wrapper."""

    web_pages: LangSearchWebPages = Field(default_factory=LangSearchWebPages, alias="webPages")


class LangSearchResponse(BaseModel):
    """Top-level LangSearch response."""

    code: int = 200
    msg: str | None = None
    data: LangSearchData = Field(default_factory=LangSearchData)


@register_engine
class LangSearchEngine(SearchEngine):
    """Implementation of the LangSearch Web Search API."""

    engine_code = LANGSEARCH
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[LANGSEARCH]
    env_api_key_names: ClassVar[list[str]] = ["LANGSEARCH_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        freshness: str | None = None,
        summary: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the LangSearch engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://api.langsearch.com/v1/web-search"
        self.freshness = freshness or self._freshness_from_time_frame(time_frame)
        self.summary = self._coalesce_bool(summary, "summary", True)

    def _coalesce_bool(self, explicit: bool | None, config_key: str, fallback: bool) -> bool:
        """Choose an explicit bool, config default, or fallback."""
        if explicit is not None:
            return explicit
        value = self.config.default_params.get(config_key)
        return fallback if value is None else bool(value)

    def _freshness_from_time_frame(self, time_frame: str | None) -> str:
        """Map shared time-frame values to LangSearch freshness values."""
        configured = self.config.default_params.get("freshness")
        if time_frame is None:
            return str(configured or "noLimit")
        normalized = time_frame.lower()
        mapping = {
            "day": "oneDay",
            "oneday": "oneDay",
            "week": "oneWeek",
            "oneweek": "oneWeek",
            "month": "oneMonth",
            "onemonth": "oneMonth",
            "year": "oneYear",
            "oneyear": "oneYear",
            "nolimit": "noLimit",
            "all": "noLimit",
        }
        return mapping.get(normalized, str(configured or "noLimit"))

    def _build_payload(self, query: str) -> dict[str, Any]:
        """Build a LangSearch web-search payload."""
        return {
            "query": query,
            "freshness": self.freshness,
            "summary": self.summary,
            "count": min(self._get_num_results(min_value=1), 10),
        }

    def _convert_result(self, item: LangSearchResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one LangSearch item into the normalized result model."""
        snippet = item.summary if self.summary and item.summary else item.snippet
        snippet = textwrap.shorten(snippet.strip(), width=500, placeholder="...")
        return SearchResult(
            title=item.name,
            url=item.url,
            snippet=snippet,
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using LangSearch."""
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
            parsed = LangSearchResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        if parsed.code != 200:
            msg = parsed.msg or f"LangSearch returned status code {parsed.code}"
            raise EngineError(self.engine_code, msg)

        raw_results = data.get("data", {}).get("webPages", {}).get("value", []) if isinstance(data, dict) else []
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.data.web_pages.value, raw_results, strict=False), start=1)
        ]
        return self.limit_results(results)


async def langsearch(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    freshness: str | None = None,
    summary: bool | None = None,
) -> list[SearchResult]:
    """Search using LangSearch."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = LangSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        freshness=freshness,
        summary=summary,
    )
    return await engine.search(query)
