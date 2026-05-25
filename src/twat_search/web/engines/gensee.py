# this_file: src/twat_search/web/engines/gensee.py
"""Gensee Search Agent API engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, GENSEE
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class GenseeResult(BaseModel):
    """One direct retrieval result returned by Gensee."""

    title: str = ""
    url: HttpUrl
    content: str = ""


class GenseeResponse(BaseModel):
    """Top-level Gensee Search Agent response."""

    search_response: list[GenseeResult] = Field(default_factory=list)
    elapsed_time: float | int | None = None


@register_engine
class GenseeSearchEngine(SearchEngine):
    """Implementation of the Gensee Search Agent direct retrieval API."""

    engine_code = GENSEE
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[GENSEE]
    env_api_key_names: ClassVar[list[str]] = ["GENSEE_SEARCH_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        multilingual: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Gensee engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://platform.gensee.ai/tool/search"
        self.multilingual = self._coalesce_bool(multilingual, "multilingual", False)

    def _coalesce_bool(self, explicit: bool | None, config_key: str, fallback: bool) -> bool:
        """Choose an explicit bool, config default, or fallback."""
        if explicit is not None:
            return explicit
        value = self.config.default_params.get(config_key)
        return fallback if value is None else bool(value)

    def _build_params(self, query: str) -> dict[str, Any]:
        """Build documented Gensee Search Agent query parameters."""
        return {
            "query": query,
            "max_results": self._get_num_results(min_value=1),
            "multilingual": str(self.multilingual).lower(),
        }

    def _convert_result(self, item: GenseeResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one Gensee item into the normalized result model."""
        snippet = textwrap.shorten(item.content.strip(), width=500, placeholder="...")
        return SearchResult(
            title=item.title,
            url=item.url,
            snippet=snippet,
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web retrieval request using Gensee Search Agent."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self.base_url,
            method="GET",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key or ''}",
            },
            params=self._build_params(query),
        )

        try:
            data = response.json()
            parsed = GenseeResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        raw_results = data.get("search_response", []) if isinstance(data, dict) else []
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.search_response, raw_results, strict=False), start=1)
        ]
        return self.limit_results(results)


async def gensee(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    multilingual: bool | None = None,
) -> list[SearchResult]:
    """Search using Gensee Search Agent."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = GenseeSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        multilingual=multilingual,
    )
    return await engine.search(query)
