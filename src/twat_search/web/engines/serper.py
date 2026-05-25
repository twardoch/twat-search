# this_file: src/twat_search/web/engines/serper.py
"""Serper Google Search API engine."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, SERPER
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class SerperOrganicResult(BaseModel):
    """Organic result returned by Serper."""

    title: str = ""
    link: HttpUrl
    snippet: str = ""
    position: int | None = None


class SerperSearchResponse(BaseModel):
    """Serper search response section used by this adapter."""

    organic: list[SerperOrganicResult] = Field(default_factory=list)


@register_engine
class SerperSearchEngine(SearchEngine):
    """Implementation of Serper's Google Search API."""

    engine_code = SERPER
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[SERPER]
    env_api_key_names: ClassVar[list[str]] = ["SERPER_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        gl: str | None = None,
        hl: str | None = None,
        location: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Serper engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://google.serper.dev/search"
        self.num_results = num_results
        self.gl = gl or country or self.config.default_params.get("gl")
        self.hl = hl or language or self.config.default_params.get("hl")
        self.location = location or self.config.default_params.get("location")

        if not self.config.api_key:
            raise EngineError(
                self.engine_code,
                f"Serper API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

    def _build_payload(self, query: str) -> dict[str, Any]:
        """Build the Serper request payload."""
        payload: dict[str, Any] = {
            "q": query,
            "num": self._get_num_results(min_value=1),
        }
        if self.gl:
            payload["gl"] = self.gl
        if self.hl:
            payload["hl"] = self.hl
        if self.location:
            payload["location"] = self.location
        return payload

    def _convert_result(self, item: SerperOrganicResult, raw: dict[str, Any]) -> SearchResult:
        """Convert a Serper organic result into the normalized result model."""
        return SearchResult(
            title=item.title,
            url=item.link,
            snippet=item.snippet,
            source=self.engine_code,
            rank=item.position,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using Serper."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self.base_url,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-API-KEY": self.config.api_key or "",
            },
            json_data=self._build_payload(query),
        )

        try:
            data = response.json()
            parsed = SerperSearchResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        results = []
        organic_items = data.get("organic", [])
        for item, raw in zip(parsed.organic, organic_items, strict=False):
            results.append(self._convert_result(item, raw))

        return self.limit_results(results)


async def serper(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    gl: str | None = None,
    hl: str | None = None,
    location: str | None = None,
) -> list[SearchResult]:
    """Search using Serper's Google Search API."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = SerperSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        gl=gl,
        hl=hl,
        location=location,
    )
    return await engine.search(query)
