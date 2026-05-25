#!/usr/bin/env python
# this_file: tests/unit/web/test_routes.py
"""Unit tests for catalog-backed route selection."""

from __future__ import annotations

import pytest

from twat_search.web.config import Config, EngineConfig
from twat_search.web.routes import get_route_policy, route_names, select_route_engines


def _route_config() -> Config:
    return Config(
        engines={
            "brave": EngineConfig(enabled=True, api_key="brave-key"),
            "brave_news": EngineConfig(enabled=True, api_key="brave-key"),
            "duckduckgo": EngineConfig(enabled=True),
            "google_serpapi": EngineConfig(enabled=True, api_key=None),
            "google_falla": EngineConfig(enabled=True),
        },
    )


def test_best_route_selects_configured_available_engines() -> None:
    """Best route only selects implemented, enabled, available, credentialed engines."""
    engines = select_route_engines(
        config=_route_config(),
        route="best",
        available_engines={"brave", "duckduckgo", "google_serpapi", "google_falla"},
    )

    assert engines == ["brave"]


def test_api_only_route_skips_missing_api_keys() -> None:
    """API-only route uses configured API providers and skips missing keys."""
    engines = select_route_engines(
        config=_route_config(),
        route="api-only",
        available_engines={"brave", "duckduckgo", "google_serpapi"},
    )

    assert engines == ["brave"]


def test_browser_route_selects_browser_engines() -> None:
    """Browser route selects browser-backed engines when available."""
    engines = select_route_engines(
        config=_route_config(),
        route="browser",
        available_engines={"google_falla", "duckduckgo"},
    )

    assert engines == ["google_falla"]


def test_unknown_route_raises_helpful_error() -> None:
    """Unknown route names fail loudly."""
    with pytest.raises(ValueError, match="Unknown search route"):
        get_route_policy("slow-and-pricey")


def test_route_names_include_public_presets() -> None:
    """Route name list exposes supported public presets."""
    assert {"best", "fast", "cheap", "resilient", "deep", "browser", "api-only", "all"}.issubset(
        set(route_names()),
    )
