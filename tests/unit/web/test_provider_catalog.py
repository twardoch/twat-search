#!/usr/bin/env python
# this_file: tests/unit/web/test_provider_catalog.py
"""Unit tests for provider metadata catalog."""

from __future__ import annotations

from twat_search.web.engine_constants import ALL_POSSIBLE_ENGINES, ENGINE_FRIENDLY_NAMES
from twat_search.web.provider_catalog import (
    get_api_key_env_names,
    get_friendly_name,
    get_provider_metadata,
    list_known_provider_codes,
    list_provider_metadata,
    select_provider_codes,
)


def test_catalog_contains_current_and_planned_providers() -> None:
    """Catalog contains both implemented engines and 2.0 target providers."""
    codes = list_known_provider_codes()

    assert "brave" in codes
    assert "google_falla" in codes
    assert "serper" in codes
    assert "dataforseo" in codes
    assert "github_search" in codes


def test_catalog_can_filter_planned_providers() -> None:
    """Implemented-provider listing excludes planned providers."""
    implemented = list_known_provider_codes(include_planned=False)

    assert "brave" in implemented
    assert "serper" in implemented
    assert "dataforseo" in implemented
    assert "exa" in implemented
    assert "firecrawl" in implemented
    assert "jina" in implemented
    assert "search1api" in implemented
    assert "apify" in implemented
    assert "gensee" not in implemented


def test_provider_metadata_captures_transport_and_proxy_support() -> None:
    """Provider metadata exposes routing-relevant capabilities."""
    brave = get_provider_metadata("brave")
    google_browser = get_provider_metadata("google-falla")

    assert brave is not None
    assert brave.transport == "api"
    assert brave.requires_api_key is True
    assert brave.proxy_support is False

    assert google_browser is not None
    assert google_browser.transport == "browser"
    assert google_browser.browser_required is True
    assert google_browser.proxy_support is True


def test_provider_metadata_exposes_env_names() -> None:
    """API-key environment names come from provider metadata."""
    assert get_api_key_env_names("brave") == ("BRAVE_API_KEY",)
    assert get_api_key_env_names("pplx") == ("PPLX_API_KEY", "PERPLEXITY_API_KEY")
    assert get_api_key_env_names("duckduckgo") == ()


def test_engine_constants_are_catalog_backed() -> None:
    """Legacy constants stay compatible while using provider metadata."""
    assert ALL_POSSIBLE_ENGINES == list_known_provider_codes(include_planned=True)
    assert ENGINE_FRIENDLY_NAMES["brave"] == get_friendly_name("brave")
    assert ENGINE_FRIENDLY_NAMES["serper"] == "Serper Google Search API"


def test_catalog_entries_have_unique_codes() -> None:
    """Provider codes are unique and match their dictionary keys."""
    providers = list_provider_metadata()
    codes = [provider.code for provider in providers]

    assert len(codes) == len(set(codes))
    assert codes == sorted(codes)


def test_browser_provider_has_derived_browser_and_proxy_policy() -> None:
    """Browser providers derive Playwright proxy and browser defaults."""
    google_browser = get_provider_metadata("google_falla")

    assert google_browser is not None
    assert google_browser.status == "implemented"
    assert google_browser.proxy_policy == "optional"
    assert google_browser.proxy_transports == ("playwright", "httpx")
    assert google_browser.browser_policy is not None
    assert google_browser.browser_policy.headless_default is True


def test_provider_status_replaces_boolean_source_of_truth() -> None:
    """Planned providers use status while preserving the planned property."""
    serper = get_provider_metadata("serper")
    gensee = get_provider_metadata("gensee")

    assert serper is not None
    assert serper.status == "implemented"
    assert serper.planned is False
    assert gensee is not None
    assert gensee.status == "planned"
    assert gensee.planned is True


def test_select_provider_codes_filters_catalog() -> None:
    """Provider selection supports route preset building."""
    free_no_key = select_provider_codes(cost_class="free", requires_api_key=False)
    browser_proxy = select_provider_codes(transport="browser", proxy_support=True)

    assert "duckduckgo" in free_no_key
    assert "brave" not in free_no_key
    assert "google_falla" in browser_proxy
    assert "browser_use" not in browser_proxy
