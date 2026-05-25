#!/usr/bin/env python
# this_file: tests/unit/web/test_provider_catalog.py
"""Unit tests for provider metadata catalog."""

from __future__ import annotations

from twat_search.web.engine_constants import ALL_POSSIBLE_ENGINES, ENGINE_FRIENDLY_NAMES
from twat_search.web.engines.base import get_engine_registry
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
    assert "google_browser" in codes
    assert "serper" in codes
    assert "dataforseo" in codes
    assert "github_search" in codes
    assert "plugin_search" in codes
    assert "langsearch" in codes
    assert "mapleserp" in codes
    assert "brightdata" in codes


def test_catalog_can_filter_planned_providers() -> None:
    """Implemented-provider listing excludes planned providers."""
    implemented = list_known_provider_codes(include_planned=False)

    assert "brave" in implemented
    assert "serper" in implemented
    assert "dataforseo" in implemented
    assert "exa" in implemented
    assert "firecrawl" in implemented
    assert "github_search" in implemented
    assert "jina" in implemented
    assert "langsearch" in implemented
    assert "mapleserp" in implemented
    assert "search1api" in implemented
    assert "search_cans" in implemented
    assert "gensee" in implemented
    assert "apify" in implemented
    assert "plugin_search" in implemented


def test_provider_metadata_captures_transport_and_proxy_support() -> None:
    """Provider metadata exposes routing-relevant capabilities."""
    brave = get_provider_metadata("brave")
    google_browser = get_provider_metadata("google-falla")

    assert brave is not None
    assert brave.transport == "api"
    assert brave.requires_api_key is True
    assert brave.proxy_support is False
    assert brave.route_priority == 10

    assert google_browser is not None
    assert google_browser.transport == "browser"
    assert google_browser.browser_required is True
    assert google_browser.proxy_support is True
    assert google_browser.route_priority == 300
    assert google_browser.code == "google_browser"
    assert "google_falla" in google_browser.aliases


def test_provider_metadata_exposes_env_names() -> None:
    """API-key environment names come from provider metadata."""
    assert get_api_key_env_names("brave") == ("BRAVE_API_KEY",)
    assert get_api_key_env_names("pplx") == ("PPLX_API_KEY", "PERPLEXITY_API_KEY")
    assert get_api_key_env_names("duckduckgo") == ()


def test_registry_entries_attach_provider_metadata() -> None:
    """Registered engine classes are exposed through typed provider metadata records."""
    registry = get_engine_registry()
    entry = registry["brave"]

    assert entry.code == "brave"
    assert entry.engine_class.engine_code == "brave"
    assert entry.provider_metadata is get_provider_metadata("brave")
    assert entry.catalog_status == "cataloged"
    assert entry.friendly_name == "Brave Search API"
    assert entry.env_api_key_names == ("BRAVE_API_KEY",)
    assert entry.transport == "api"
    assert entry.proxy_policy == "none"


def test_engine_constants_are_catalog_backed() -> None:
    """Engine constants expose canonical provider metadata."""
    assert ALL_POSSIBLE_ENGINES == list_known_provider_codes(include_planned=True)
    assert ENGINE_FRIENDLY_NAMES["brave"] == get_friendly_name("brave")
    assert ENGINE_FRIENDLY_NAMES["serper"] == "Serper Google Search API"
    assert "google_falla" not in ALL_POSSIBLE_ENGINES


def test_catalog_entries_have_unique_codes() -> None:
    """Provider codes are unique and match their dictionary keys."""
    providers = list_provider_metadata()
    codes = [provider.code for provider in providers]

    assert len(codes) == len(set(codes))
    assert codes == sorted(codes)


def test_browser_provider_has_derived_browser_and_proxy_policy() -> None:
    """Browser providers derive Playwright proxy and browser defaults."""
    google_browser = get_provider_metadata("google_browser")

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
    brightdata = get_provider_metadata("brightdata")
    langsearch = get_provider_metadata("langsearch")
    mapleserp = get_provider_metadata("mapleserp")
    search_cans = get_provider_metadata("search_cans")
    plugin_search = get_provider_metadata("plugin_search")

    assert serper is not None
    assert serper.status == "implemented"
    assert serper.planned is False
    assert gensee is not None
    assert gensee.status == "implemented"
    assert gensee.planned is False
    assert gensee.env_api_key_names == ("GENSEE_SEARCH_API_KEY",)
    assert brightdata is not None
    assert brightdata.status == "planned"
    assert brightdata.proxy_policy == "recommended"
    assert brightdata.proxy_transports == ("httpx", "playwright")
    assert langsearch is not None
    assert langsearch.status == "implemented"
    assert langsearch.env_api_key_names == ("LANGSEARCH_API_KEY",)
    assert mapleserp is not None
    assert mapleserp.status == "implemented"
    assert mapleserp.env_api_key_names == ("MAPLESERP_API_KEY",)
    assert search_cans is not None
    assert search_cans.status == "implemented"
    assert search_cans.env_api_key_names == ("SEARCH_CANS_API_KEY",)
    assert plugin_search is not None
    assert plugin_search.status == "implemented"
    assert plugin_search.transport == "plugin"
    assert plugin_search.default_enabled is False


def test_select_provider_codes_filters_catalog() -> None:
    """Provider selection supports route preset building."""
    free_no_key = select_provider_codes(cost_class="free", requires_api_key=False)
    browser_proxy = select_provider_codes(transport="browser", proxy_support=True)

    assert "duckduckgo" in free_no_key
    assert "brave" not in free_no_key
    assert "google_browser" in browser_proxy
    assert "browser_use" not in browser_proxy
