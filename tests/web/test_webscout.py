#!/usr/bin/env python3
# this_file: tests/web/test_webscout.py

"""
Tests for the WebScout search engine.
"""

import pytest
from unittest.mock import patch, MagicMock

from twat_search.web.config import EngineConfig
from twat_search.web.engines import WebScoutEngine
from twat_search.web.engines.webscout import webscout
from twat_search.web.models import SearchResult


@pytest.fixture
def engine_config():
    """Create a basic engine configuration for testing."""
    return EngineConfig(enabled=True)


@pytest.fixture
def engine(engine_config):
    """Create a WebScout engine instance for testing."""
    return WebScoutEngine(config=engine_config, num_results=5, safe_search="off")


class TestWebScoutEngine:
    """Tests for the WebScout search engine."""

    @patch("webscout.GoogleS")
    def test_init(self, mock_GoogleS, engine):
        """Test WebScoutEngine initialization."""
        assert engine.name == "webscout"
        assert engine.num_results == 5
        assert engine.safe_search == "off"
        # Lazy initialization - GoogleS shouldn't be called yet
        mock_GoogleS.assert_not_called()

    @patch("webscout.GoogleS")
    async def test_search_basic(self, mock_GoogleS, engine):
        """Test basic search functionality."""
        # Setup mock
        mock_instance = MagicMock()
        mock_GoogleS.return_value = mock_instance

        # Mock search results
        mock_instance.search.return_value = [
            {
                "title": "Test Result 1",
                "href": "https://example.com/1",
                "abstract": "First test result",
                "index": 0,
            },
            {
                "title": "Test Result 2",
                "href": "example.com/2",  # Missing protocol
                "abstract": "Second test result",
                "index": 1,
            },
        ]

        # Perform search
        results = await engine.search("test query")

        # Verify results
        assert len(results) == 2
        assert isinstance(results[0], SearchResult)
        assert results[0].title == "Test Result 1"
        assert str(results[0].url) == "https://example.com/1"
        assert results[0].snippet == "First test result"
        assert results[0].source == "webscout"

        # Verify URL handling (protocol added)
        assert str(results[1].url) == "https://example.com/2"

        # Verify search parameters
        mock_instance.search.assert_called_once()
        call_args = mock_instance.search.call_args[1]
        assert call_args["query"] == "test query"
        assert call_args["max_results"] == 5
        assert call_args["safe"] == "off"

    @patch("webscout.GoogleS")
    async def test_search_parameters(self, mock_GoogleS, engine):
        """Test search with various parameters."""
        # Setup mock
        mock_instance = MagicMock()
        mock_GoogleS.return_value = mock_instance
        mock_instance.search.return_value = []

        # Perform search with parameters
        await engine.search(
            "test query",
            num_results=10,
            country="us",
            language="en",
            safe_search="strict",
            time_frame="month",
        )

        # Verify parameter mapping
        call_args = mock_instance.search.call_args[1]
        assert call_args["query"] == "test query"
        assert call_args["max_results"] == 10
        assert call_args["country"] == "us"
        assert call_args["language"] == "en"
        assert call_args["safe"] == "active"
        assert call_args["time_period"] == "month"

    @patch("webscout.GoogleS")
    async def test_safe_search_mapping(self, mock_GoogleS, engine):
        """Test safe search parameter mapping."""
        # Setup mock
        mock_instance = MagicMock()
        mock_GoogleS.return_value = mock_instance
        mock_instance.search.return_value = []

        # Test 'strict' mapping
        await engine.search("test", safe_search="strict")
        assert mock_instance.search.call_args[1]["safe"] == "active"

        # Test 'moderate' mapping
        await engine.search("test", safe_search="moderate")
        assert mock_instance.search.call_args[1]["safe"] == "moderate"

        # Test 'off' mapping
        await engine.search("test", safe_search="off")
        assert mock_instance.search.call_args[1]["safe"] == "off"

    @patch("webscout.GoogleS")
    async def test_invalid_url_handling(self, mock_GoogleS, engine):
        """Test handling of invalid URLs."""
        # Setup mock
        mock_instance = MagicMock()
        mock_GoogleS.return_value = mock_instance

        # Include an invalid URL that will fail HttpUrl validation
        mock_instance.search.return_value = [
            {
                "title": "Valid Result",
                "href": "https://example.com/valid",
                "abstract": "Valid URL",
                "index": 0,
            },
            {
                "title": "Invalid Result",
                "href": "invalid::/url",  # Invalid URL format
                "abstract": "Invalid URL",
                "index": 1,
            },
        ]

        # Perform search
        results = await engine.search("test query")

        # Only the valid result should be included
        assert len(results) == 1
        assert results[0].title == "Valid Result"

    @patch("webscout.GoogleS")
    async def test_webscout_convenience_function(self, mock_GoogleS):
        """Test the webscout convenience function."""
        # Setup mock
        mock_instance = MagicMock()
        mock_GoogleS.return_value = mock_instance
        mock_instance.search.return_value = [
            {
                "title": "Test Result",
                "href": "https://example.com",
                "abstract": "Test abstract",
                "index": 0,
            }
        ]

        # Use convenience function
        results = await webscout(
            "test query",
            num_results=3,
            country="ca",
            language="fr",
            safe_search="moderate",
        )

        # Verify results
        assert len(results) == 1
        assert results[0].title == "Test Result"

        # Verify parameters
        call_args = mock_instance.search.call_args[1]
        assert call_args["query"] == "test query"
        assert call_args["max_results"] == 3
        assert call_args["country"] == "ca"
        assert call_args["language"] == "fr"
        assert call_args["safe"] == "moderate"
