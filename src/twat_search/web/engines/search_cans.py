# this_file: src/twat_search/web/engines/search_cans.py
"""SearchCans SERP API engine."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, SEARCH_CANS
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class SearchCansResult(BaseModel):
    """One result item returned by SearchCans."""

    title: str = ""
    url: HttpUrl
    content: str = ""


class SearchCansResponse(BaseModel):
    """Top-level SearchCans response."""

    code: int = 0
    msg: str = ""
    data: list[SearchCansResult] = []


@register_engine
class SearchCansSearchEngine(SearchEngine):
    """Implementation of the SearchCans SERP API."""

    engine_code = SEARCH_CANS
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[SEARCH_CANS]
    env_api_key_names: ClassVar[list[str]] = ["SEARCH_CANS_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        engine: str | None = None,
        page: int | None = None,
        timeout_ms: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the SearchCans engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://www.searchcans.com/api/search"
        self.search_engine = engine or self.config.default_params.get("engine", "google")
        self.page = self._coalesce_int(page, "page", 1, min_value=1, max_value=100)
        self.timeout_ms = self._coalesce_int(timeout_ms, "timeout_ms", 20000, min_value=1000, max_value=120000)

        if not self.config.api_key:
            raise EngineError(
                self.engine_code,
                f"SearchCans API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

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
        """Build a SearchCans SERP payload."""
        return {
            "s": query,
            "t": self.search_engine,
            "p": self.page,
            "d": self.timeout_ms,
        }

    def _convert_result(self, item: SearchCansResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one SearchCans result into the normalized result model."""
        return SearchResult(
            title=item.title,
            url=item.url,
            snippet=item.content,
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using SearchCans."""
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
            parsed = SearchCansResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        if parsed.code != 0:
            raise EngineError(self.engine_code, parsed.msg or f"SearchCans returned code {parsed.code}")

        raw_results = data.get("data", []) if isinstance(data, dict) else []
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.data, raw_results, strict=False), start=1)
        ]
        return self.limit_results(results)


async def search_cans(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    engine: str | None = None,
    page: int | None = None,
    timeout_ms: int | None = None,
) -> list[SearchResult]:
    """Search using SearchCans."""
    config = EngineConfig(api_key=api_key, enabled=True)
    search_engine = SearchCansSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        engine=engine,
        page=page,
        timeout_ms=timeout_ms,
    )
    return await search_engine.search(query)
