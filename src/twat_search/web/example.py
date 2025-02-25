#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["httpx>=0.24.1", "pydantic>=2.0.0", "python-dotenv>=1.0.0"]
# ///
# this_file: src/twat_search/web/example.py

"""
Example usage of the web search API.

This script demonstrates how to use the web search API with different
configurations and search engines.
"""

import asyncio
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
    logger.info("Loaded environment variables from .env file")
except ImportError:
    logger.warning("python-dotenv not installed, skipping .env loading")

# Import the search API
from twat_search.web.api import search
from twat_search.web.models import SearchResult
from twat_search.web.config import Config, EngineConfig


async def display_results(results: list[SearchResult], title: str) -> None:
    """Display search results in a readable format."""

    for _i, _result in enumerate(results, 1):
        pass  # Truncate long snippets


async def example_default_config() -> None:
    """Example using default configuration."""
    try:
        results = await search("latest news about AI")
        await display_results(results, "Default Configuration")
    except Exception as e:
        logger.error(f"Example failed: {e}")


async def example_specific_engines() -> None:
    """Example using only specific engines."""
    try:
        results = await search("population of Tokyo", engines=["brave", "google"])
        await display_results(results, "Specific Engines (Brave, Google)")
    except Exception as e:
        logger.error(f"Example failed: {e}")


async def example_override_params() -> None:
    """Example overriding default parameters."""
    try:
        results = await search(
            "best Python libraries for data science",
            brave_count=5,  # Brave-specific override
            google_count=3,  # Google-specific override
            count=10,  # Default for all other engines
        )
        await display_results(results, "Override Parameters")
    except Exception as e:
        logger.error(f"Example failed: {e}")


async def example_custom_config() -> None:
    """Example using custom configuration."""
    try:
        # Create a custom configuration
        config = Config(
            engines={
                "brave": EngineConfig(
                    api_key=os.environ.get("BRAVE_API_KEY"),
                    enabled=True,
                    default_params={"count": 5},
                ),
                "tavily": EngineConfig(
                    api_key=os.environ.get("TAVILY_API_KEY"),
                    enabled=True,
                    default_params={"max_results": 3},
                ),
            }
        )

        results = await search("machine learning tutorials", config=config)
        await display_results(results, "Custom Configuration")
    except Exception as e:
        logger.error(f"Example failed: {e}")


async def main() -> None:
    """Run all examples."""
    logger.info("Starting web search examples")

    # Print available API keys for debugging
    api_keys = {
        "BRAVE_API_KEY": bool(os.environ.get("BRAVE_API_KEY")),
        "SERPAPI_API_KEY": bool(os.environ.get("SERPAPI_API_KEY")),
        "TAVILY_API_KEY": bool(os.environ.get("TAVILY_API_KEY")),
        "PERPLEXITYAI_API_KEY": bool(os.environ.get("PERPLEXITYAI_API_KEY")),
        "YOUCOM_API_KEY": bool(os.environ.get("YOUCOM_API_KEY")),
    }
    logger.info(f"API keys available: {api_keys}")

    # Run examples
    await example_default_config()
    await example_specific_engines()
    await example_override_params()
    await example_custom_config()

    logger.info("All examples completed")


if __name__ == "__main__":
    asyncio.run(main())
