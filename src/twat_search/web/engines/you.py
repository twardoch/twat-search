# this_file: src/twat_search/web/engines/you.py

"""
You.com Search engine implementation.

This module implements the You.com Search API integration.
"""

import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl, Field

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class YouSearchHit(BaseModel):
    """
    Pydantic model for a single You.com search hit.

    This model is used to validate the response from the You.com API.
    """

    title: str
    url: HttpUrl
    snippet: str = Field(alias="description")


class YouSearchResponse(BaseModel):
    """
    Pydantic model for the entire You.com API response.

    This captures the essential parts of the response.
    """

    hits: list[YouSearchHit]
    search_id: str | None = Field(None, alias="searchId")


@register_engine
class YouSearchEngine(SearchEngine):
    """Implementation of the You.com Search API."""

    name = "you"
    env_api_key_names: ClassVar[list[str]] = [
        "YOUCOM_API_KEY",
        "YOUCOM_SEARCH_API_KEY",
        "YOU_API_KEY",
    ]

    def __init__(
        self,
        config: EngineConfig,
        num_web_results: int | None = None,
        country_code: str | None = None,
        safe_search: bool | None = None,
    ) -> None:
        """
        Initialize the You.com search engine.

        Args:
            config: Configuration for this search engine
            num_web_results: Number of results to return (overrides config)
            country_code: Country code for localization (ISO-3166 Alpha-2)
            safe_search: Whether to enable safe search

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.you.com/api/search"

        # Use provided count if available, otherwise, use default from config
        self.num_web_results = num_web_results or self.config.default_params.get(
            "num_web_results", 10
        )

        # Additional parameters
        self.country_code = country_code or self.config.default_params.get(
            "country_code", None
        )
        self.safe_search = safe_search or self.config.default_params.get(
            "safe_search", None
        )

        if not self.config.api_key:
            raise EngineError(
                self.name,
                "You.com API key is required. Set it in the config or via the YOU_API_KEY env var.",
            )

        self.headers = {
            "X-API-Key": self.config.api_key,
            "Accept": "application/json",
        }

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
        params: dict[str, Any] = {"q": query, "num_web_results": self.num_web_results}

        # Add optional parameters if they have values
        if self.country_code:
            params["country_code"] = self.country_code
        if self.safe_search is not None:  # Explicit check since it's a boolean
            params["safe_search"] = str(self.safe_search).lower()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                you_response = YouSearchResponse(**data)

                results = []
                for hit in you_response.hits:
                    try:
                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=hit.title,
                                url=hit.url,
                                snippet=hit.snippet,
                                source=self.name,
                                raw=hit.model_dump(
                                    by_alias=True
                                ),  # Include raw result for debugging
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


class YouNewsArticle(BaseModel):
    """
    Pydantic model for a single You.com news article.

    This model is used to validate the response from the You.com News API.
    """

    title: str
    url: HttpUrl
    snippet: str = Field(alias="description")
    source: str | None = None
    published_date: str | None = None


class YouNewsResponse(BaseModel):
    """
    Pydantic model for the entire You.com News API response.

    This captures the essential parts of the response.
    """

    articles: list[YouNewsArticle]
    search_id: str | None = Field(None, alias="searchId")


@register_engine
class YouNewsSearchEngine(SearchEngine):
    """Implementation of the You.com News Search API."""

    name = "you-news"
    env_api_key_names: ClassVar[list[str]] = ["YOU_API_KEY", "YOU_NEWS_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_news_results: int | None = None,
        country_code: str | None = None,
        safe_search: bool | None = None,
    ) -> None:
        """
        Initialize the You.com News search engine.

        Args:
            config: Configuration for this search engine
            num_news_results: Number of results to return (overrides config)
            country_code: Country code for localization (ISO-3166 Alpha-2)
            safe_search: Whether to enable safe search

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.you.com/api/news"

        # Use provided count if available, otherwise, use default from config
        self.num_news_results = num_news_results or self.config.default_params.get(
            "num_news_results", 10
        )

        # Additional parameters
        self.country_code = country_code or self.config.default_params.get(
            "country_code", None
        )
        self.safe_search = safe_search or self.config.default_params.get(
            "safe_search", None
        )

        if not self.config.api_key:
            raise EngineError(
                self.name,
                "You.com API key is required. Set it in the config or via the YOU_API_KEY env var.",
            )

        self.headers = {
            "X-API-Key": self.config.api_key,
            "Accept": "application/json",
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a news search using the You.com News API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params: dict[str, Any] = {"q": query, "num_news_results": self.num_news_results}

        # Add optional parameters if they have values
        if self.country_code:
            params["country_code"] = self.country_code
        if self.safe_search is not None:  # Explicit check since it's a boolean
            params["safe_search"] = str(self.safe_search).lower()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                you_response = YouNewsResponse(**data)

                results = []
                for article in you_response.articles:
                    try:
                        # Build a richer snippet if we have source and date
                        snippet = article.snippet
                        if article.source and article.published_date:
                            snippet = f"{snippet} - {article.source} ({article.published_date})"
                        elif article.source:
                            snippet = f"{snippet} - {article.source}"

                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=article.title,
                                url=article.url,
                                snippet=snippet,
                                source=self.name,
                                raw=article.model_dump(
                                    by_alias=True
                                ),  # Include raw result for debugging
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


# For backward compatibility
YoucomSearchEngine = YouSearchEngine


async def you(
    query: str,
    api_key: str | None = None,
    num_web_results: int = 10,
    country_code: str | None = None,
    safe_search: bool | None = None,
) -> list[SearchResult]:
    """
    Perform a web search using the You.com Search API.

    This function provides a simple interface to the You.com Search API, allowing
    users to search the web and get structured results.

    If no API key is provided, the function will attempt to find one in the environment
    variables using the names defined in YouSearchEngine.env_api_key_names
    (typically "YOUCOM_API_KEY", "YOUCOM_SEARCH_API_KEY", or "YOU_API_KEY").

    Args:
        query: The search query string
        api_key: Optional You.com API key. If not provided, will look for it in environment variables
        num_web_results: Number of results to return (default: 10)
        country_code: Country code for localization (ISO-3166 Alpha-2)
        safe_search: Whether to enable safe search

    Returns:
        A list of SearchResult objects containing the search results with:
        - title: The title of the search result
        - url: The URL of the search result
        - snippet: A brief description or excerpt
        - source: The source engine ("you")
        - raw: The raw result data from the API

    Raises:
        EngineError: If the search fails or API key is missing

    Examples:
        # Using API key from environment variable
        >>> results = await you("Python programming")
        >>> for result in results:
        ...     print(f"{result.title}: {result.url}")

        # Explicitly providing API key
        >>> results = await you("machine learning", api_key="your-api-key")

        # With advanced parameters
        >>> results = await you(
        ...     "python programming",
        ...     num_web_results=5,
        ...     country_code="US",
        ...     safe_search=True
        ... )
    """
    # Try to get API key from environment if not provided
    actual_api_key = api_key
    if not actual_api_key:
        import os

        # Check environment variables using the engine's env_api_key_names
        for env_var in YouSearchEngine.env_api_key_names:
            if env_var in os.environ:
                actual_api_key = os.environ[env_var]
                break

    # Create a simple config for this request
    config = EngineConfig(
        api_key=actual_api_key,
        enabled=True,
        default_params={
            "num_web_results": num_web_results,
            "country_code": country_code,
            "safe_search": safe_search,
        },
    )

    # Create the engine instance
    engine = YouSearchEngine(
        config=config,
        num_web_results=num_web_results,
        country_code=country_code,
        safe_search=safe_search,
    )

    # Perform the search
    return await engine.search(query)


async def you_news(
    query: str,
    api_key: str | None = None,
    num_news_results: int = 10,
    country_code: str | None = None,
    safe_search: bool | None = None,
) -> list[SearchResult]:
    """
    Perform a news search using the You.com News API.

    This function provides a simple interface to the You.com News API, allowing
    users to search for news articles and get structured results.

    If no API key is provided, the function will attempt to find one in the environment
    variables using the names defined in YouNewsSearchEngine.env_api_key_names
    (typically "YOU_API_KEY" or "YOU_NEWS_API_KEY").

    Args:
        query: The search query string
        api_key: Optional You.com API key. If not provided, will look for it in environment variables
        num_news_results: Number of news results to return (default: 10)
        country_code: Country code for localization (ISO-3166 Alpha-2)
        safe_search: Whether to enable safe search

    Returns:
        A list of SearchResult objects containing the news search results with:
        - title: The title of the news article
        - url: The URL of the news article
        - snippet: A brief description or excerpt, may include publisher and publication time
        - source: The source engine ("you-news")
        - raw: The raw result data from the API

    Raises:
        EngineError: If the search fails or API key is missing

    Examples:
        # Using API key from environment variable
        >>> results = await you_news("Climate change")
        >>> for result in results:
        ...     print(f"{result.title}: {result.url}")

        # Explicitly providing API key
        >>> results = await you_news("politics", api_key="your-api-key")

        # With advanced parameters
        >>> results = await you_news(
        ...     "technology trends",
        ...     num_news_results=5,
        ...     country_code="US",
        ...     safe_search=True
        ... )
    """
    # Try to get API key from environment if not provided
    actual_api_key = api_key
    if not actual_api_key:
        import os

        # Check environment variables using the engine's env_api_key_names
        for env_var in YouNewsSearchEngine.env_api_key_names:
            if env_var in os.environ:
                actual_api_key = os.environ[env_var]
                break

    # Create a simple config for this request
    config = EngineConfig(
        api_key=actual_api_key,
        enabled=True,
        default_params={
            "num_news_results": num_news_results,
            "country_code": country_code,
            "safe_search": safe_search,
        },
    )

    # Create the engine instance
    engine = YouNewsSearchEngine(
        config=config,
        num_news_results=num_news_results,
        country_code=country_code,
        safe_search=safe_search,
    )

    # Perform the search
    return await engine.search(query)


# Alias for backward compatibility
youcom = you
