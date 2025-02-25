# this_file: src/twat_search/web/engines/brave.py

"""
Brave Search engine implementation.

This module implements the Brave Search API integration.
"""

import httpx
from typing import Any
from pydantic import BaseModel, ValidationError, HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class BraveResult(BaseModel):
    """
    Pydantic model for a single Brave search result.

    This model is used to validate the response from the Brave API.
    """

    title: str
    url: HttpUrl
    description: str


class BraveResponse(BaseModel):
    """
    Pydantic model for the entire Brave API response.

    This is a simplified model that only captures the essentials.
    """

    web: dict[str, Any]


@register_engine
class BraveSearchEngine(SearchEngine):
    """Implementation of the Brave Search API."""

    name = "brave"

    def __init__(self, config: EngineConfig, count: int | None = None) -> None:
        """
        Initialize the Brave search engine.

        Args:
            config: Configuration for this search engine
            count: Number of results to return (overrides config)

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

        # Use provided count if available, otherwise, use default from config
        self.count = count or self.config.default_params.get("count", 10)

        if not self.config.api_key:
            raise EngineError(
                self.name,
                "Brave API key is required. Set it in the config or via the BRAVE_API_KEY env var.",
            )

        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.config.api_key,
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Brave Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params = {"q": query, "count": self.count}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                brave_response = BraveResponse(**data)

                results = []
                # Ensure web and results exist
                if brave_response.web and brave_response.web.get("results"):
                    for result in brave_response.web["results"]:
                        try:
                            # Validate and convert to BraveResult
                            brave_result = BraveResult(**result)

                            # Convert to common SearchResult format
                            results.append(
                                SearchResult(
                                    title=brave_result.title,
                                    url=str(brave_result.url),
                                    snippet=brave_result.description,
                                    source=self.name,
                                    raw=result,  # Include raw result for debugging
                                )
                            )
                        except ValidationError:
                            # Log the specific validation error and skip this result
                            continue

                return results

            except httpx.RequestError as exc:
                raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
            except httpx.HTTPStatusError as exc:
                raise EngineError(
                    self.name,
                    f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
                ) from exc
            except ValidationError as exc:
                raise EngineError(self.name, f"Response parsing error: {exc}") from exc
