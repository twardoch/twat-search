# this_file: src/twat_search/web/engines/apify.py
"""Apify actor-backed search engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar
from urllib.parse import quote

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import APIFY, DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class ApifyOrganicResult(BaseModel):
    """Organic result shape used by Google Search Scraper actors."""

    title: str = ""
    url: HttpUrl | None = None
    link: HttpUrl | None = None
    displayed_url: str | None = Field(default=None, alias="displayedUrl")
    description: str | None = None
    snippet: str | None = None

    @property
    def result_url(self) -> HttpUrl | None:
        """Return whichever URL field this actor output used."""
        return self.url or self.link


@register_engine
class ApifySearchEngine(SearchEngine):
    """Run an Apify search actor synchronously and normalize dataset items."""

    engine_code = APIFY
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[APIFY]
    env_api_key_names: ClassVar[list[str]] = ["APIFY_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        actor_id: str | None = None,
        country_code: str | None = None,
        language_code: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Apify actor-backed search engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.actor_id = actor_id or self.config.default_params.get("actor_id", "apify/google-search-scraper")
        self.country_code = country_code or country or self.config.default_params.get("country_code")
        self.language_code = language_code or language or self.config.default_params.get("language_code")

    def _build_url(self) -> str:
        """Build Apify run-sync-get-dataset-items URL for the configured actor."""
        actor_id = self.actor_id.replace("/", "~")
        return f"https://api.apify.com/v2/acts/{quote(actor_id, safe='~')}/run-sync-get-dataset-items"

    def _build_payload(self, query: str) -> dict[str, Any]:
        """Build conservative Google Search Scraper actor input."""
        payload: dict[str, Any] = {
            "queries": query,
            "maxPagesPerQuery": 1,
            "resultsPerPage": min(max(self._get_num_results(min_value=1), 1), 10),
        }
        if self.country_code:
            payload["countryCode"] = self.country_code
        if self.language_code:
            payload["languageCode"] = self.language_code
        if self.time_frame:
            payload["timeRange"] = self.time_frame
        return payload

    def _extract_organic_items(self, data: Any) -> list[tuple[ApifyOrganicResult, dict[str, Any]]]:
        """Extract organic-result candidates from Apify dataset items."""
        if not isinstance(data, list):
            msg = f"Unexpected Apify response type: {type(data).__name__}"
            raise ValueError(msg)

        extracted: list[tuple[ApifyOrganicResult, dict[str, Any]]] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            candidates = item.get("organicResults") or item.get("organic_results") or item.get("results")
            if isinstance(candidates, list):
                extracted.extend(
                    (ApifyOrganicResult.model_validate(candidate), candidate)
                    for candidate in candidates
                    if isinstance(candidate, dict)
                )
                continue
            if item.get("url") or item.get("link"):
                extracted.append((ApifyOrganicResult.model_validate(item), item))
        return extracted

    def _convert_result(self, item: ApifyOrganicResult, rank: int, raw: dict[str, Any]) -> SearchResult | None:
        """Convert one Apify organic result to the normalized result model."""
        url = item.result_url
        if url is None:
            return None
        snippet = item.description or item.snippet or ""
        snippet = textwrap.shorten(snippet.strip(), width=500, placeholder="...")
        return SearchResult(
            title=item.title,
            url=url,
            snippet=snippet,
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a search by running the configured Apify actor."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self._build_url(),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key or ''}",
            },
            json_data=self._build_payload(query),
            timeout=self.config.default_params.get("timeout", 300),
        )

        try:
            data = response.json()
            items = self._extract_organic_items(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        results: list[SearchResult] = []
        for item, raw in items:
            result = self._convert_result(item, len(results) + 1, raw)
            if result is not None:
                results.append(result)
        return self.limit_results(results)


async def apify(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    actor_id: str | None = None,
) -> list[SearchResult]:
    """Search using an Apify actor."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = ApifySearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        actor_id=actor_id,
    )
    return await engine.search(query)
