# this_file: src/twat_search/web/engines/pplx.py
"""
Perplexity AI search engine implementation.

This module implements the Perplexity AI API integration.
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar

import httpx
from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engines import ENGINE_FRIENDLY_NAMES, PPLX
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult

# Initialize logger
logger = logging.getLogger(__name__)


class PerplexityResult(BaseModel):
    """
    Pydantic model for a single Perplexity result.
    """

    # Perplexity may sometimes not include all details
    answer: str = Field(default="")
    # Default URL if none provided
    url: str = Field(default="https://perplexity.ai")
    title: str = Field(default="Perplexity AI Response")  # Default title


@register_engine
class PerplexitySearchEngine(SearchEngine):
    """Implementation of the Perplexity AI API."""

    engine_code = PPLX
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[PPLX]
    env_api_key_names: ClassVar[list[str]] = [
        "PERPLEXITYAI_API_KEY",
        "PERPLEXITY_API_KEY",
    ]

    def __init__(
        self,
        config: EngineConfig,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Perplexity search engine.
        """
        super().__init__(config, **kwargs)
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = kwargs.get("model") or self.config.default_params.get("model", "pplx-70b-online")

        # Set up the authentication headers using the api_key from base class
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}",
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Perplexity AI API.
        """
        if not query:
            raise EngineError(self.engine_code, "Search query cannot be empty")

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise. I am an expert and do not need explanation",
                },
                {"role": "user", "content": query},
            ],
        }

        try:
            response = await self.make_http_request(
                url=self.base_url,
                method="POST",
                headers=self.headers,
                json_data=payload,
            )
            data = response.json()
        except EngineError as e:
            raise EngineError(
                self.engine_code,
                f"API request failed: {str(e)!s}",
            )
        except Exception as e:
            raise EngineError(
                self.engine_code,
                f"Unexpected error: {str(e)!s}",
            )

        results = []
        for choice in data.get("choices", []):
            answer = choice.get("message", {}).get("content", "")
            url = "https://perplexity.ai"
            title = f"Perplexity AI Response: {query[:30]}..."
            try:
                # Validate and build the result using the PerplexityResult model
                pr = PerplexityResult(answer=answer, url=url, title=title)
                url_obj = HttpUrl(pr.url)  # Validate URL format
                results.append(
                    SearchResult(
                        title=pr.title,
                        url=url_obj,
                        snippet=pr.answer,
                        source=self.engine_code,
                        raw=data,
                    ),
                )

                # Respect the max_results limit
                if len(results) >= self.max_results:
                    break
            except ValidationError as e:
                logger.warning(f"Invalid result from Perplexity: {e}")
                continue

        return self.limit_results(results)


async def pplx(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search with Perplexity AI.

    Args:
        query: The search query
        num_results: Maximum number of results to return
        country: Not used by Perplexity
        language: Not used by Perplexity
        safe_search: Not used by Perplexity
        time_frame: Not used by Perplexity
        model: The model to use (e.g., "pplx-70b-online")
        api_key: Perplexity API key (if not set via environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
        engine_code=PPLX,
    )

    engine = PerplexitySearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        model=model,
    )

    return await engine.search(query)
