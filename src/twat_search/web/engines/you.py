# this_file: src/twat_search/web/engines/youcom.py

"""
You.com Search engine implementation.

This module implements the You.com Search API integration.
"""

import httpx
from pydantic import BaseModel, ValidationError

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class YoucomResult(BaseModel):
    """
    Pydantic model for a single You.com search result.

    This model is used to validate results from the You.com API.
    """

    title: str
    url: str  # Use str instead of HttpUrl for flexibility
    snippet: str


class YoucomResponse(BaseModel):
    """
    Pydantic model for the You.com API response.

    This model focuses on the results array.
    """

    results: list[YoucomResult] = []  # Default to empty list if not found


@register_engine
class YoucomSearchEngine(SearchEngine):
    """Implementation of the You.com Search API."""

    name = "youcom"

    def __init__(self, config: EngineConfig, count: int | None = None) -> None:
        """
        Initialize the You.com search engine.

        Args:
            config: Configuration for this search engine
            count: Number of results to return (overrides config)

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.ydc-index.io/search"

        # Use provided count if available, otherwise, use default from config
        self.count = count or self.config.default_params.get("count", 10)

        if not self.config.api_key:
            raise EngineError(
                self.name,
                "You.com API key is required. Set it in config or the YOUCOM_API_KEY env var.",
            )

        self.headers = {"X-API-Key": self.config.api_key}

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the You.com Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params = {"query": query, "limit": self.count}  # Limit is for you.com

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()

                data = response.json()
                youcom_response = YoucomResponse(**data)  # Use Pydantic model

                results = []
                # Iterate safely with the Pydantic model
                for result in youcom_response.results:
                    try:
                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=result.title,
                                url=result.url,  # URLs are already strings
                                snippet=result.snippet,
                                source=self.name,
                                raw=result.model_dump(),  # Include raw result
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
