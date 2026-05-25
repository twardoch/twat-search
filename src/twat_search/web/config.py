# this_file: src/twat_search/web/config.py
"""
Configuration management for the web search module.

This module handles loading and managing configuration for the web search API.
It supports loading from environment variables, a configuration file, or explicit parameters.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, ClassVar
from urllib.parse import quote

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

from twat_search.web.engines.base import get_registered_engines  # Added import
from twat_search.web.provider_catalog import list_provider_metadata

# Load environment variables from .env file if present
load_dotenv()

# Initialize logger
logger = logging.getLogger(__name__)


def _build_default_config() -> dict[str, dict[str, Any]]:
    """Build default config from implemented provider metadata."""
    return {
        "engines": {
            provider.code: {
                "enabled": provider.default_enabled,
                "api_key": None,
                "default_params": provider.default_params,
                "engine_code": provider.code,
            }
            for provider in list_provider_metadata(include_planned=False)
        },
    }


DEFAULT_CONFIG: dict[str, dict[str, Any]] = _build_default_config()


BASE_ENV_VAR_MAP: dict[str, str | list[str]] = {
    # General
    "TWAT_SEARCH_LOG_LEVEL": "log_level",
    # Shared proxy configuration
    "TWAT_SEARCH_PROXY_ENABLED": ["proxies", "enabled"],
    "TWAT_SEARCH_PROXY_URL": ["proxies", "url"],
    "TWAT_SEARCH_PROXY_PROVIDER": ["proxies", "provider"],
    "WEBSHARE_PROXY_USER": ["proxies", "username"],
    "WEBSHARE_PROXY_PASS": ["proxies", "password"],
    "WEBSHARE_DOMAIN_NAME": ["proxies", "host"],
    "WEBSHARE_PROXY_PORT": ["proxies", "port"],
    "TWAT_SEARCH_PROXY_TIMEOUT": ["proxies", "timeout"],
    "TWAT_SEARCH_PROXY_RETRIES": ["proxies", "retries"],
    "TWAT_SEARCH_PROXY_RETRY_DELAY": ["proxies", "retry_delay"],
    "TWAT_SEARCH_PROXY_MIN_DELAY": ["proxies", "min_delay"],
    "TWAT_SEARCH_PROXY_MAX_PARALLELISM": ["proxies", "max_parallelism"],
    # Shared LLM routing configuration
    "TWAT_SEARCH_LLM_PROVIDER": ["llm", "provider"],
    "TWAT_SEARCH_LLM_MODEL": ["llm", "model"],
    "TWAT_SEARCH_LLM_API_KEY": ["llm", "api_key"],
    "TWAT_SEARCH_LLM_BASE_URL": ["llm", "base_url"],
    "TWAT_SEARCH_LLM_ENABLED": ["llm", "enabled"],
    "TWAT_SEARCH_LLM_QUERY_REWRITE": ["llm", "query_rewrite"],
    "TWAT_SEARCH_LLM_QUERY_DECOMPOSITION": ["llm", "query_decomposition"],
    "TWAT_SEARCH_LLM_DECOMPOSITION_MAX_QUERIES": ["llm", "decomposition_max_queries"],
    "TWAT_SEARCH_LLM_RESULT_RERANK": ["llm", "result_rerank"],
    "TWAT_SEARCH_LLM_RERANK_TOP_N": ["llm", "rerank_top_n"],
    "TWAT_SEARCH_LLM_ANSWER_SYNTHESIS": ["llm", "answer_synthesis"],
    "TWAT_SEARCH_LLM_SYNTHESIS_TOP_N": ["llm", "synthesis_top_n"],
    "TWAT_SEARCH_LLM_TEMPERATURE": ["llm", "temperature"],
    "TWAT_SEARCH_LLM_MAX_TOKENS": ["llm", "max_tokens"],
    "TWAT_SEARCH_LLM_SYSTEM_PROMPT": ["llm", "system_prompt"],
}


def _build_env_var_maps() -> tuple[dict[str, str | list[str]], list[tuple[str, list[list[str]]]]]:
    """Build environment-variable mappings from provider metadata."""
    env_var_map = dict(BASE_ENV_VAR_MAP)
    multi_paths: dict[str, list[list[str]]] = {}

    for provider in list_provider_metadata(include_planned=False):
        prefix = provider.code.upper()
        env_var_map[f"{prefix}_ENABLED"] = ["engines", provider.code, "enabled"]
        env_var_map[f"{prefix}_DEFAULT_PARAMS"] = ["engines", provider.code, "default_params"]
        for env_name in provider.env_api_key_names:
            multi_paths.setdefault(env_name, []).append(["engines", provider.code, "api_key"])

    simple_multi_paths = []
    for env_name, paths in multi_paths.items():
        if len(paths) == 1:
            env_var_map[env_name] = paths[0]
        else:
            simple_multi_paths.append((env_name, paths))

    return env_var_map, simple_multi_paths


ENV_VAR_MAP, MULTI_PATH_ENV_VARS = _build_env_var_maps()


# Type definitions
class ProxyConfig(BaseModel):
    """Configuration for shared HTTP and browser proxy usage."""

    enabled: bool = False
    provider: str = "webshare"
    url: str | None = None
    username: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | str | None = None
    timeout: float = 30.0
    retries: int = 3
    retry_delay: float = 0.5
    min_delay: float = 0.1
    max_parallelism: int = 6

    def is_configured(self) -> bool:
        """Return True when either a full URL or all proxy parts are present."""
        return self.url is not None or all([self.username, self.password, self.host, self.port])

    def build_url(self) -> str | None:
        """Build an HTTP proxy URL from explicit URL or Webshare-style parts."""
        if self.url:
            return self.url
        if not all([self.username, self.password, self.host, self.port]):
            return None
        user = quote(str(self.username), safe="")
        password = quote(str(self.password), safe="")
        return f"http://{user}:{password}@{self.host}:{self.port}"

    def httpx_proxy_url(self) -> str | None:
        """Return the proxy URL to pass to HTTPX clients."""
        if not self.enabled:
            return None
        return self.build_url()

    def http_request_kwargs(self) -> dict[str, float | int | str]:
        """Return proxy-aware HTTP request overrides for shared engines."""
        proxy_url = self.httpx_proxy_url()
        if not proxy_url:
            return {}
        return {
            "proxy_url": proxy_url,
            "timeout": self.timeout,
            "retries": self.retries,
            "retry_delay": self.retry_delay,
            "min_delay": self.min_delay,
        }

    def playwright_proxy(self) -> dict[str, str] | None:
        """Return Playwright's proxy dict shape without leaking credentials."""
        if not self.enabled or not self.host or not self.port:
            return None
        proxy: dict[str, str] = {"server": f"http://{self.host}:{self.port}"}
        if self.username:
            proxy["username"] = self.username
        if self.password:
            proxy["password"] = self.password
        return proxy

    def redacted_url(self) -> str | None:
        """Return a log-safe proxy URL."""
        proxy_url = self.build_url()
        if not proxy_url or not self.password:
            return proxy_url
        return proxy_url.replace(str(self.password), "****").replace(quote(str(self.password), safe=""), "****")


class LLMConfig(BaseModel):
    """Configuration for optional LLM-assisted search stages."""

    enabled: bool = False
    query_rewrite: bool = False
    query_decomposition: bool = False
    decomposition_max_queries: int = 4
    result_rerank: bool = False
    rerank_top_n: int = 20
    answer_synthesis: bool = False
    synthesis_top_n: int = 8
    provider: str | None = None
    model: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    timeout: float = 60.0
    temperature: float = 0.0
    max_tokens: int = 128
    system_prompt: str | None = None

    def is_configured(self) -> bool:
        """Return True when enough data exists to call a model."""
        return bool(self.enabled and self.model and self.api_key and self.base_url)


class EngineConfig(BaseModel):
    """Configuration for a single search engine."""

    enabled: bool = True
    api_key: str | None = None
    default_params: dict[str, Any] = Field(default_factory=dict)
    engine_code: str | None = None  # Added for reference during validation

    def __init__(self, **data: Any) -> None:
        """
        Initialize the engine configuration with API key from environment variables if needed.

        Args:
            **data: Configuration data
        """
        # Call parent init first
        super().__init__(**data)

        # If no API key is provided but we have an engine code, try to get it from environment variables
        if self.api_key is None and self.engine_code:
            logger.debug(f"No API key provided for {self.engine_code}, checking environment variables")
            try:
                engine_class = get_registered_engines().get(self.engine_code)
                if engine_class and hasattr(engine_class, "env_api_key_names") and engine_class.env_api_key_names:
                    logger.debug(
                        f"Engine '{self.engine_code}' requires API key from env vars: {engine_class.env_api_key_names}",
                    )
                    # Try to get API key from environment variables
                    for env_var in engine_class.env_api_key_names:
                        env_value = os.environ.get(env_var)
                        logger.debug(f"Checking env var '{env_var}' in __init__: {env_value is not None}")
                        if env_value:
                            logger.debug(f"Using API key from environment variable '{env_var}'")
                            self.api_key = env_value
                            break
            except (ImportError, AttributeError) as e:
                logger.debug(f"Couldn't check API key requirements for {self.engine_code}: {e}")

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v: str | None, info: Any) -> str | None:
        """
        Validate the API key for the engine.

        If the engine requires an API key (has env_api_key_names), ensure it's set.
        This validator runs during config loading, so we don't have the actual
        engine instance yet - we'll do more thorough validation when creating
        engine instances.
        """
        engine_code = info.data.get("engine_code")
        logger.debug(f"Validating API key for engine '{engine_code}', current value: {v is not None}")

        if engine_code and v is None:
            # We have an engine code but no API key - we'll check in the registry
            # if this engine requires an API key
            try:
                engine_class = get_registered_engines().get(engine_code)
                logger.debug(f"Found engine class for '{engine_code}': {engine_class is not None}")

                # If we found the engine class and it requires an API key,
                # check environment variables
                if engine_class and hasattr(engine_class, "env_api_key_names") and engine_class.env_api_key_names:
                    logger.debug(
                        f"Engine '{engine_code}' requires API key from env vars: {engine_class.env_api_key_names}",
                    )
                    # Try to get API key from environment variables
                    for env_var in engine_class.env_api_key_names:
                        env_value = os.environ.get(env_var)
                        logger.debug(f"Checking env var '{env_var}': {env_value is not None}")
                        if env_value:
                            logger.debug(f"Using API key from environment variable '{env_var}'")
                            return env_value

                    # If we get here, no environment variables were set
                    logger.warning(
                        f"Engine '{engine_code}' may require an API key. "
                        f"Please set one of these environment variables: {', '.join(engine_class.env_api_key_names)}",
                    )
            except (ImportError, AttributeError) as e:
                # Can't access the engine registry yet - this happens during
                # initial import. We'll validate again when creating the engine.
                logger.debug(f"Couldn't check API key requirements for {engine_code}: {e}")

        return v


class Config(BaseModel):
    """Main configuration model for the web search module."""

    engines: dict[str, EngineConfig] = Field(default_factory=dict)
    proxies: ProxyConfig = Field(default_factory=ProxyConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    config_path: ClassVar[str | None] = None

    @classmethod
    def get_config_path(cls) -> Path:
        """
        Determine the configuration file path.

        Checks the following locations in order:
        1. TWAT_SEARCH_CONFIG_PATH environment variable
        2. ~/.twat/search_config.json
        3. ~/.config/twat/search_config.json
        """
        # Get from environment variable if set
        if cls.config_path:
            return Path(cls.config_path)

        env_path = os.environ.get("TWAT_SEARCH_CONFIG_PATH")
        if env_path:
            return Path(env_path)

        # Check ~/.twat/search_config.json
        home_config = Path.home() / ".twat" / "search_config.json"
        if home_config.exists():
            return home_config

        # Check ~/.config/twat/search_config.json
        xdg_config = Path.home() / ".config" / "twat" / "search_config.json"
        if xdg_config.exists():
            return xdg_config

        # Default to ~/.twat/search_config.json (may not exist yet)
        return home_config

    def __init__(self, **data: Any) -> None:
        """
        Initialize configuration with default values and overrides.

        Args:
            **data: Configuration override values
        """
        # Start with default configuration
        config_data = {}

        # Only load default configuration if not in test mode
        if "_TEST_ENGINE" not in os.environ:
            config_data = json.loads(json.dumps(DEFAULT_CONFIG))  # Deep copy

        # Load from config file if it exists
        config_path = self.get_config_path()
        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    file_config = json.load(f)
                self._merge_config(config_data, file_config)
                logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.error(f"Error loading configuration from {config_path}: {e}")

        # Apply environment variable overrides
        _apply_env_overrides(config_data)

        # Apply explicit overrides
        if data:
            self._merge_config(config_data, data)

        # Initialize with the final configuration
        super().__init__(**config_data)

    def _merge_config(self, target: dict[str, Any], source: dict[str, Any]) -> None:
        """
        Recursively merge the source configuration into the target.

        Args:
            target: Target dictionary to merge into
            source: Source dictionary to merge from
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_config(target[key], value)
            else:
                target[key] = value

    def add_engine(
        self,
        engine_name: str,
        enabled: bool = True,
        api_key: str | None = None,
        default_params: dict[str, Any] | None = None,
    ) -> None:
        """
        Add or update an engine configuration.

        Args:
            engine_name: Name of the engine
            enabled: Whether the engine is enabled
            api_key: API key for the engine
            default_params: Default parameters for the engine
        """
        if default_params is None:
            default_params = {}

        if engine_name in self.engines:
            # Update existing engine config
            engine_config = self.engines[engine_name]
            engine_config.enabled = enabled
            if api_key is not None:
                engine_config.api_key = api_key
            engine_config.default_params.update(default_params)
        else:
            # Create new engine config
            self.engines[engine_name] = EngineConfig(
                enabled=enabled,
                api_key=api_key,
                default_params=default_params,
                engine_code=engine_name,
            )


def _apply_env_overrides(config_data: dict[str, Any]) -> None:
    """
    Apply overrides from environment variables to the configuration.

    Args:
        config_data: Configuration data to update
    """
    # Process simple mappings
    for env_var, config_path in ENV_VAR_MAP.items():
        env_value = os.environ.get(env_var)
        if env_value is not None:
            # Handle special cases for boolean/numeric values
            value = _parse_env_value(env_value)

            # Apply the value to the config
            if isinstance(config_path, str):
                # Top-level key
                config_data[config_path] = value
            else:
                # Nested path
                _set_nested_value(config_data, config_path, value)

    # Process multi-path mappings
    for env_var, paths in MULTI_PATH_ENV_VARS:
        env_value = os.environ.get(env_var)
        if env_value is not None:
            value = _parse_env_value(env_value)
            for path in paths:
                _set_nested_value(config_data, path, value)


def _parse_env_value(env_value: str) -> Any:
    """Parse environment variable value with type conversion."""
    # Try to parse as JSON first (for default_params and other complex values)
    if env_value.startswith("{") and env_value.endswith("}"):
        try:
            return json.loads(env_value)
        except json.JSONDecodeError:
            # Not valid JSON, continue with other parsing methods
            pass

    if env_value.lower() in ("true", "yes", "1"):
        return True
    if env_value.lower() in ("false", "no", "0"):
        return False
    if env_value.isdigit():
        return int(env_value)
    if env_value.replace(".", "", 1).isdigit():
        return float(env_value)
    return env_value


def _set_nested_value(config_data: dict[str, Any], path: list[str], value: Any) -> None:
    """
    Set a value in a nested dictionary structure.

    Args:
        config_data: The dictionary to update
        path: List of keys forming the path to the target
        value: The value to set
    """
    current = config_data
    for i, path_part in enumerate(path):
        if i == len(path) - 1:
            current[path_part] = value
        else:
            # Create path if it doesn't exist
            if path_part not in current or not isinstance(current[path_part], dict):
                current[path_part] = {}
            current = current[path_part]
