#!/usr/bin/env python
# this_file: tests/unit/web/test_routes.py
"""Unit tests for catalog-backed route selection."""

from __future__ import annotations

import pytest

from twat_search.web.config import Config, EngineConfig
from twat_search.web.routes import explain_route_selection, get_route_policy, route_names, select_route_engines


def _route_config() -> Config:
    return Config(
        engines={
            "brave": EngineConfig(enabled=True, api_key="brave-key"),
            "brave_news": EngineConfig(enabled=True, api_key="brave-key"),
            "exa": EngineConfig(enabled=True, api_key="exa-key"),
            "tavily": EngineConfig(enabled=True, api_key="tavily-key"),
            "you": EngineConfig(enabled=True, api_key="you-key"),
            "duckduckgo": EngineConfig(enabled=True),
            "google_serpapi": EngineConfig(enabled=True, api_key=None),
            "google_browser": EngineConfig(enabled=True),
            "plugin_search": EngineConfig(enabled=True),
        },
    )


def test_best_route_selects_configured_available_engines() -> None:
    """Best route selects configured engines by provider route priority."""
    engines = select_route_engines(
        config=_route_config(),
        route="best",
        available_engines={"brave", "duckduckgo", "exa", "tavily", "you"},
    )

    assert engines == ["brave", "exa", "tavily"]


def test_api_only_route_skips_missing_api_keys() -> None:
    """API-only route uses configured API providers and skips missing keys."""
    engines = select_route_engines(
        config=_route_config(),
        route="api-only",
        available_engines={"brave", "duckduckgo", "google_serpapi"},
    )

    assert engines == ["brave"]


def test_route_selection_explains_skipped_engines() -> None:
    """Route selection returns typed reasons for skipped providers."""
    selection = explain_route_selection(
        config=_route_config(),
        route="api-only",
        available_engines={"brave", "duckduckgo", "google_serpapi"},
    )

    assert selection.selected_engines == ["brave"]
    assert selection.policy.model_dump()["name"] == "api-only"
    assert selection.policy.model_dump()["transports"] == ("api",)
    skipped = {decision.engine: decision.reason for decision in selection.skipped}
    assert skipped["duckduckgo"] == "transport"
    assert skipped["google_serpapi"] == "missing_api_key"


def test_browser_route_selects_browser_engines() -> None:
    """Browser route selects browser-backed engines when available."""
    engines = select_route_engines(
        config=_route_config(),
        route="browser",
        available_engines={"google_browser", "duckduckgo"},
    )

    assert engines == ["google_browser"]


def test_browser_route_normalizes_useful_legacy_aliases() -> None:
    """Useful legacy aliases resolve to canonical browser provider codes."""
    engines = select_route_engines(
        config=_route_config(),
        route="browser",
        available_engines={"google_falla"},
    )

    assert engines == ["google_browser"]


def test_unknown_route_raises_helpful_error() -> None:
    """Unknown route names fail loudly."""
    with pytest.raises(ValueError, match="Unknown search route"):
        get_route_policy("slow-and-pricey")


def test_route_policy_normalizes_underscore_names() -> None:
    """Route lookup accepts CLI-friendly underscore aliases."""
    policy = get_route_policy("api_only")

    assert policy.name == "api-only"
    assert policy.model_dump()["include_keyed"] is True


def test_route_names_include_public_presets() -> None:
    """Route name list exposes supported public presets."""
    assert {"best", "fast", "cheap", "resilient", "deep", "browser", "api-only", "plugins", "all"}.issubset(
        set(route_names()),
    )


def test_plugins_route_selects_plugin_engines() -> None:
    """Plugin route selects configured plugin adapters."""
    engines = select_route_engines(
        config=_route_config(),
        route="plugins",
        available_engines={"plugin_search", "brave"},
    )

    assert engines == ["plugin_search"]
