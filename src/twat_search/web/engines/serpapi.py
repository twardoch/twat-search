# this_file: src/twat_search/web/engines/google.py

"""
Google Search engine implementation (via SerpAPI).

This module implements the Google Search API integration using SerpAPI.
"""

import httpx
from pydantic import BaseModel, HttpUrl, ValidationError

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class GoogleResult(BaseModel):
    """
    Pydantic model for a single Google search result.

    This model is used to validate results from the SerpAPI response.
    """

    title: str
    link: HttpUrl
    snippet: str


class GoogleResponse(BaseModel):
    """
    Pydantic model for the entire Google API response.

    This is a simplified model that focuses on organic results.
    """

    organic_results: list[GoogleResult]


@register_engine
class GoogleSearchEngine(SearchEngine):
    """Implementation of the Google Search API via SerpAPI."""

    name = "google"

    def __init__(self, config: EngineConfig, count: int | None = None) -> None:
        """
        Initialize the Google search engine.

        Args:
            config: Configuration for this search engine
            count: Number of results to return (overrides config)

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://serpapi.com/search"

        # Use provided count if available, otherwise, use default from config
        self.count = count or self.config.default_params.get("count", 10)

        if not self.config.api_key:
            raise EngineError(
                self.name,
                "Google (SerpAPI) API key is required. Set it in config or via the SERPAPI_API_KEY env var.",
            )

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Google Search API via SerpAPI.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params = {
            "q": query,
            "api_key": self.config.api_key,
            "num": self.count,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                google_response = GoogleResponse(**data)  # Parse entire response

                results = []
                for result in google_response.organic_results:
                    try:
                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=result.title,
                                url=str(result.link),  # Convert HttpUrl to string
                                snippet=result.snippet,
                                source=self.name,
                                raw=result.model_dump(),  # Include the raw result
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
