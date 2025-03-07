#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["duckduckgo-search"]
# ///
# this_file: src/twat_search/web/engines/duckduckgo.py
"""
DuckDuckGo Search engine implementation.

This module implements the DuckDuckGo search API integration using the duckduckgo_search library.
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

from duckduckgo_search import DDGS
from pydantic import BaseModel, HttpUrl, ValidationError

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS
from twat_search.web.engines import DUCKDUCKGO, ENGINE_FRIENDLY_NAMES
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult

logger = logging.getLogger(__name__)


class DuckDuckGoResult(BaseModel):
    """
    Pydantic model for a single DuckDuckGo search result.
    """

    title: str
    href: HttpUrl
    body: str


@register_engine
class DuckDuckGoSearchEngine(SearchEngine):
    """Implementation of the DuckDuckGo Search API."""

    engine_code = DUCKDUCKGO
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[DUCKDUCKGO]
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
        Initialize DuckDuckGo Search engine.

        Args:
            config: Engine configuration.
            num_results: Number of results to return.
            country: Country code for results.
            language: Language code (not directly used by DuckDuckGo).
            safe_search: Whether to enable safe search.
            time_frame: Time frame for results.
            **kwargs: Additional DuckDuckGo-specific parameters.
        """
        super().__init__(config, **kwargs)
        (
            self.num_results,
            self.region,
            self.language,
            self.timelimit,
            self.safesearch,
            self.proxy,
            self.timeout,
        ) = self._map_init_params(
            num_results,
            country,
            language,
            safe_search,
            time_frame,
            kwargs,
            self.config,
        )
        if self.language:
            logger.debug(
                f"Language '{self.language}' set but not directly used by DuckDuckGo API",
            )

    @staticmethod
    def _map_init_params(
        num_results: int,
        country: str | None,
        language: str | None,
        safe_search: bool | str | None,
        time_frame: str | None,
        kwargs: dict[str, Any],
        config: EngineConfig,
    ) -> tuple[int, str | None, str | None, str | None, bool, str | None, int]:
        """
        Map and normalize initialization parameters.
        """
        num_results = kwargs.get(
            "num_results",
            num_results,
        ) or config.default_params.get("num_results", 10)
        region = kwargs.get("region", country) or config.default_params.get(
            "region",
            None,
        )
        lang = language or config.default_params.get("language", None)
        timelimit = kwargs.get("timelimit", time_frame) or config.default_params.get(
            "timelimit",
            None,
        )
        if timelimit and not kwargs.get("timelimit"):
            time_mapping = {"day": "d", "week": "w", "month": "m", "year": "y"}
            timelimit = time_mapping.get(timelimit.lower(), timelimit)
        safesearch = kwargs.get("safesearch", safe_search)
        if isinstance(safesearch, str):
            safesearch = safesearch.lower() not in ["off", "false"]
        proxy = kwargs.get("proxy") or config.default_params.get("proxy", None)
        timeout = kwargs.get(
            "timeout",
        ) or config.default_params.get("timeout", 10)
        return num_results, region, lang, timelimit, safesearch, proxy, timeout

    def _convert_result(self, raw: dict[str, Any]) -> SearchResult | None:
        """
        Convert a raw DuckDuckGo result to a SearchResult.
        """
        try:
            ddg_result = DuckDuckGoResult(
                title=raw["title"],
                href=raw["href"],
                body=raw["body"],
            )
            return SearchResult(
                title=ddg_result.title,
                url=ddg_result.href,
                snippet=ddg_result.body,
                source=self.engine_code,
                raw=raw,
            )
        except ValidationError as exc:
            logger.warning(f"Validation error for result: {exc}")
            return None

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the DuckDuckGo Search API.

        Args:
            query: The search query string.

        Returns:
            A list of SearchResult objects.

        Raises:
            EngineError: If the search fails.
        """
        try:
            ddgs = DDGS(proxy=self.proxy, timeout=self.timeout)

            # Convert boolean safesearch to string value expected by the API
            safesearch_value = "moderate"
            if self.safesearch is False:
                safesearch_value = "off"
            elif self.safesearch is True:
                safesearch_value = "moderate"

            # Call with positional and named parameters according to the method signature
            raw_results = ddgs.text(
                keywords=query,
                region=self.region or "wt-wt",  # Default to worldwide
                safesearch=safesearch_value,
                timelimit=self.timelimit,
                max_results=self.num_results,
            )

            results = []
            for raw in raw_results:
                converted = self._convert_result(raw)
                if converted:
                    results.append(converted)
                    # Limit results to max_results
                    if len(results) >= self.num_results:
                        break
            return results

        except Exception as exc:
            raise EngineError(
                self.engine_code,
                f"Search failed: {exc}",
            ) from exc


async def duckduckgo(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool = True,
    time_frame: str | None = None,
    proxy: str | None = None,
    timeout: int = 10,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using DuckDuckGo.

    This convenience function creates and uses a DuckDuckGoSearchEngine instance
    directly to avoid any potential fallback behavior.

    Args:
        query: The search query.
        num_results: Number of results to return.
        country: Country code for results.
        language: Language code.
        safe_search: Whether to enable safe search.
        time_frame: Time frame for results.
        proxy: Optional proxy to use.
        timeout: Request timeout in seconds.
        **kwargs: Additional parameters.

    Returns:
        A list of search results.

    Raises:
        EngineError: If the search fails.
    """
    # Create a simple configuration (no API key required)
    config = EngineConfig(enabled=True)

    # Create the engine instance with all parameters
    engine = DuckDuckGoSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        proxy=proxy,
        timeout=timeout,
        **kwargs,
    )

    # Perform the search directly using the engine
    return await engine.search(query)
