#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_plugin_search.py
"""Unit tests for template-driven search plugins."""

from __future__ import annotations

from typing import Any

import pytest

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import get_engine
from twat_search.web.engines.plugin_search import PluginSearchEngine, SearchPluginSpec, parse_plugin_specs
from twat_search.web.exceptions import EngineError


def test_plugin_search_engine_is_registered() -> None:
    """Template plugin search is available through the shared registry."""
    engine = get_engine("plugin_search", EngineConfig(enabled=True))

    assert isinstance(engine, PluginSearchEngine)


def test_parse_plugin_specs_rejects_invalid_shape() -> None:
    """Plugin specs must be a list of validated plugin objects."""
    with pytest.raises(EngineError, match="must be a list"):
        parse_plugin_specs({"code": "bad"})


def test_plugin_spec_rejects_unknown_template_fields() -> None:
    """Template plugins fail fast when a field is not supported."""
    with pytest.raises(EngineError, match="Unsupported search plugin template fields"):
        parse_plugin_specs(
            [
                {
                    "code": "bad",
                    "name": "Bad plugin",
                    "url_template": "https://example.com/search?q={unknown}",
                },
            ],
        )


@pytest.mark.asyncio
async def test_plugin_search_expands_configured_url_templates() -> None:
    """Configured URL templates become normalized search results."""
    engine = PluginSearchEngine(
        EngineConfig(
            enabled=True,
            default_params={
                "plugins": [
                    {
                        "code": "docs",
                        "name": "Docs",
                        "url_template": "https://example.com/search?q={query_url}",
                        "title_template": "Docs: {query}",
                        "snippet_template": "Search docs for {query}",
                    },
                ],
            },
        ),
    )

    results = await engine.search("font tools")

    assert len(results) == 1
    assert results[0].title == "Docs: font tools"
    assert str(results[0].url) == "https://example.com/search?q=font+tools"
    assert results[0].snippet == "Search docs for font tools"
    assert results[0].source == "plugin_search:docs"
    assert results[0].raw is not None
    assert results[0].raw["rendered_query"] == "font tools"


@pytest.mark.asyncio
async def test_plugin_search_supports_dork_style_query_templates() -> None:
    """Plugin query templates can borrow GitHub dork-style query expansion."""
    engine = PluginSearchEngine(
        EngineConfig(enabled=True),
        plugins=[
            SearchPluginSpec(
                code="github-env",
                name="GitHub env files",
                query_template="{query} filename:.env",
                url_template="https://github.com/search?q={query_url}&type=code",
                title_template="{plugin_name}: {query}",
            ),
        ],
    )

    results = await engine.search("twat-search")

    assert str(results[0].url) == "https://github.com/search?q=twat-search+filename%3A.env&type=code"
    assert results[0].title == "GitHub env files: twat-search filename:.env"


@pytest.mark.asyncio
async def test_plugin_search_limits_results_and_skips_disabled_plugins() -> None:
    """Plugin search respects num_results and per-plugin enabled flags."""
    plugins: list[dict[str, Any]] = [
        {
            "code": "one",
            "name": "One",
            "url_template": "https://example.com/one?q={query_url}",
        },
        {
            "code": "disabled",
            "name": "Disabled",
            "enabled": False,
            "url_template": "https://example.com/disabled?q={query_url}",
        },
        {
            "code": "two",
            "name": "Two",
            "url_template": "https://example.com/two?q={query_url}",
        },
    ]
    engine = PluginSearchEngine(EngineConfig(enabled=True), plugins=plugins, num_results=1)

    results = await engine.search("query")

    assert [result.source for result in results] == ["plugin_search:one"]
