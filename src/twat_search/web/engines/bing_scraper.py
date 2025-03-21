#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["scrape-bing"]
# ///
# this_file: src/twat_search/web/engines/bing_scraper.py
"""
Bing Scraper search engine implementation.

This module implements the Bing search integration using the scrape-bing library.
It provides a web scraping approach to search Bing without requiring an API key.

The BingScraperSearchEngine class handles all interactions with the scrape-bing
library, providing robust error handling, result validation, and conversion to
the standard SearchResult format used throughout the package.
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from pydantic import BaseModel, HttpUrl, ValidationError

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import BING_SCRAPER, DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult

# Set up logger
logger = logging.getLogger(__name__)

# Import the BingScraper class from scrape-bing package
try:
    from scrape_bing import BingScraper  # type: ignore
except ImportError:
    # For type checking when scrape-bing is not installed
    class BingScraper:  # type: ignore
        """Dummy class for type checking when scrape-bing is not installed."""

        def __init__(
            self,
            max_retries: int = 3,
            delay_between_requests: float = 1.0,
        ) -> None:
            """
            Initialize a dummy BingScraper for type checking.

            Args:
                max_retries: Maximum number of retries for failed requests
                delay_between_requests: Delay between requests in seconds
            """
            self.max_retries = max_retries
            self.delay_between_requests = delay_between_requests

        def search(self, query: str, num_results: int = 10) -> list[Any]:
            """
            Dummy search method for type checking.

            Args:
                query: Search query
                num_results: Number of results to return

            Returns:
                Empty list (dummy implementation)
            """
            return []


class BingScraperResult(BaseModel):
    """
    Pydantic model for a single Bing Scraper search result.

    This model is used to validate the response from the Bing Scraper.
    It ensures that each result has the required fields and proper types
    before being converted to the standard SearchResult model.

    Attributes:
        title: The title of the search result
        url: The URL of the search result, validated as a proper HTTP URL
        description: Optional description/snippet of the search result
    """

    title: str
    url: HttpUrl
    description: str | None = None


@register_engine
class BingScraperSearchEngine(SearchEngine):
    """
    Implementation of the Bing search using scrape-bing library.

    This engine scrapes Bing search results without requiring an API key.
    It provides a way to search Bing using web scraping techniques, with
    configurable retry behavior and delay between requests.

    Attributes:
        engine_code: The name of the search engine ("bing_scraper")
        env_api_key_names: Empty list since no API key is needed
    """

    engine_code = BING_SCRAPER
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[BING_SCRAPER]
    env_api_key_names: ClassVar[list[str]] = []  # No API key needed

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | str | None = True,
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize Bing Scraper Search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return
            country: Country code for results (not used by Bing Scraper, kept for interface consistency)
            language: Language code for results (not used by Bing Scraper, kept for interface consistency)
            safe_search: Whether to enable safe search (not used by Bing Scraper, kept for interface consistency)
            time_frame: Time frame for results (not used by Bing Scraper, kept for interface consistency)
            **kwargs: Additional Bing Scraper-specific parameters including:
                max_retries: Maximum number of retries for failed requests
                delay_between_requests: Delay between requests in seconds
        """
        super().__init__(config, **kwargs)
        # Set max_results from num_results or fall back to config default
        self.num_results = num_results

        self.max_retries: int = kwargs.get(
            "max_retries",
        ) or self.config.default_params.get("max_retries", 3)
        self.delay_between_requests: float = kwargs.get(
            "delay_between_requests",
        ) or self.config.default_params.get("delay_between_requests", 1.0)

        # Log any unused parameters for clarity
        unused_params: list[str] = []
        if country:
            unused_params.append(f"country='{country}'")
        if language:
            unused_params.append(f"language='{language}'")
        if safe_search is not None:
            unused_params.append(f"safe_search={safe_search}")
        if time_frame:
            unused_params.append(f"time_frame='{time_frame}'")
        if unused_params:
            logger.debug(
                f"Parameters {', '.join(unused_params)} set but not used by Bing Scraper",
            )

    def _convert_result(self, result: Any) -> SearchResult | None:
        """
        Convert a raw result from BingScraper into a SearchResult.

        This method validates the raw result using the BingScraperResult model
        and converts it to the standard SearchResult format if valid.

        Args:
            result: Raw result object from the BingScraper

        Returns:
            SearchResult object or None if validation fails
        """
        if not result:
            logger.warning("Empty result received from Bing Scraper")
            return None

        if not hasattr(result, "title") or not hasattr(result, "url"):
            logger.warning(f"Invalid result format: {result}")
            return None

        try:
            # Validate result fields
            validated = BingScraperResult(
                title=result.title,
                url=result.url,
                description=result.description if hasattr(result, "description") else None,
            )

            # Create and return the SearchResult
            return SearchResult(
                title=validated.title,
                url=validated.url,
                snippet=validated.description or "",
                source=self.engine_code,
                raw={
                    "title": result.title,
                    "url": str(result.url),
                    "description": result.description if hasattr(result, "description") else None,
                },
            )
        except ValidationError as exc:
            logger.warning(f"Validation error for result: {exc}")
            return None
        except Exception as exc:
            logger.warning(f"Unexpected error converting result: {exc}")
            return None

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Bing Scraper.

        This method uses the scrape-bing library, performs the search,
        and converts the results to the standard SearchResult format.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails due to invalid input, network issues,
                         parsing errors, or other exceptions
        """
        if not query:
            raise EngineError(self.engine_code, "Search query cannot be empty")

        logger.info(f"Searching Bing with query: '{query}'")

        try:
            # Create a scraper instance
            scraper = BingScraper(
                max_retries=self.max_retries,
                delay_between_requests=self.delay_between_requests,
            )

            # Perform the search
            raw_results = scraper.search(query, num_results=self.num_results)

            # Return an empty list if no results
            if not raw_results:
                logger.info("No results returned from Bing Scraper")
                return []

            logger.debug(
                f"Received {len(raw_results)} raw results from Bing Scraper",
            )

            # Convert the results - respecting max_results
            results = []
            for result in raw_results[: self.num_results]:
                search_result = self._convert_result(result)
                if search_result:
                    results.append(search_result)
                    # Stop if we've reached the desired number of results
                    if len(results) >= self.num_results:
                        break

            logger.info(
                f"Returning {len(results)} validated results from Bing Scraper",
            )
            return self.limit_results(results)

        except ConnectionError as exc:
            error_msg = f"Network error connecting to Bing: {exc}"
            logger.error(error_msg)
            raise EngineError(self.engine_code, error_msg) from exc
        except Exception as exc:
            error_msg = f"Error parsing Bing search results: {exc}"
            logger.error(error_msg)
            raise EngineError(self.engine_code, error_msg) from exc


async def bing_scraper(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    max_retries: int = 3,
    delay_between_requests: float = 1.0,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Bing Scraper.

    This convenience function creates and uses the BingScraperSearchEngine
    directly to avoid any potential fallback behavior.

    Args:
        query: The search query
        num_results: Number of results to return
        max_retries: Maximum number of retries for failed requests
        delay_between_requests: Delay between requests in seconds
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results
    """
    # Create a simple configuration with no API key required
    config = EngineConfig(enabled=True)

    # Create the engine with the provided parameters
    engine = BingScraperSearchEngine(
        config,
        num_results=num_results,
        max_retries=max_retries,
        delay_between_requests=delay_between_requests,
        **kwargs,
    )

    # Perform the search directly using the engine
    return await engine.search(query)
