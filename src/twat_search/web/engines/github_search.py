# this_file: src/twat_search/web/engines/github_search.py
"""GitHub REST API search engine."""

from __future__ import annotations

import textwrap
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, GITHUB_SEARCH
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult

GitHubSearchType = Literal["repositories", "code", "issues"]


class GitHubRepositoryRef(BaseModel):
    """Minimal repository object embedded in GitHub search results."""

    full_name: str = ""
    html_url: HttpUrl | None = None
    description: str | None = None


class GitHubSearchItem(BaseModel):
    """Flexible item returned by GitHub search endpoints."""

    name: str | None = None
    full_name: str | None = None
    path: str | None = None
    title: str | None = None
    html_url: HttpUrl
    description: str | None = None
    body: str | None = None
    text_matches: list[dict[str, Any]] = Field(default_factory=list, alias="text_matches")
    repository: GitHubRepositoryRef | None = None


class GitHubSearchResponse(BaseModel):
    """Top-level GitHub search response."""

    total_count: int = Field(default=0, alias="total_count")
    incomplete_results: bool = Field(default=False, alias="incomplete_results")
    items: list[GitHubSearchItem] = Field(default_factory=list)


@register_engine
class GitHubSearchEngine(SearchEngine):
    """Search GitHub repositories, code, or issues through the REST API."""

    engine_code = GITHUB_SEARCH
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[GITHUB_SEARCH]
    env_api_key_names: ClassVar[list[str]] = [
        "GITHUB_API_TOKEN",
        "GITHUB_TOKEN",
        "HOMEBREW_GITHUB_API_TOKEN",
        "ZENCLI_GITHUBAUTHTOKEN",
    ]
    endpoint_by_type: ClassVar[dict[GitHubSearchType, str]] = {
        "repositories": "https://api.github.com/search/repositories",
        "code": "https://api.github.com/search/code",
        "issues": "https://api.github.com/search/issues",
    }

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        search_type: GitHubSearchType | None = None,
        sort: str | None = None,
        order: Literal["asc", "desc"] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the GitHub search engine."""
        super().__init__(
            config=config,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            **kwargs,
        )
        configured_type = self.config.default_params.get("search_type", "repositories")
        self.search_type: GitHubSearchType = search_type or configured_type
        if self.search_type not in self.endpoint_by_type:
            msg = f"Unsupported GitHub search_type: {self.search_type}"
            raise EngineError(self.engine_code, msg)
        self.sort = sort if sort is not None else self.config.default_params.get("sort")
        self.order = order or self.config.default_params.get("order", "desc")

    def _build_params(self, query: str) -> dict[str, Any]:
        """Build GitHub search query parameters."""
        params: dict[str, Any] = {
            "q": query,
            "per_page": min(max(self._get_num_results(min_value=1), 1), 100),
        }
        if self.sort:
            params["sort"] = self.sort
        if self.order:
            params["order"] = self.order
        return params

    def _endpoint(self) -> str:
        """Return the selected GitHub search endpoint."""
        return self.endpoint_by_type[self.search_type]

    def _snippet_from_text_matches(self, item: GitHubSearchItem) -> str | None:
        """Return a short text-match fragment when GitHub sends one."""
        for match in item.text_matches:
            fragment = match.get("fragment")
            if isinstance(fragment, str) and fragment.strip():
                return fragment
        return None

    def _convert_result(self, item: GitHubSearchItem, rank: int, raw: dict[str, Any]) -> SearchResult:
        """Convert one GitHub search item into the normalized result model."""
        repo_name = item.repository.full_name if item.repository else None
        if self.search_type == "code":
            title = f"{repo_name or 'GitHub'}:{item.path or item.name or ''}".rstrip(":")
            snippet = self._snippet_from_text_matches(item) or item.repository.description if item.repository else None
        elif self.search_type == "issues":
            title = item.title or item.html_url.unicode_string()
            snippet = item.body
        else:
            title = item.full_name or item.name or item.html_url.unicode_string()
            snippet = item.description

        return SearchResult(
            title=title,
            url=item.html_url,
            snippet=textwrap.shorten((snippet or "").strip(), width=500, placeholder="..."),
            source=self.engine_code,
            rank=rank,
            raw=raw,
        )

    async def search(self, query: str) -> list[SearchResult]:
        """Search GitHub via REST API."""
        if not query.strip():
            raise EngineError(self.engine_code, "Search query cannot be empty")

        response = await self.make_http_request(
            url=self._endpoint(),
            method="GET",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.config.api_key or ''}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            params=self._build_params(query),
        )

        try:
            data = response.json()
            parsed = GitHubSearchResponse.model_validate(data)
        except (ValueError, ValidationError) as exc:
            raise EngineError(self.engine_code, f"Response parsing error: {exc}") from exc

        raw_items = data.get("items", []) if isinstance(data, dict) else []
        results = [
            self._convert_result(item, rank, raw)
            for rank, (item, raw) in enumerate(zip(parsed.items, raw_items, strict=False), start=1)
        ]
        return self.limit_results(results)


async def github_search(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
    search_type: GitHubSearchType | None = None,
    sort: str | None = None,
    order: Literal["asc", "desc"] | None = None,
) -> list[SearchResult]:
    """Search GitHub repositories, code, or issues."""
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = GitHubSearchEngine(
        config=config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        search_type=search_type,
        sort=sort,
        order=order,
    )
    return await engine.search(query)
