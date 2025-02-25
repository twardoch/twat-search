# this_file: src/twat_search/web/engines/serpapi.py

"""
SerpApi Google search engine implementation.

This module implements the SerpApi Google Search API integration.
"""

import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class SerpApiResult(BaseModel):
    """
    Pydantic model for a single SerpApi Google search result.

    This model is used to validate the response from the SerpApi API.
    """

    title: str
    link: HttpUrl  # SerpApi uses 'link' for URLs
    snippet: str
    position: int | None = None


class SerpApiResponse(BaseModel):
    """
    Pydantic model for the entire SerpApi API response.

    This captures the essential parts of the response.
    """

    organic_results: list[SerpApiResult]
    search_metadata: dict[str, Any]
    search_parameters: dict[str, Any]


@register_engine
class SerpApiSearchEngine(SearchEngine):
    """Implementation of the SerpApi Google Search API."""

    name = "serpapi"
    env_api_key_names: ClassVar[list[str]] = ["SERPAPI_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num: int | None = None,
        google_domain: str | None = None,
        gl: str | None = None,  # Country for Google search
        hl: str | None = None,  # Language for Google search
        safe: str | None = None,  # Safe search setting
        time_period: str | None = None,  # Time period for search
    ) -> None:
        """
        Initialize the SerpApi Google search engine.

        Args:
            config: Configuration for this search engine
            num: Number of results to return (overrides config)
            google_domain: Google domain to use (e.g., google.com, google.co.uk)
            gl: Country for Google search (e.g., us, uk)
            hl: Language for Google search (e.g., en, fr)
            safe: Safe search setting (active or off)
            time_period: Time period for search (e.g., last_day, last_week, last_month, last_year)

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://serpapi.com/search"

        # Use provided num if available, otherwise, use default from config
        self.num = num or self.config.default_params.get("num", 10)

        # Additional parameters
        self.google_domain = google_domain or self.config.default_params.get(
            "google_domain", "google.com"
        )
        self.gl = gl or self.config.default_params.get("gl", None)
        self.hl = hl or self.config.default_params.get("hl", None)
        self.safe = safe or self.config.default_params.get("safe", None)
        self.time_period = time_period or self.config.default_params.get(
            "time_period", None
        )

        if not self.config.api_key:
            raise EngineError(
                self.name,
                "SerpApi API key is required. Set it in the config or via the SERPAPI_API_KEY env var.",
            )

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the SerpApi Google Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params: dict[str, Any] = {
            "q": query,
            "api_key": self.config.api_key,
            "engine": "google",
            "num": self.num,
            "google_domain": self.google_domain,
        }

        # Add optional parameters if they have values
        if self.gl:
            params["gl"] = self.gl
        if self.hl:
            params["hl"] = self.hl
        if self.safe:
            params["safe"] = self.safe
        if self.time_period:
            params["time_period"] = self.time_period

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url,
                    params=params,
                    timeout=30,  # SerpApi can be slower
                )
                response.raise_for_status()

                data = response.json()

                # Check if organic_results exists in the response
                if "organic_results" not in data:
                    return []  # No results found

                serpapi_response = SerpApiResponse(**data)

                results = []
                for result in serpapi_response.organic_results:
                    try:
                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=result.title,
                                url=result.link,  # SerpApi uses 'link' instead of 'url'
                                snippet=result.snippet,
                                source=self.name,
                                rank=result.position,  # Use position as rank if available
                                raw=result.model_dump(),  # Include raw result for debugging
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


async def serpapi(
    query: str,
    api_key: str | None = None,
    num: int = 10,
    google_domain: str = "google.com",
    gl: str | None = None,
    hl: str | None = None,
    safe: str | None = None,
    time_period: str | None = None,
) -> list[SearchResult]:
    """
    Perform a web search using the SerpApi Google Search API.

    This function provides a simple interface to the SerpApi Google Search API,
    allowing users to search the web and get structured results from Google.

    If no API key is provided, the function will attempt to find one in the environment
    variables using the names defined in SerpApiSearchEngine.env_api_key_names
    (typically "SERPAPI_API_KEY").

    Args:
        query: The search query string
        api_key: Optional SerpApi API key. If not provided, will look for it in environment variables
        num: Number of results to return (default: 10)
        google_domain: Google domain to use (default: "google.com")
        gl: Country for Google search (e.g., "us", "uk", "fr")
        hl: Language for Google search (e.g., "en", "fr", "de")
        safe: Safe search setting ("active" or "off")
        time_period: Time period for search ("last_day", "last_week", "last_month", "last_year")

    Returns:
        A list of SearchResult objects containing the search results with:
        - title: The title of the search result
        - url: The URL of the search result
        - snippet: A brief description or excerpt
        - source: The source engine ("serpapi")
        - rank: The ranking position of the result (if available)
        - raw: The raw result data from the API

    Raises:
        EngineError: If the search fails or API key is missing

    Examples:
        # Using API key from environment variable
        >>> results = await serpapi("Python programming")
        >>> for result in results:
        ...     print(f"{result.title}: {result.url}")

        # Explicitly providing API key
        >>> results = await serpapi("machine learning", api_key="your-api-key")

        # With advanced parameters
        >>> results = await serpapi(
        ...     "python programming",
        ...     num=5,
        ...     gl="us",
        ...     hl="en",
        ...     time_period="last_month"
        ... )
    """
    # Try to get API key from environment if not provided
    actual_api_key = api_key
    if not actual_api_key:
        import os

        # Check environment variables using the engine's env_api_key_names
        for env_var in SerpApiSearchEngine.env_api_key_names:
            if env_var in os.environ:
                actual_api_key = os.environ[env_var]
                break

    # Create a simple config for this request
    config = EngineConfig(
        api_key=actual_api_key,
        enabled=True,
        default_params={
            "num": num,
            "google_domain": google_domain,
            "gl": gl,
            "hl": hl,
            "safe": safe,
            "time_period": time_period,
        },
    )

    # Create the engine instance
    engine = SerpApiSearchEngine(
        config=config,
        num=num,
        google_domain=google_domain,
        gl=gl,
        hl=hl,
        safe=safe,
        time_period=time_period,
    )

    # Perform the search
    return await engine.search(query)
