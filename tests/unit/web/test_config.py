#!/usr/bin/env python
# this_file: tests/unit/web/test_config.py
"""
Unit tests for the twat_search.web.config module.

This module tests the configuration classes used for search engine settings.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from twat_search.web.config import (
    Config,
    DEFAULT_CONFIG,
    ENV_VAR_MAP,
    MULTI_PATH_ENV_VARS,
    EngineConfig,
    LLMConfig,
    ProxyConfig,
)
from twat_search.web.provider_catalog import get_provider_metadata, list_provider_metadata

if TYPE_CHECKING:
    from pytest import MonkeyPatch


def test_engine_config_defaults() -> None:
    """Test EngineConfig with default values."""
    config = EngineConfig()

    assert config.api_key is None
    assert config.enabled is True
    assert config.default_params == {}


def test_engine_config_values() -> None:
    """Test EngineConfig with custom values."""
    config = EngineConfig(
        api_key="test_key",
        enabled=False,
        default_params={"count": 10, "include_domains": ["example.com"]},
    )

    assert config.api_key == "test_key"
    assert config.enabled is False
    assert config.default_params == {"count": 10, "include_domains": ["example.com"]}


def test_config_defaults(isolate_env_vars: None) -> None:
    """Test Config with default values."""
    config = Config()

    assert isinstance(config.engines, dict)
    assert len(config.engines) == 0


def test_config_with_env_vars(monkeypatch: MonkeyPatch, env_vars_for_brave: None) -> None:
    """Test Config loads settings from environment variables."""
    # Create config
    config = Config()

    # Check the brave engine was configured
    assert "brave" in config.engines
    brave_config = config.engines["brave"]
    assert brave_config.api_key == "test_brave_key"
    assert brave_config.enabled is True
    assert brave_config.default_params == {"count": 10}


def test_default_config_is_catalog_backed() -> None:
    """Default engine config is generated from implemented provider metadata."""
    implemented_codes = {provider.code for provider in list_provider_metadata(include_planned=False)}

    assert set(DEFAULT_CONFIG["engines"]) == implemented_codes
    assert "aisearch" in DEFAULT_CONFIG["engines"]
    assert "apify" in DEFAULT_CONFIG["engines"]
    assert "serper" in DEFAULT_CONFIG["engines"]
    assert "google_cse" in DEFAULT_CONFIG["engines"]
    assert "dataforseo" in DEFAULT_CONFIG["engines"]
    assert "exa" in DEFAULT_CONFIG["engines"]
    assert "firecrawl" in DEFAULT_CONFIG["engines"]
    assert "jina" in DEFAULT_CONFIG["engines"]
    assert "search1api" in DEFAULT_CONFIG["engines"]
    assert (
        DEFAULT_CONFIG["engines"]["duckduckgo"]["default_params"]
        == get_provider_metadata(
            "duckduckgo",
        ).default_params
    )
    assert DEFAULT_CONFIG["engines"]["brave"]["engine_code"] == "brave"


def test_env_var_map_is_catalog_backed() -> None:
    """Engine env-var mapping includes generated key, enabled, and params paths."""
    multi_path_map = dict(MULTI_PATH_ENV_VARS)

    assert multi_path_map["BRAVE_API_KEY"] == [
        ["engines", "brave", "api_key"],
        ["engines", "brave_news", "api_key"],
    ]
    assert ENV_VAR_MAP["BRAVE_ENABLED"] == ["engines", "brave", "enabled"]
    assert ENV_VAR_MAP["BRAVE_DEFAULT_PARAMS"] == ["engines", "brave", "default_params"]
    assert ENV_VAR_MAP["AISEARCH_API_KEY"] == ["engines", "aisearch", "api_key"]
    assert ENV_VAR_MAP["APIFY_API_KEY"] == ["engines", "apify", "api_key"]
    assert ENV_VAR_MAP["GOOGLE_SERPAPI_DEFAULT_PARAMS"] == [
        "engines",
        "google_serpapi",
        "default_params",
    ]
    assert ENV_VAR_MAP["GOOGLE_CSE_API_KEY"] == ["engines", "google_cse", "api_key"]
    assert ENV_VAR_MAP["DATAFORSEO_API_KEY"] == ["engines", "dataforseo", "api_key"]
    assert ENV_VAR_MAP["EXAAI_API_KEY"] == ["engines", "exa", "api_key"]
    assert ENV_VAR_MAP["FIRECRAWL_API_KEY"] == ["engines", "firecrawl", "api_key"]
    assert ENV_VAR_MAP["JINA_API_KEY"] == ["engines", "jina", "api_key"]
    assert ENV_VAR_MAP["SEARCH1API_KEY"] == ["engines", "search1api", "api_key"]
    assert ENV_VAR_MAP["SERPER_API_KEY"] == ["engines", "serper", "api_key"]


def test_config_with_direct_initialization() -> None:
    """Test Config can be initialized directly with engines."""
    custom_config = Config(
        engines={"test_engine": EngineConfig(api_key="direct_key", enabled=True, default_params={"count": 5})},
    )

    assert "test_engine" in custom_config.engines
    assert custom_config.engines["test_engine"].api_key == "direct_key"
    assert custom_config.engines["test_engine"].default_params == {"count": 5}


def test_config_env_vars_override_direct_config(monkeypatch: MonkeyPatch) -> None:
    """Test environment variables do not override direct config."""
    # Set environment variables
    monkeypatch.setenv("BRAVE_API_KEY", "env_key")

    # Create config with direct values (should take precedence)
    custom_config = Config(
        engines={"brave": EngineConfig(api_key="direct_key", enabled=True, default_params={"count": 5})},
    )

    # Check that direct config was not overridden
    assert custom_config.engines["brave"].api_key == "direct_key"


def test_proxy_config_builds_webshare_url() -> None:
    """Test Webshare-style proxy URL construction."""
    config = ProxyConfig(
        enabled=True,
        username="user name",
        password="p@ss word",  # noqa: S106
        host="p.webshare.io",
        port=80,
    )

    assert config.is_configured() is True
    assert config.httpx_proxy_url() == "http://user%20name:p%40ss%20word@p.webshare.io:80"
    assert config.redacted_url() == "http://user%20name:****@p.webshare.io:80"


def test_proxy_config_builds_playwright_shape() -> None:
    """Test Playwright proxy dict construction."""
    config = ProxyConfig(
        enabled=True,
        username="user",
        password="pass",  # noqa: S106
        host="p.webshare.io",
        port="80",
    )

    assert config.playwright_proxy() == {
        "server": "http://p.webshare.io:80",
        "username": "user",
        "password": "pass",
    }


def test_config_loads_proxy_env(monkeypatch: MonkeyPatch) -> None:
    """Test Config loads shared proxy settings from environment variables."""
    monkeypatch.delenv("_TEST_ENGINE", raising=False)
    monkeypatch.setenv("TWAT_SEARCH_PROXY_ENABLED", "true")
    monkeypatch.setenv("WEBSHARE_PROXY_USER", "user")
    monkeypatch.setenv("WEBSHARE_PROXY_PASS", "pass")
    monkeypatch.setenv("WEBSHARE_DOMAIN_NAME", "p.webshare.io")
    monkeypatch.setenv("WEBSHARE_PROXY_PORT", "80")

    config = Config()

    assert config.proxies.enabled is True
    assert config.proxies.httpx_proxy_url() == "http://user:pass@p.webshare.io:80"


def test_llm_config_requires_enabled_model_and_key() -> None:
    """Test LLM config readiness guard."""
    assert LLMConfig(enabled=True, model="gpt-5-mini", api_key="key").is_configured() is True
    assert LLMConfig(enabled=False, model="gpt-5-mini", api_key="key").is_configured() is False
    assert LLMConfig(enabled=True, model=None, api_key="key").is_configured() is False
