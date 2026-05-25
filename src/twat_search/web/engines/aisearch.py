# this_file: src/twat_search/web/engines/aisearch.py
"""AI Search API web-summary engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import AISEARCH, DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult

ResponseType = Literal["text", "markdown"]


class AISearchContextMessage(BaseModel):
    """Conversation context item accepted by AI Search API."""

    role: Literal["user"] = "user"
    content: str


class AISearchResponse(BaseModel):
    """Documented AI Search API response shape."""

    answer: str
    response_type: str = Field(alias="response_type")
    sources: list[HttpUrl]
    response_time: float = Field(alias="response_time")


@register_engine
class AISearchEngine(SearchEngine):
    """Implementation of AI Search API's summarized web search endpoint."""

    engine_code = AISEARCH
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[AISEARCH]
    env_api_key_names: ClassVar[list[str]] = ["AISEARCH_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        response_type: ResponseType | None = None,
        context: list[dict[str, str] | AISearchContextMessage] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the AI Search API engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        self.base_url = "https://api.aisearchapi.io/v1/search"
        configured_response_type = self.config.default_params.get("response_type", "markdown")
        self.response_type: ResponseType = response_type or configured_response_type
        self.context = self._parse_context(
            context if context is not None else self.config.default_params.get("context", []),
        )

    def _parse_context(
        self,
        context: list[dict[str, str] | AISearchContextMessage] | Any,
    ) -> list[AISearchContextMessage]:
        """Parse user-provided context messages into the documented shape."""
        if context is None:
            return []
        if not isinstance(context, list):
            msg = "AISearch context must be a list of message objects"
            raise EngineError(self.engine_code, msg)
        try:
            return [
                item if isinstance(item, AISearchContextMessage) else AISearchContextMessage.model_validate(item)
                for item in context
            ]
        except ValidationError as exc:
            raise EngineError(self.engine_code, f"Invalid AISearch context: {exc}") from exc

    def _build_payload(self, query: str) -> dict[str, Any]:
        """Build the documented AI Search API request payload."""
        payload: dict[str, Any] = {
            "prompt": query,
            "response_type": self.response_type,
        }
        if self.context:
            payload["context"] = [message.model_dump() for message in self.context]
        return payload

    def _convert_results(self, parsed: AISearchResponse, raw: dict[str, Any]) -> list[SearchResult]:
        """Convert source-backed AISearch answer data to normalized results."""
        snippet = textwrap.shorten(parsed.answer.strip(), width=500, placeholder="...")
        return [
            SearchResult(
                title=f"AI Search API answer source {rank}",
                url=source_url,
                snippet=snippet,
                source=self.engine_code,
                rank=rank,
                raw={**raw, "source_url": str(source_url)},
            )
            for rank, source_url in enumerate(parsed.sources, start=1)
        ]

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a summarized web search using AI Search API."""
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
            parsed = AISearchResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        return self.limit_results(self._convert_results(parsed, data))


async def aisearch(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    response_type: ResponseType | None = None,
    context: list[dict[str, str] | AISearchContextMessage] | None = None,
) -> list[SearchResult]:
    """Search using AI Search API."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = AISearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        response_type=response_type,
        context=context,
    )
    return await engine.search(query)
