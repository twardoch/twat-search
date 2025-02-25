#!/usr/bin/env python3
# this_file: src/twat_search/web/engines/webscout.py

"""
WebScout search engine integration.

This module implements the WebScout integration using the webscout library's
GoogleS class, which provides Google search functionality without requiring an API key.
"""

import logging
from typing import Any, ClassVar

try:
    from webscout import GoogleS  # type: ignore
except ImportError:
    msg = (
        "The 'webscout' package is not installed. "
        "Install it with 'pip install webscout>=0.3.1'"
    )
    raise ImportError(msg)

from pydantic import BaseModel, Field, HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine

logger = logging.getLogger(__name__)


class WebScoutResult(BaseModel):
    """Validate WebScout search results."""

    title: str
    href: str
    abstract: str = ""
    index: int = Field(ge=0)


@register_engine
class WebScoutEngine(SearchEngine):
    """
    WebScout search engine integration.

    This search engine uses the webscout library's GoogleS class to perform
    Google searches without requiring an API key.
    """

    name = "webscout"
    env_enabled_names: ClassVar[list[str]] = ["WEBSCOUT_ENABLED"]
    env_params_names: ClassVar[list[str]] = ["WEBSCOUT_DEFAULT_PARAMS"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 10,
        country: str | None = None,
        language: str | None = None,
        safe_search: str = "off",
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the WebScout search engine.

        Args:
            config: Engine configuration
            num_results: Maximum number of results to return
            country: Country code for localized results
            language: Language code for results
            safe_search: Level of safe search filtering ("off", "moderate", "strict")
            time_frame: Time frame filter ("day", "week", "month", "year")
            **kwargs: Additional parameters for the GoogleS class
        """
        super().__init__(config)
        self.num_results = num_results
        self.country = country
        self.language = language
        self.safe_search = safe_search
        self.time_frame = time_frame

        # Lazy initialization of GoogleS to avoid connection issues during testing
        self._googles = None

        logger.debug(f"Initialized {self.name} engine")

    @property
    def googles(self) -> GoogleS:
        """
        Lazy initialization of the GoogleS instance.

        Returns:
            GoogleS: The initialized GoogleS instance
        """
        if self._googles is None:
            self._googles = GoogleS(rate_limit=2.0)
        return self._googles

    async def search(
        self,
        query: str,
        num_results: int | None = None,
        country: str | None = None,
        language: str | None = None,
        safe_search: str | None = None,
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> list[SearchResult]:
        """
        Perform a search using WebScout's GoogleS implementation.

        Args:
            query: The search query
            num_results: Maximum number of results to return
            country: Country code for localized results
            language: Language code for results
            safe_search: Level of safe search filtering ("off", "moderate", "strict")
            time_frame: Time frame filter ("day", "week", "month", "year")
            **kwargs: Additional parameters to pass to the GoogleS search method

        Returns:
            List of search results

        Raises:
            EngineError: If the search fails
        """
        # Use provided values or fall back to instance defaults
        num_results = num_results or self.num_results
        country = country or self.country
        language = language or self.language
        safe_search = safe_search or self.safe_search
        time_frame = time_frame or self.time_frame

        logger.info(f"Searching with {self.name} for: {query}")

        # Build search parameters
        params: dict[str, Any] = {
            "max_results": num_results,
        }

        # Add optional parameters if they have values
        if country:
            params["country"] = country

        if language:
            params["language"] = language

        # Map safe_search values to webscout's safe parameter
        if safe_search:
            if safe_search == "strict":
                params["safe"] = "active"
            elif safe_search == "moderate":
                params["safe"] = "moderate"
            else:
                params["safe"] = "off"

        # Map time_frame to webscout's time parameter
        if time_frame:
            params["time_period"] = time_frame

        # Add any additional parameters
        params.update(kwargs)

        logger.debug(f"Search parameters: {params}")

        try:
            # Perform the search
            raw_results = self.googles.search(query=query, **params)

            # Process results
            results: list[SearchResult] = []

            for result in raw_results:
                try:
                    # Parse and validate the result
                    webscout_result = WebScoutResult(**result)

                    # Ensure URL has a protocol for proper HttpUrl validation
                    url_str = webscout_result.href
                    if not url_str.startswith(("http://", "https://")):
                        url_str = f"https://{url_str}"

                    # Create a SearchResult - Pydantic will convert valid str to HttpUrl
                    try:
                        search_result = SearchResult(
                            title=webscout_result.title,
                            url=HttpUrl(url_str),  # Explicitly convert to HttpUrl
                            snippet=webscout_result.abstract,
                            source=self.name,
                            rank=webscout_result.index,
                            raw=result,
                        )
                        results.append(search_result)
                    except ValueError as url_error:
                        # Log and skip results with invalid URLs
                        logger.warning(f"Invalid URL '{url_str}': {url_error}")

                except Exception as e:
                    logger.warning(f"Failed to parse result: {e}")
                    continue

            logger.info(f"Found {len(results)} results for '{query}'")
            return results

        except Exception as e:
            error_msg = f"WebScout search failed: {e!s}"
            logger.error(error_msg)
            raise EngineError(self.name, error_msg) from e


async def webscout(
    query: str,
    num_results: int = 10,
    country: str | None = None,
    language: str | None = None,
    safe_search: str = "off",
    time_frame: str | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Convenience function to search using the WebScout engine.

    Args:
        query: The search query
        num_results: Maximum number of results to return
        country: Country code for localized results
        language: Language code for results
        safe_search: Level of safe search filtering ("off", "moderate", "strict")
        time_frame: Time frame filter ("day", "week", "month", "year")
        **kwargs: Additional parameters to pass to the WebScout search method

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.config import Config, EngineConfig

    # Create config with WebScout enabled
    config = Config()
    if "webscout" not in config.engines:
        config.engines["webscout"] = EngineConfig(enabled=True)

    engine = WebScoutEngine(
        config=config.engines["webscout"],
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
    )

    return await engine.search(query, **kwargs)
