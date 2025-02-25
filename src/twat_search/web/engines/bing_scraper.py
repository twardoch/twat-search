#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["scrape-bing"]
# ///
# this_file: src/twat_search/web/engines/bing_scraper.py

"""
Bing Scraper search engine implementation.

This module implements the Bing search integration using the scrape-bing library.
"""

import logging
from typing import Any, ClassVar

from pydantic import BaseModel, HttpUrl, ValidationError

try:
    from scrape_bing import BingScraper
except ImportError:
    # For type checking when scrape-bing is not installed
    class BingScraper:  # type: ignore
        """Dummy class for type checking when scrape-bing is not installed."""

        def __init__(self, max_retries=3, delay_between_requests=1.0):
            pass

        def search(self, query, num_results=10):
            pass


from twat_search.web.config import EngineConfig
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine

logger = logging.getLogger(__name__)


class BingScraperResult(BaseModel):
    """
    Pydantic model for a single Bing Scraper search result.

    This model is used to validate the response from the Bing Scraper.
    """

    title: str
    url: HttpUrl
    description: str | None = None


@register_engine
class BingScraperSearchEngine(SearchEngine):
    """Implementation of the Bing search using scrape-bing library."""

    name = "bing-scraper"
    env_api_key_names: ClassVar[list[str]] = []  # No API key needed

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
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
            **kwargs: Additional Bing Scraper-specific parameters
        """
        super().__init__(config, **kwargs)
        self.max_results = num_results or self.config.default_params.get(
            "max_results", 5
        )
        self.max_retries = kwargs.get("max_retries") or self.config.default_params.get(
            "max_retries", 3
        )
        self.delay_between_requests = kwargs.get(
            "delay_between_requests"
        ) or self.config.default_params.get("delay_between_requests", 1.0)

        # Log any unused parameters for clarity
        unused_params = []
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
                f"Parameters {', '.join(unused_params)} set but not used by Bing Scraper"
            )

    def _convert_result(self, result: Any) -> SearchResult | None:
        """
        Convert a raw result from BingScraper into a SearchResult.

        Returns None if validation fails.
        """
        try:
            validated = BingScraperResult(
                title=result.title,
                url=result.url,
                description=result.description,
            )
            return SearchResult(
                title=validated.title,
                url=validated.url,
                snippet=validated.description or "",
                source=self.name,
                raw={
                    "title": result.title,
                    "url": result.url,
                    "description": result.description,
                },
            )
        except ValidationError as exc:
            logger.warning(f"Validation error for result: {exc}")
            return None

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Bing Scraper.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        try:
            scraper = BingScraper(
                max_retries=self.max_retries,
                delay_between_requests=self.delay_between_requests,
            )
            raw_results = scraper.search(query, num_results=self.max_results)
        except ValueError as exc:
            raise EngineError(self.name, f"Invalid input: {exc}") from exc
        except ConnectionError as exc:
            raise EngineError(self.name, f"Network error: {exc}") from exc
        except RuntimeError as exc:
            raise EngineError(self.name, f"Parsing error: {exc}") from exc
        except Exception as exc:
            raise EngineError(self.name, f"Search failed: {exc}") from exc

        # Convert and filter results in a single comprehension
        results = [
            search_result
            for search_result in (
                self._convert_result(result) for result in raw_results
            )
            if search_result is not None
        ]
        return results


async def bing_scraper(
    query: str,
    num_results: int = 5,
    max_retries: int = 3,
    delay_between_requests: float = 1.0,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using Bing Scraper.

    This is a convenience function that calls the main search API with
    the Bing Scraper engine.

    Args:
        query: The search query
        num_results: Number of results to return
        max_retries: Maximum number of retries for failed requests
        delay_between_requests: Delay between requests in seconds
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        List of search results

    Raises:
        EngineError: If the search fails
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["bing-scraper"],
        num_results=num_results,
        bing_scraper_max_retries=max_retries,
        bing_scraper_delay_between_requests=delay_between_requests,
        **kwargs,
    )
