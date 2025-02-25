# this_file: src/twat_search/web/engines/brave.py

"""
Brave Search engine implementation.

This module implements the Brave Search API integration.
"""

import httpx
from typing import Any, ClassVar
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
    env_api_key_names: ClassVar[list[str]] = ["BRAVE_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        count: int | None = None,
        country: str | None = None,
        search_lang: str | None = None,
        ui_lang: str | None = None,
        safe_search: str | None = None,
        freshness: str | None = None,
    ) -> None:
        """
        Initialize the Brave search engine.

        Args:
            config: Configuration for this search engine
            count: Number of results to return (overrides config)
            country: Country code for search localization
            search_lang: Language for search results
            ui_lang: Language for user interface
            safe_search: Safe search setting ('strict', 'moderate', 'off')
            freshness: Time range for results ('past_day', 'past_week', 'past_month', 'past_year')

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

        # Use provided count if available, otherwise, use default from config
        self.count = count or self.config.default_params.get("count", 10)

        # Additional parameters
        self.country = country or self.config.default_params.get("country", None)
        self.search_lang = search_lang or self.config.default_params.get(
            "search_lang", None
        )
        self.ui_lang = ui_lang or self.config.default_params.get("ui_lang", None)
        self.safe_search = safe_search or self.config.default_params.get(
            "safe_search", None
        )
        self.freshness = freshness or self.config.default_params.get("freshness", None)

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
        params: dict[str, Any] = {"q": query, "count": self.count}

        # Add optional parameters if they have values
        if self.country:
            params["country"] = self.country
        if self.search_lang:
            params["search_lang"] = self.search_lang
        if self.ui_lang:
            params["ui_lang"] = self.ui_lang
        if self.safe_search:
            params["safe_search"] = self.safe_search
        if self.freshness:
            params["freshness"] = self.freshness

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
                            # The URL is already a validated HttpUrl object from Pydantic
                            results.append(
                                SearchResult(
                                    title=brave_result.title,
                                    url=brave_result.url,
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


class BraveNewsResult(BaseModel):
    """
    Pydantic model for a single Brave News search result.

    This model is used to validate the response from the Brave News API.
    """

    title: str
    url: HttpUrl
    description: str
    published_time: str | None = None
    publisher: str | None = None


class BraveNewsResponse(BaseModel):
    """
    Pydantic model for the entire Brave News API response.

    This is a simplified model that only captures the essentials.
    """

    news: dict[str, Any]


@register_engine
class BraveNewsSearchEngine(SearchEngine):
    """Implementation of the Brave News Search API."""

    name = "brave-news"
    env_api_key_names: ClassVar[list[str]] = ["BRAVE_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        count: int | None = None,
        country: str | None = None,
        search_lang: str | None = None,
        ui_lang: str | None = None,
        freshness: str | None = None,
    ) -> None:
        """
        Initialize the Brave News search engine.

        Args:
            config: Configuration for this search engine
            count: Number of results to return (overrides config)
            country: Country code for search localization
            search_lang: Language for search results
            ui_lang: Language for user interface
            freshness: Time range for results ('past_hour', 'past_day', 'past_week', 'past_month')

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.search.brave.com/res/v1/news/search"

        # Use provided count if available, otherwise, use default from config
        self.count = count or self.config.default_params.get("count", 10)

        # Additional parameters
        self.country = country or self.config.default_params.get("country", None)
        self.search_lang = search_lang or self.config.default_params.get(
            "search_lang", None
        )
        self.ui_lang = ui_lang or self.config.default_params.get("ui_lang", None)
        self.freshness = freshness or self.config.default_params.get("freshness", None)

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
        Perform a news search using the Brave News Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params: dict[str, Any] = {"q": query, "count": self.count}

        # Add optional parameters if they have values
        if self.country:
            params["country"] = self.country
        if self.search_lang:
            params["search_lang"] = self.search_lang
        if self.ui_lang:
            params["ui_lang"] = self.ui_lang
        if self.freshness:
            params["freshness"] = self.freshness

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                brave_response = BraveNewsResponse(**data)

                results = []
                # Ensure news and results exist
                if brave_response.news and brave_response.news.get("results"):
                    for result in brave_response.news["results"]:
                        try:
                            # Validate and convert to BraveNewsResult
                            brave_result = BraveNewsResult(**result)

                            # Build a snippet that includes publication info if available
                            snippet = brave_result.description
                            if brave_result.publisher and brave_result.published_time:
                                snippet = f"{snippet} - {brave_result.publisher} ({brave_result.published_time})"
                            elif brave_result.publisher:
                                snippet = f"{snippet} - {brave_result.publisher}"

                            # Convert to common SearchResult format
                            # The URL is already a validated HttpUrl object from Pydantic
                            results.append(
                                SearchResult(
                                    title=brave_result.title,
                                    url=brave_result.url,
                                    snippet=snippet,
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


async def brave(
    query: str,
    api_key: str | None = None,
    count: int = 10,
    country: str | None = None,
    search_lang: str | None = None,
    ui_lang: str | None = None,
    safe_search: str | None = None,
    freshness: str | None = None,
) -> list[SearchResult]:
    """
    Perform a web search using Brave Search API.

    This function provides a simple interface to the Brave Search API, allowing
    users to search the web and get structured results. It returns web search
    results that match the provided query.

    If no API key is provided, the function will attempt to find one in the environment
    variables using the names defined in BraveSearchEngine.env_api_key_names
    (typically "BRAVE_API_KEY").

    Args:
        query: The search query string
        api_key: Optional Brave Search API key. If not provided, will look for it in environment variables
        count: Number of results to return (default: 10)
        country: Country code for search localization (ISO 3166-1 alpha-2)
            Example: 'US', 'GB', 'DE', etc.
        search_lang: Language for search results (ISO 639-1)
            Example: 'en', 'fr', 'de', etc.
        ui_lang: Language for user interface (ISO 639-1)
            Example: 'en', 'fr', 'de', etc.
        safe_search: Safe search setting ('strict', 'moderate', 'off')
        freshness: Time range for results ('past_day', 'past_week', 'past_month', 'past_year')

    Returns:
        A list of SearchResult objects containing the search results with:
        - title: The title of the search result
        - url: The URL of the search result
        - snippet: A brief description or excerpt
        - source: The source engine ("brave")
        - raw: The raw result data from the API

    Raises:
        EngineError: If the search fails or API key is missing

    Examples:
        # Using API key from environment variable
        >>> results = await brave("Python programming")
        >>> for result in results:
        ...     print(f"{result.title}: {result.url}")

        # Explicitly providing API key
        >>> results = await brave("machine learning", api_key="your-api-key")

        # With advanced parameters
        >>> results = await brave(
        ...     "machine learning",
        ...     count=5,
        ...     country="US",
        ...     search_lang="en",
        ...     freshness="past_week"
        ... )
    """
    # Try to get API key from environment if not provided
    actual_api_key = api_key
    if not actual_api_key:
        import os

        # Check environment variables using the engine's env_api_key_names
        for env_var in BraveSearchEngine.env_api_key_names:
            if env_var in os.environ:
                actual_api_key = os.environ[env_var]
                break

    # Create a simple config for this request
    config = EngineConfig(
        api_key=actual_api_key,
        enabled=True,
        default_params={
            "count": count,
            "country": country,
            "search_lang": search_lang,
            "ui_lang": ui_lang,
            "safe_search": safe_search,
            "freshness": freshness,
        },
    )

    # Create the engine instance
    engine = BraveSearchEngine(
        config=config,
        count=count,
        country=country,
        search_lang=search_lang,
        ui_lang=ui_lang,
        safe_search=safe_search,
        freshness=freshness,
    )

    # Perform the search
    return await engine.search(query)


async def brave_news(
    query: str,
    api_key: str | None = None,
    count: int = 10,
    country: str | None = None,
    search_lang: str | None = None,
    ui_lang: str | None = None,
    freshness: str | None = None,
) -> list[SearchResult]:
    """
    Perform a news search using Brave News Search API.

    This function provides a simple interface to the Brave News Search API, allowing
    users to search for news articles and get structured results. It returns news
    articles that match the provided query.

    If no API key is provided, the function will attempt to find one in the environment
    variables using the names defined in BraveNewsSearchEngine.env_api_key_names
    (typically "BRAVE_API_KEY" or "BRAVE_NEWS_API_KEY").

    Args:
        query: The search query string
        api_key: Optional Brave Search API key. If not provided, will look for it in environment variables
        count: Number of results to return (default: 10)
        country: Country code for search localization (ISO 3166-1 alpha-2)
            Example: 'US', 'GB', 'DE', etc.
        search_lang: Language for search results (ISO 639-1)
            Example: 'en', 'fr', 'de', etc.
        ui_lang: Language for user interface (ISO 639-1)
            Example: 'en', 'fr', 'de', etc.
        freshness: Time range for results ('past_hour', 'past_day', 'past_week', 'past_month')

    Returns:
        A list of SearchResult objects containing the news search results with:
        - title: The title of the news article
        - url: The URL of the news article
        - snippet: A brief description or excerpt, may include publisher and publication time
        - source: The source engine ("brave-news")
        - raw: The raw result data from the API

    Raises:
        EngineError: If the search fails or API key is missing

    Examples:
        # Using API key from environment variable
        >>> results = await brave_news("Climate change")
        >>> for result in results:
        ...     print(f"{result.title}: {result.url}")

        # Explicitly providing API key
        >>> results = await brave_news("politics", api_key="your-api-key")

        # With advanced parameters
        >>> results = await brave_news(
        ...     "politics",
        ...     count=5,
        ...     country="US",
        ...     freshness="past_day"
        ... )
    """
    # Try to get API key from environment if not provided
    actual_api_key = api_key
    if not actual_api_key:
        import os

        # Check environment variables using the engine's env_api_key_names
        for env_var in BraveNewsSearchEngine.env_api_key_names:
            if env_var in os.environ:
                actual_api_key = os.environ[env_var]
                break

    # Create a simple config for this request
    config = EngineConfig(
        api_key=actual_api_key,
        enabled=True,
        default_params={
            "count": count,
            "country": country,
            "search_lang": search_lang,
            "ui_lang": ui_lang,
            "freshness": freshness,
        },
    )

    # Create the engine instance
    engine = BraveNewsSearchEngine(
        config=config,
        count=count,
        country=country,
        search_lang=search_lang,
        ui_lang=ui_lang,
        freshness=freshness,
    )

    # Perform the search
    return await engine.search(query)
