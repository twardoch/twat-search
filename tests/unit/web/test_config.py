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
    assert "github_search" in DEFAULT_CONFIG["engines"]
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
    assert ENV_VAR_MAP["GENSEE_SEARCH_API_KEY"] == ["engines", "gensee", "api_key"]
    assert ENV_VAR_MAP["GITHUB_API_TOKEN"] == ["engines", "github_search", "api_key"]
    assert ENV_VAR_MAP["JINA_API_KEY"] == ["engines", "jina", "api_key"]
    assert ENV_VAR_MAP["LANGSEARCH_API_KEY"] == ["engines", "langsearch", "api_key"]
    assert ENV_VAR_MAP["MAPLESERP_API_KEY"] == ["engines", "mapleserp", "api_key"]
    assert ENV_VAR_MAP["SEARCH1API_KEY"] == ["engines", "search1api", "api_key"]
    assert ENV_VAR_MAP["SEARCH_CANS_API_KEY"] == ["engines", "search_cans", "api_key"]
    assert ENV_VAR_MAP["SERPER_API_KEY"] == ["engines", "serper", "api_key"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_QUERY_REWRITE"] == ["llm", "query_rewrite"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_QUERY_DECOMPOSITION"] == ["llm", "query_decomposition"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_DECOMPOSITION_MAX_QUERIES"] == ["llm", "decomposition_max_queries"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_RESULT_RERANK"] == ["llm", "result_rerank"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_RERANK_TOP_N"] == ["llm", "rerank_top_n"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_ANSWER_SYNTHESIS"] == ["llm", "answer_synthesis"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_SYNTHESIS_TOP_N"] == ["llm", "synthesis_top_n"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_TEMPERATURE"] == ["llm", "temperature"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_MAX_TOKENS"] == ["llm", "max_tokens"]
    assert ENV_VAR_MAP["TWAT_SEARCH_LLM_SYSTEM_PROMPT"] == ["llm", "system_prompt"]


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
    assert config.http_request_kwargs() == {
        "proxy_url": "http://user%20name:p%40ss%20word@p.webshare.io:80",
        "timeout": 30.0,
        "retries": 3,
        "retry_delay": 0.5,
        "min_delay": 0.1,
    }


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
    monkeypatch.setenv("TWAT_SEARCH_PROXY_TIMEOUT", "45")
    monkeypatch.setenv("TWAT_SEARCH_PROXY_RETRIES", "4")
    monkeypatch.setenv("TWAT_SEARCH_PROXY_RETRY_DELAY", "0.25")
    monkeypatch.setenv("TWAT_SEARCH_PROXY_MIN_DELAY", "0.05")
    monkeypatch.setenv("TWAT_SEARCH_PROXY_MAX_PARALLELISM", "8")

    config = Config()

    assert config.proxies.enabled is True
    assert config.proxies.httpx_proxy_url() == "http://user:pass@p.webshare.io:80"
    assert config.proxies.timeout == 45
    assert config.proxies.retries == 4
    assert config.proxies.retry_delay == 0.25
    assert config.proxies.min_delay == 0.05
    assert config.proxies.max_parallelism == 8


def test_llm_config_requires_enabled_model_and_key() -> None:
    """Test LLM config readiness guard."""
    assert (
        LLMConfig(
            enabled=True,
            model="gpt-5-mini",
            api_key="key",
            base_url="https://llm.example/v1",
        ).is_configured()
        is True
    )
    assert (
        LLMConfig(
            enabled=False,
            model="gpt-5-mini",
            api_key="key",
            base_url="https://llm.example/v1",
        ).is_configured()
        is False
    )
    assert LLMConfig(enabled=True, model=None, api_key="key", base_url="https://llm.example/v1").is_configured() is False
    assert LLMConfig(enabled=True, model="gpt-5-mini", api_key="key", base_url=None).is_configured() is False


def test_config_loads_llm_env(monkeypatch: MonkeyPatch) -> None:
    """Test Config loads optional LLM search-stage settings from environment variables."""
    monkeypatch.delenv("_TEST_ENGINE", raising=False)
    monkeypatch.setenv("TWAT_SEARCH_LLM_ENABLED", "true")
    monkeypatch.setenv("TWAT_SEARCH_LLM_QUERY_REWRITE", "true")
    monkeypatch.setenv("TWAT_SEARCH_LLM_RESULT_RERANK", "true")
    monkeypatch.setenv("TWAT_SEARCH_LLM_RERANK_TOP_N", "12")
    monkeypatch.setenv("TWAT_SEARCH_LLM_ANSWER_SYNTHESIS", "true")
    monkeypatch.setenv("TWAT_SEARCH_LLM_SYNTHESIS_TOP_N", "5")
    monkeypatch.setenv("TWAT_SEARCH_LLM_PROVIDER", "openai-compatible")
    monkeypatch.setenv("TWAT_SEARCH_LLM_MODEL", "gpt-test")
    monkeypatch.setenv("TWAT_SEARCH_LLM_API_KEY", "llm-key")
    monkeypatch.setenv("TWAT_SEARCH_LLM_BASE_URL", "https://llm.example/v1")
    monkeypatch.setenv("TWAT_SEARCH_LLM_TEMPERATURE", "0.1")
    monkeypatch.setenv("TWAT_SEARCH_LLM_MAX_TOKENS", "96")
    monkeypatch.setenv("TWAT_SEARCH_LLM_SYSTEM_PROMPT", "Rewrite only.")

    config = Config()

    assert config.llm.enabled is True
    assert config.llm.query_rewrite is True
    assert config.llm.result_rerank is True
    assert config.llm.rerank_top_n == 12
    assert config.llm.answer_synthesis is True
    assert config.llm.synthesis_top_n == 5
    assert config.llm.provider == "openai-compatible"
    assert config.llm.model == "gpt-test"
    assert config.llm.api_key == "llm-key"
    assert config.llm.base_url == "https://llm.example/v1"
    assert config.llm.temperature == 0.1
    assert config.llm.max_tokens == 96
    assert config.llm.system_prompt == "Rewrite only."
