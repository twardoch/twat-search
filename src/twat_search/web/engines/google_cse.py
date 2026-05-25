# this_file: src/twat_search/web/engines/google_cse.py
"""Google Custom Search JSON API engine."""

from __future__ import annotations

import os
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, GOOGLE_CSE
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class GoogleCseResult(BaseModel):
    """Result item returned by Google's Custom Search JSON API."""

    title: str = ""
    link: HttpUrl
    snippet: str = ""


class GoogleCseResponse(BaseModel):
    """Google CSE response section used by this adapter."""

    items: list[GoogleCseResult] = Field(default_factory=list)


@register_engine
class GoogleCseSearchEngine(SearchEngine):
    """Implementation of Google Custom Search JSON API."""

    engine_code = GOOGLE_CSE
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[GOOGLE_CSE]
    env_api_key_names: ClassVar[list[str]] = ["GOOGLE_CSE_API_KEY"]
    env_cx_names: ClassVar[list[str]] = ["GOOGLE_CSE_ID", "GOOGLE_CSE_CX"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        cx: str | None = None,
        gl: str | None = None,
        hl: str | None = None,
        lr: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Google CSE engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.num_results = num_results
        self.cx = cx or self.config.default_params.get("cx") or self._get_cx_from_env()
        self.gl = gl or country or self.config.default_params.get("gl")
        self.hl = hl or language or self.config.default_params.get("hl")
        self.lr = lr or self.config.default_params.get("lr")

        if not self.cx:
            raise EngineError(
                self.engine_code,
                f"Google CSE search engine ID is required. Set it via one of these env vars: {', '.join(self.env_cx_names)}",
            )

    def _get_cx_from_env(self) -> str | None:
        """Return the first configured Google CSE search engine ID."""
        for env_name in self.env_cx_names:
            env_value = os.environ.get(env_name)
            if env_value:
                return env_value
        return None

    def _build_params(self, query: str) -> dict[str, Any]:
        """Build Google CSE query parameters."""
        params: dict[str, Any] = {
            "key": self.config.api_key,
            "cx": self.cx,
            "q": query,
            "num": min(self._get_num_results(min_value=1), 10),
        }
        if self.gl:
            params["gl"] = self.gl
        if self.hl:
            params["hl"] = self.hl
        if self.lr:
            params["lr"] = self.lr
        if self.safe_search is not None:
            params["safe"] = "active" if self.safe_search else "off"
        return params

    def _convert_result(self, item: GoogleCseResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert a Google CSE item into the normalized result model."""
        return SearchResult(
            title=item.title,
            url=item.link,
            snippet=item.snippet,
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using Google Custom Search JSON API."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self.base_url,
            method="GET",
            headers={"Accept": "application/json"},
            params=self._build_params(query),
        )

        try:
            data = response.json()
            parsed = GoogleCseResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        raw_items = data.get("items", [])
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.items, raw_items, strict=False), start=1)
        ]
        return self.limit_results(results)


async def google_cse(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    cx: str | None = None,
    gl: str | None = None,
    hl: str | None = None,
    lr: str | None = None,
) -> list[SearchResult]:
    """Search using Google Custom Search JSON API."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = GoogleCseSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        cx=cx,
        gl=gl,
        hl=hl,
        lr=lr,
    )
    return await engine.search(query)
