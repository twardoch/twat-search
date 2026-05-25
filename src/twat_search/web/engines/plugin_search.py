# this_file: src/twat_search/web/engines/plugin_search.py
"""Template-driven search plugin engine for external search adapters."""

from __future__ import annotations

from string import Formatter
from typing import Any
from urllib.parse import quote, quote_plus

from pydantic import BaseModel, Field, ValidationError, field_validator

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import DEFAULT_NUM_RESULTS, ENGINE_FRIENDLY_NAMES, PLUGIN_SEARCH
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from twat_search.web.provider_catalog import get_provider_metadata

_ALLOWED_TEMPLATE_FIELDS = {
    "query",
    "query_plus",
    "query_quote",
    "query_url",
    "plugin_code",
    "plugin_name",
}


class SearchPluginSpec(BaseModel):
    """Configurable search plugin that expands a user query into a result URL."""

    code: str
    name: str
    url_template: str
    title_template: str = "{plugin_name}: {query}"
    snippet_template: str = "Search {plugin_name} for {query}"
    source: str | None = None
    enabled: bool = True
    query_template: str = "{query}"
    rank: int | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

    @field_validator("code", "name", "url_template")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Require non-empty text fields at the plugin boundary."""
        text = value.strip()
        if not text:
            msg = "Search plugin code, name, and url_template must be non-empty"
            raise ValueError(msg)
        return text

    @field_validator("url_template", "title_template", "snippet_template", "query_template")
    @classmethod
    def validate_template_fields(cls, value: str) -> str:
        """Reject unknown template fields before runtime expansion."""
        fields = {name for _, name, _, _ in Formatter().parse(value) if name}
        unknown = fields - _ALLOWED_TEMPLATE_FIELDS
        if unknown:
            msg = f"Unsupported search plugin template fields: {', '.join(sorted(unknown))}"
            raise ValueError(msg)
        return value

    def render(self, query: str) -> SearchResult:
        """Expand this plugin into a normalized search result."""
        rendered_query = _render_template(self.query_template, _template_context(query, self))
        context = _template_context(rendered_query, self)
        title = _render_template(self.title_template, context)
        snippet = _render_template(self.snippet_template, context)
        url = _render_template(self.url_template, context)
        raw = {
            "plugin_code": self.code,
            "plugin_name": self.name,
            "query_template": self.query_template,
            "rendered_query": rendered_query,
            **self.raw,
        }
        return SearchResult(
            title=title,
            url=url,
            snippet=snippet,
            source=self.source or f"{PLUGIN_SEARCH}:{self.code}",
            rank=self.rank,
            raw=raw,
        )


def _template_context(query: str, plugin: SearchPluginSpec) -> dict[str, str]:
    """Build the small template context allowed for plugin expansion."""
    return {
        "query": query,
        "query_plus": quote_plus(query),
        "query_quote": quote(query, safe=""),
        "query_url": quote_plus(query),
        "plugin_code": plugin.code,
        "plugin_name": plugin.name,
    }


def _render_template(template: str, context: dict[str, str]) -> str:
    """Render a plugin template with a fixed set of validated fields."""
    return template.format(**context)


def parse_plugin_specs(specs: Any) -> list[SearchPluginSpec]:
    """Parse raw plugin dictionaries into validated plugin specs."""
    if specs is None:
        return []
    if not isinstance(specs, list):
        msg = "plugin_search plugins must be a list of plugin objects"
        raise EngineError(PLUGIN_SEARCH, msg)
    try:
        return [item if isinstance(item, SearchPluginSpec) else SearchPluginSpec.model_validate(item) for item in specs]
    except ValidationError as exc:
        raise EngineError(PLUGIN_SEARCH, f"Invalid plugin_search configuration: {exc}") from exc


@register_engine
class PluginSearchEngine(SearchEngine):
    """Search engine that exposes configured query-template plugins as results."""

    engine_code = PLUGIN_SEARCH
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[PLUGIN_SEARCH]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        plugins: list[dict[str, Any] | SearchPluginSpec] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize plugin search with explicit or configured plugin specs."""
        super().__init__(config=config, num_results=num_results, **kwargs)
        raw_plugins = plugins
        if raw_plugins is None:
            raw_plugins = self.config.default_params.get("plugins")
        if raw_plugins is None:
            provider = get_provider_metadata(PLUGIN_SEARCH)
            raw_plugins = provider.default_params.get("plugins", []) if provider else []
        self.plugins = parse_plugin_specs(raw_plugins)

    async def search(self, query: str) -> list[SearchResult]:
        """Return one normalized result per enabled configured search plugin."""
        results = [plugin.render(query) for plugin in self.plugins if plugin.enabled]
        return self.limit_results(results)


async def plugin_search(
    query: str,
    num_results: int = DEFAULT_NUM_RESULTS,
    plugins: list[dict[str, Any] | SearchPluginSpec] | None = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """Search configured query-template plugins."""
    config = EngineConfig(
        enabled=True,
        default_params={"plugins": plugins} if plugins is not None else {},
    )
    engine = PluginSearchEngine(config, num_results=num_results, plugins=plugins, **kwargs)
    return await engine.search(query)
