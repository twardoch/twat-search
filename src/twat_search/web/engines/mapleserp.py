# this_file: src/twat_search/web/engines/mapleserp.py
"""MapleSERP search API engine."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError, model_validator
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, MAPLESERP
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class MapleSerpOrganicResult(BaseModel):
    """Organic result returned by MapleSERP."""

    title: str = ""
    link: HttpUrl | None = None
    url: HttpUrl | None = None
    snippet: str = ""
    description: str | None = None
    position: int | None = None

    @model_validator(mode="after")
    def require_url(self) -> MapleSerpOrganicResult:
        """Accept either link or url as the canonical result URL."""
        if self.link is None and self.url is None:
            msg = "MapleSERP organic result requires link or url"
            raise ValueError(msg)
        return self

    @property
    def result_url(self) -> HttpUrl:
        """Return the provider result URL."""
        return self.link or self.url  # type: ignore[return-value]

    @property
    def result_snippet(self) -> str:
        """Return the best available text snippet."""
        return self.description or self.snippet


class MapleSerpResponse(BaseModel):
    """Top-level MapleSERP response section used by this adapter."""

    organic_results: list[MapleSerpOrganicResult] = Field(default_factory=list)


@register_engine
class MapleSerpSearchEngine(SearchEngine):
    """Implementation of MapleSERP's SERP API."""

    engine_code = MAPLESERP
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[MAPLESERP]
    env_api_key_names: ClassVar[list[str]] = ["MAPLESERP_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        engine: str | None = None,
        search_type: str | None = None,
        device: str | None = None,
        location: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the MapleSERP engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://mapleserp.io/api/serp/search"
        self.search_engine = engine or self.config.default_params.get("engine", "google")
        self.search_type = search_type or self.config.default_params.get("search_type")
        self.device = device or self.config.default_params.get("device")
        self.location = location or self.config.default_params.get("location")

        if not self.config.api_key:
            raise EngineError(
                self.engine_code,
                f"MapleSERP API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

    def _build_params(self, query: str) -> dict[str, Any]:
        """Build MapleSERP query parameters."""
        params: dict[str, Any] = {
            "query": query,
            "engine": self.search_engine,
            "num": self._get_num_results(min_value=1),
        }
        if self.country:
            params["gl"] = self.country
        if self.language:
            params["hl"] = self.language
        if self.search_type:
            params["search_type"] = self.search_type
        if self.device:
            params["device"] = self.device
        if self.location:
            params["location"] = self.location
        if self.safe_search is not None:
            params["safe"] = "active" if self.safe_search else "off"
        if self.time_frame:
            params["time_period"] = self.time_frame
        return params

    def _convert_result(self, item: MapleSerpOrganicResult, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one MapleSERP organic result into the normalized result model."""
        return SearchResult(
            title=item.title,
            url=item.result_url,
            snippet=item.result_snippet,
            source=self.engine_code,
            rank=item.position or rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using MapleSERP."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self.base_url,
            method="GET",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.config.api_key or ''}",
            },
            params=self._build_params(query),
        )

        try:
            data = response.json()
            parsed = MapleSerpResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        raw_results = data.get("organic_results", []) if isinstance(data, dict) else []
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.organic_results, raw_results, strict=False), start=1)
        ]
        return self.limit_results(results)


async def mapleserp(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    engine: str | None = None,
    search_type: str | None = None,
) -> list[SearchResult]:
    """Search using MapleSERP's SERP API."""
    config = EngineConfig(api_key=api_key, enabled=True)
    search_engine = MapleSerpSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        engine=engine,
        search_type=search_type,
    )
    return await search_engine.search(query)
