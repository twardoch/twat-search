#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_github_search.py
"""Unit tests for the GitHub search engine."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.github_search import GitHubSearchEngine
from twat_search.web.exceptions import EngineError


class FakeResponse:
    """Minimal HTTP response double for engine tests."""

    def __init__(self, data: Any) -> None:
        self.data = data

    def json(self) -> Any:
        """Return the fake JSON payload."""
        return self.data


def test_github_search_engine_is_registered() -> None:
    """GitHub search is available through the shared engine registry."""
    engine = get_engine("github_search", EngineConfig(api_key="test-token"))

    assert isinstance(engine, GitHubSearchEngine)


def test_github_search_builds_repository_params() -> None:
    """GitHub params use q, per_page, sort, and order."""
    engine = GitHubSearchEngine(
        EngineConfig(api_key="test-token"),
        num_results=150,
        sort="stars",
        order="asc",
    )

    assert engine._endpoint() == "https://api.github.com/search/repositories"
    assert engine._build_params("font tooling") == {
        "q": "font tooling",
        "per_page": 100,
        "sort": "stars",
        "order": "asc",
    }


def test_github_search_rejects_unsupported_type() -> None:
    """Unsupported search types fail at the boundary."""
    with pytest.raises(EngineError, match="Unsupported GitHub search_type"):
        GitHubSearchEngine(EngineConfig(api_key="test-token"), search_type="users")  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_github_search_converts_repository_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Repository search responses become normalized results."""
    engine = GitHubSearchEngine(EngineConfig(api_key="test-token"), num_results=2)
    captured_request: dict[str, Any] = {}

    async def fake_request(**kwargs: Any) -> FakeResponse:
        captured_request.update(kwargs)
        return FakeResponse(
            {
                "total_count": 2,
                "incomplete_results": False,
                "items": [
                    {
                        "full_name": "fonttools/fonttools",
                        "html_url": "https://github.com/fonttools/fonttools",
                        "description": "Tools to manipulate font files.",
                    },
                    {
                        "full_name": "googlefonts/fontbakery",
                        "html_url": "https://github.com/googlefonts/fontbakery",
                        "description": "Font quality checker.",
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("font tooling")

    assert captured_request["url"] == "https://api.github.com/search/repositories"
    assert captured_request["method"] == "GET"
    assert captured_request["headers"]["Accept"] == "application/vnd.github+json"
    assert captured_request["headers"]["Authorization"] == "Bearer test-token"
    assert captured_request["headers"]["X-GitHub-Api-Version"] == "2022-11-28"
    assert captured_request["params"]["q"] == "font tooling"
    assert [result.title for result in results] == ["fonttools/fonttools", "googlefonts/fontbakery"]
    assert [result.rank for result in results] == [1, 2]
    assert all(result.source == "github_search" for result in results)


@pytest.mark.asyncio
async def test_github_search_converts_code_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Code search responses include repository/path title and text match snippets."""
    engine = GitHubSearchEngine(EngineConfig(api_key="test-token"), search_type="code")

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse(
            {
                "items": [
                    {
                        "name": "classes.js",
                        "path": "src/attributes/classes.js",
                        "html_url": "https://github.com/jquery/jquery/blob/main/src/attributes/classes.js",
                        "repository": {
                            "full_name": "jquery/jquery",
                            "html_url": "https://github.com/jquery/jquery",
                            "description": "jQuery JavaScript Library",
                        },
                        "text_matches": [{"fragment": "function addClass(value) {"}],
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("addClass repo:jquery/jquery")

    assert results[0].title == "jquery/jquery:src/attributes/classes.js"
    assert results[0].snippet == "function addClass(value) {"


@pytest.mark.asyncio
async def test_github_search_converts_issue_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Issue search responses use issue titles and bodies."""
    engine = GitHubSearchEngine(EngineConfig(api_key="test-token"), search_type="issues")

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse(
            {
                "items": [
                    {
                        "title": "Bug in search",
                        "html_url": "https://github.com/example/project/issues/1",
                        "body": "Search fails with an edge case.",
                    },
                ],
            },
        )

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    results = await engine.search("bug search repo:example/project")

    assert results[0].title == "Bug in search"
    assert results[0].snippet == "Search fails with an edge case."


@pytest.mark.asyncio
async def test_github_search_reports_parse_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Invalid provider payloads raise a provider-specific EngineError."""
    engine = GitHubSearchEngine(EngineConfig(api_key="test-token"))

    async def fake_request(**_kwargs: Any) -> FakeResponse:
        return FakeResponse({"items": [{"full_name": "bad", "html_url": "not-a-url"}]})

    monkeypatch.setattr(engine, "make_http_request", fake_request)

    with pytest.raises(EngineError, match="Response parsing error"):
        await engine.search("font tooling")
