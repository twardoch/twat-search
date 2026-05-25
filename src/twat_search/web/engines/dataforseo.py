# this_file: src/twat_search/web/engines/dataforseo.py
"""DataForSEO live organic SERP API engine."""

from __future__ import annotations

import base64
from typing import Any, ClassVar

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DATAFORSEO, DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class DataForSeoItem(BaseModel):
    """SERP item returned by DataForSEO."""

    type: str = ""
    title: str = ""
    url: HttpUrl | None = None
    description: str = ""
    rank_group: int | None = None
    rank_absolute: int | None = None


class DataForSeoTaskResult(BaseModel):
    """Task result wrapper returned by DataForSEO."""

    items: list[DataForSeoItem] = Field(default_factory=list)


class DataForSeoTask(BaseModel):
    """Task wrapper returned by DataForSEO."""

    status_code: int | None = None
    status_message: str | None = None
    result: list[DataForSeoTaskResult] = Field(default_factory=list)


class DataForSeoResponse(BaseModel):
    """Top-level DataForSEO live response."""

    status_code: int | None = None
    status_message: str | None = None
    tasks: list[DataForSeoTask] = Field(default_factory=list)


@register_engine
class DataForSeoSearchEngine(SearchEngine):
    """Implementation of DataForSEO Live SERP Advanced API."""

    engine_code = DATAFORSEO
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[DATAFORSEO]
    env_api_key_names: ClassVar[list[str]] = ["DATAFORSEO_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        search_engine: str | None = None,
        location_code: int | None = None,
        language_code: str | None = None,
        device: str | None = None,
        os_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the DataForSEO engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.search_engine = search_engine or self.config.default_params.get("search_engine", "google")
        self.base_url = f"https://api.dataforseo.com/v3/serp/{self.search_engine}/organic/live/advanced"
        self.location_code = location_code or self.config.default_params.get("location_code")
        self.language_code = language_code or language or self.config.default_params.get("language_code")
        self.device = device or self.config.default_params.get("device")
        self.os_name = os_name or self.config.default_params.get("os")

    def _auth_header(self) -> str:
        """Return DataForSEO Basic auth header from configured credentials."""
        token = base64.b64encode((self.config.api_key or "").encode("utf-8")).decode("ascii")
        return f"Basic {token}"

    def _build_payload(self, query: str) -> list[dict[str, Any]]:
        """Build DataForSEO's one-task live SERP payload."""
        task: dict[str, Any] = {
            "keyword": query,
            "depth": self._get_num_results(min_value=1),
        }
        if self.location_code:
            task["location_code"] = self.location_code
        if self.language_code:
            task["language_code"] = self.language_code
        if self.device:
            task["device"] = self.device
        if self.os_name:
            task["os"] = self.os_name
        return [task]

    def _convert_item(self, item: DataForSeoItem, raw: dict[str, Any]) -> SearchResult | None:
        """Convert one organic DataForSEO item into the normalized result model."""
        if item.type != "organic" or item.url is None:
            return None
        return SearchResult(
            title=item.title,
            url=item.url,
            snippet=item.description,
            source=self.engine_code,
            rank=item.rank_absolute or item.rank_group,
            raw=raw,
        )

    def _extract_results(self, data: dict[str, Any]) -> list[SearchResult]:
        """Extract normalized organic results from a DataForSEO response."""
        parsed = DataForSeoResponse.model_validate(data)
        results: list[SearchResult] = []
        raw_tasks = data.get("tasks", [])
        for task_index, task in enumerate(parsed.tasks):
            if task.status_code is not None and task.status_code >= 40000:
                raise EngineError(self.engine_code, task.status_message or f"Task failed with {task.status_code}")
            raw_task = raw_tasks[task_index] if task_index < len(raw_tasks) else {}
            raw_results = raw_task.get("result", [])
            for result_index, result in enumerate(task.result):
                raw_result = raw_results[result_index] if result_index < len(raw_results) else {}
                raw_items = raw_result.get("items", [])
                for item_index, item in enumerate(result.items):
                    raw_item = raw_items[item_index] if item_index < len(raw_items) else {}
                    converted = self._convert_item(item, raw_item)
                    if converted:
                        results.append(converted)
        return self.limit_results(results)

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a live organic SERP search through DataForSEO."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self.base_url,
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": self._auth_header(),
            },
            json_data=self._build_payload(query),
        )

        try:
            return self._extract_results(response.json())
        except ValidationError as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc


async def dataforseo(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    search_engine: str | None = None,
    location_code: int | None = None,
    language_code: str | None = None,
) -> list[SearchResult]:
    """Search using DataForSEO Live SERP Advanced API."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = DataForSeoSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        search_engine=search_engine,
        location_code=location_code,
        language_code=language_code,
    )
    return await engine.search(query)
