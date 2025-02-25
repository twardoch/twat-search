# this_file: src/twat_search/web/engines/tavily.py

"""
Tavily Search engine implementation.

This module implements the Tavily Search API integration.
"""

import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class TavilySearchResult(BaseModel):
    """
    Pydantic model for a single Tavily search result.

    This model is used to validate results from the Tavily API.
    """

    title: str
    url: str  # Use str instead of HttpUrl as Tavily might return non-standard URLs
    content: str  # Tavily returns content, not just a snippet
    score: float | None = None  # Relevance score, if available


class TavilySearchResponse(BaseModel):
    """
    Pydantic model for the entire Tavily API response.

    This model focuses on the results array.
    """

    results: list[TavilySearchResult]
    query: str
    search_id: str | None = None


@register_engine
class TavilySearchEngine(SearchEngine):
    """Implementation of the Tavily Search API."""

    name = "tavily"
    env_api_key_names: ClassVar[list[str]] = ["TAVILY_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        max_results: int | None = None,
        search_depth: str | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        search_type: str | None = None,
    ) -> None:
        """
        Initialize the Tavily search engine.

        Args:
            config: Configuration for this search engine
            max_results: Maximum number of results to return (overrides config)
            search_depth: 'basic' for faster results or 'comprehensive' for more thorough search
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            search_type: Type of search ('search' or 'news') - defaults to 'search'

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.tavily.com/search"

        # Use provided max_results if available, otherwise use default from config
        self.max_results = max_results or self.config.default_params.get(
            "max_results", 5
        )

        # Set search parameters
        self.search_depth = search_depth or self.config.default_params.get(
            "search_depth", "basic"
        )
        self.include_domains = include_domains or self.config.default_params.get(
            "include_domains", []
        )
        self.exclude_domains = exclude_domains or self.config.default_params.get(
            "exclude_domains", []
        )
        self.search_type = search_type or self.config.default_params.get(
            "search_type", "search"
        )

        if not self.config.api_key:
            raise EngineError(
                self.name,
                "Tavily API key is required. Set it in the config or via the TAVILY_API_KEY env var.",
            )

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Tavily Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        headers = {"Content-Type": "application/json"}
        payload: dict[str, Any] = {
            "api_key": self.config.api_key,
            "query": query,
            "max_results": self.max_results,
            "search_depth": self.search_depth,
            "search_type": self.search_type,
        }

        # Only add these if they have values
        if self.include_domains:
            payload["include_domains"] = self.include_domains
        if self.exclude_domains:
            payload["exclude_domains"] = self.exclude_domains

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url, headers=headers, json=payload, timeout=10
                )
                response.raise_for_status()

                data = response.json()
                tavily_response = TavilySearchResponse(**data)

                results = []
                for result in tavily_response.results:
                    try:
                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=result.title,
                                url=result.url,  # URLs are already strings
                                snippet=result.content[:500],  # Limit snippet length
                                source=self.name,
                                raw=result.model_dump(),
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
