# this_file: src/twat_search/web/engines/pplx.py

"""
Perplexity AI search engine implementation.

This module implements the Perplexity AI API integration.
"""

import httpx
from typing import ClassVar
from pydantic import BaseModel, Field, ValidationError

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class PerplexityResult(BaseModel):
    """
    Pydantic model for a single Perplexity result.

    This model is used to validate the response content.
    """

    answer: str = Field(default="")  # Perplexity may sometimes not include all details
    url: str = Field(default="https://perplexity.ai")  # Default URL if none provided
    title: str = Field(default="Perplexity AI Response")  # Default title


class PerplexityResponse(BaseModel):
    """
    Pydantic model for the Perplexity API response structure.
    """

    answers: list[PerplexityResult]  # Expect a list based on the API spec


@register_engine
class PerplexitySearchEngine(SearchEngine):
    """Implementation of the Perplexity AI API."""

    name = "pplx"
    env_api_key_names: ClassVar[list[str]] = [
        "PERPLEXITYAI_API_KEY",
        "PERPLEXITY_API_KEY",
        "PPLX_API_KEY",
    ]

    def __init__(self, config: EngineConfig, model: str | None = None) -> None:
        """
        Initialize the Perplexity search engine.

        Args:
            config: Configuration for this search engine
            model: Model to use for search (overrides config)

        Raises:
            EngineError: If the API key is missing
        """
        super().__init__(config)
        self.base_url = "https://api.perplexity.ai/chat/completions"

        # Use provided model if available, otherwise use default from config
        self.model = model or self.config.default_params.get(
            "model", "llama-3.1-sonar-large-128k-online"
        )

        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Perplexity API key is required. Set it in config or via one of these env vars: {', '.join(self.env_api_key_names)}.",
            )

        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.config.api_key}",
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Perplexity AI API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
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

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url, headers=self.headers, json=payload, timeout=10
                )
                response.raise_for_status()

                data = response.json()

                # Adapt the parsing logic to Perplexity's response format
                # We wrap the response in a structure that matches our expected model
                perplexity_response = PerplexityResponse(
                    answers=[
                        {
                            "answer": choice["message"]["content"],
                            "url": "https://perplexity.ai",
                            "title": f"Perplexity AI Response: {query[:30]}...",
                        }
                        for choice in data.get("choices", [])
                    ]
                )

                results = []
                for result in perplexity_response.answers:
                    try:
                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=result.title,
                                url=result.url,  # URLs are already strings
                                snippet=result.answer,  # Use the answer as the snippet
                                source=self.name,
                                raw=data,  # Include raw API response
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


async def pplx(
    query: str,
    api_key: str | None = None,
    model: str | None = None,
) -> list[SearchResult]:
    """
    Perform an AI-powered search using Perplexity AI API.

    This function provides a simple interface to the Perplexity AI API, allowing
    users to get AI-generated answers to their queries. It returns structured
    results with answer content from the specified AI model.

    If no API key is provided, the function will attempt to find one in the environment
    variables using the names defined in PerplexitySearchEngine.env_api_key_names
    (typically "PERPLEXITYAI_API_KEY", "PERPLEXITY_API_KEY", or "PPLX_API_KEY").

    Args:
        query: The search query string
        api_key: Optional Perplexity API key. If not provided, will look for it in environment variables
        model: Model to use for search (defaults to "llama-3.1-sonar-large-128k-online" if not specified)

    Returns:
        A list of SearchResult objects containing the search results with:
        - title: The title of the result (formatted as "Perplexity AI Response: {query}")
        - url: The URL (defaults to "https://perplexity.ai")
        - snippet: The AI-generated answer content
        - source: The source engine ("pplx")
        - raw: The raw result data from the API

    Raises:
        EngineError: If the search fails or API key is missing

    Examples:
        # Using API key from environment variable
        >>> results = await pplx("What is quantum computing?")
        >>> for result in results:
        ...     print(result.snippet)

        # Explicitly providing API key
        >>> results = await pplx(
        ...     "Explain the theory of relativity",
        ...     api_key="your-api-key"
        ... )

        # Specifying a different model
        >>> results = await pplx(
        ...     "What are the benefits of green energy?",
        ...     model="llama-3.1-sonar-small-32k-online"
        ... )
    """
    # Try to get API key from environment if not provided
    actual_api_key = api_key
    if not actual_api_key:
        import os

        # Check environment variables using the engine's env_api_key_names
        for env_var in PerplexitySearchEngine.env_api_key_names:
            if env_var in os.environ:
                actual_api_key = os.environ[env_var]
                break

    # Create a simple config for this request
    config = EngineConfig(
        api_key=actual_api_key, enabled=True, default_params={"model": model}
    )

    # Create the engine instance
    engine = PerplexitySearchEngine(
        config=config,
        model=model,
    )

    # Perform the search
    return await engine.search(query)
