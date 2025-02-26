# this_file: src/twat_search/web/config.py
"""
Configuration management for the twat_search.web module.

This module provides classes for loading and accessing configuration
settings for the web search functionality.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, Field

from twat_search.web.engine_constants import (
    BING_ANYWS,
    BING_SCRAPER,
    BING_SEARCHIT,
    BRAVE,
    BRAVE_ANYWS,
    BRAVE_NEWS,
    CRITIQUE,
    DUCKDUCKGO,
    GOOGLE_ANYWS,
    GOOGLE_HASDATA,
    GOOGLE_HASDATA_FULL,
    GOOGLE_SCRAPER,
    GOOGLE_SEARCHIT,
    GOOGLE_SERPAPI,
    PPLX,
    QWANT_ANYWS,
    QWANT_SEARCHIT,
    TAVILY,
    YANDEX_ANYWS,
    YANDEX_SEARCHIT,
    YOU,
    YOU_NEWS,
    standardize_engine_name,
)
from twat_search.web.utils import load_environment

# Remove direct dotenv import and add our utils import
# Import engine name constants from the dedicated constants module

# Load environment variables
load_environment()

logger = logging.getLogger(__name__)

# Default configuration dictionary
DEFAULT_CONFIG: dict[str, Any] = {
    "engines": {
        # Brave Search
        BRAVE: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "country": "US",
                "language": "en-US",
                "safe_search": True,
            },
        },
        BRAVE_NEWS: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "country": "US",
                "language": "en-US",
                "safe_search": True,
            },
        },
        # Brave AnyWebSearch
        BRAVE_ANYWS: {
            "enabled": True,
            "api_key": None,  # BRAVE_API_KEY
            "default_params": {
                "language": "en",
                "num_results": 10,
                "merge": True,
            },
        },
        # SerpAPI (Google)
        GOOGLE_SERPAPI: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "country": "us",
                "language": "en",
                "safe_search": True,
            },
        },
        # Google AnyWebSearch
        GOOGLE_ANYWS: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "language": "en",
                "num_results": 10,
                "merge": True,
            },
        },
        # Google Scraper
        GOOGLE_SCRAPER: {
            "enabled": True,
            "api_key": None,  # No API key required
            "default_params": {
                "language": "en",
                "region": "us",
                "safe": "active",
                "sleep_interval": 0.0,
                "ssl_verify": True,
                "proxy": None,
                "unique": True,
            },
        },
        # Google SearchIT
        GOOGLE_SEARCHIT: {
            "enabled": True,
            "api_key": None,  # No API key required
            "default_params": {
                "language": "en",
                "domain": "com",
                "sleep_interval": 0,
                "proxy": None,
            },
        },
        # Tavily Search
        TAVILY: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "search_depth": "basic",
                "include_domains": None,
                "exclude_domains": None,
                "return_rank": True,
                "max_tokens": None,
                "api_version": "2023-11-08",
            },
        },
        # Perplexity AI
        PPLX: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "model": "search",
            },
        },
        # You.com Search
        YOU: {
            "enabled": True,
            "api_key": None,
            "default_params": {},
        },
        YOU_NEWS: {
            "enabled": True,
            "api_key": None,
            "default_params": {},
        },
        # Critique Labs
        CRITIQUE: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "source_whitelist": None,
                "source_blacklist": None,
                "additional_params": None,
                "image_url": None,
            },
        },
        # DuckDuckGo
        DUCKDUCKGO: {
            "enabled": True,
            "api_key": None,  # DuckDuckGo doesn't require an API key
            "default_params": {"timeout": 10},
        },
        # Bing Scraper
        BING_SCRAPER: {
            "enabled": True,
            "api_key": None,  # No API key required, it's a scraper
            "default_params": {"num_pages": 1, "delay": 0.5},
        },
        # Bing AnyWebSearch
        BING_ANYWS: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "language": "en",
                "num_results": 10,
                "merge": True,
            },
        },
        # Bing SearchIT
        BING_SEARCHIT: {
            "enabled": True,
            "api_key": None,  # No API key required
            "default_params": {
                "language": "en",
                "domain": "com",
                "sleep_interval": 0,
                "proxy": None,
            },
        },
        # Qwant AnyWebSearch
        QWANT_ANYWS: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "language": "en",
                "num_results": 10,
                "merge": True,
            },
        },
        # Qwant SearchIT
        QWANT_SEARCHIT: {
            "enabled": True,
            "api_key": None,  # No API key required
            "default_params": {
                "language": "en",
                "geo": "us",
                "sleep_interval": 0,
                "proxy": None,
            },
        },
        # Yandex AnyWebSearch
        YANDEX_ANYWS: {
            "enabled": True,
            "api_key": None,  # YA_KEY and YA_FLDID environment variables
            "default_params": {
                "language": "en",
                "num_results": 10,
                "merge": True,
            },
        },
        # Yandex SearchIT
        YANDEX_SEARCHIT: {
            "enabled": True,
            "api_key": None,  # No API key required
            "default_params": {
                "language": "en",
                "country": "us",
                "sleep_interval": 0,
                "proxy": None,
            },
        },
        # HasData Google (Full version)
        GOOGLE_HASDATA_FULL: {
            "enabled": True,
            "api_key": None,
            "default_params": {
                "device_type": "desktop",
            },
        },
        # HasData Google (Light version)
        GOOGLE_HASDATA: {
            "enabled": True,
            "api_key": None,
            "default_params": {},
        },
    },
}


# Engine-specific configuration model
class EngineConfig(BaseModel):
    """Configuration for a single search engine."""

    enabled: bool = True
    api_key: str | None = None
    default_params: dict[str, Any] = Field(default_factory=dict)


# Main configuration model
class Config(BaseModel):
    """Main configuration model for the web search module."""

    engines: dict[str, EngineConfig] = Field(default_factory=dict)
    config_path: ClassVar[str | None] = None

    @classmethod
    def get_config_path(cls) -> Path:
        """Get the path to the configuration file.

        Returns:
            Path to the configuration file
        """
        if cls.config_path:
            return Path(cls.config_path)

        # Find the configuration directory
        config_dir = Path(
            os.environ.get(
                "XDG_CONFIG_HOME",
                Path.home() / ".config",
            ),
        )
        config_file = config_dir / "twat_search" / "config.json"
        return config_file

    def __init__(self, **data: Any) -> None:
        """Initialize configuration by loading defaults and user settings.

        Args:
            **data: Additional configuration parameters
        """
        # Start with default configuration
        config_data = DEFAULT_CONFIG.copy()

        # Load configuration from file if it exists
        config_file = self.get_config_path()
        if config_file.exists():
            try:
                with open(config_file, encoding="utf-8") as f:
                    user_config = json.load(f)
                    # Deep merge user configuration with defaults
                    self._merge_config(config_data, user_config)
            except Exception as e:
                logger.warning(
                    f"Failed to load configuration from {config_file}: {e}",
                )

        # Apply environment variable overrides
        _apply_env_overrides(config_data)

        # Apply any directly provided data
        self._merge_config(config_data, data)

        # Standardize engine names
        engines_data = config_data.get("engines", {})
        standardized_engines = {}
        for engine_name, engine_config in engines_data.items():
            std_name = standardize_engine_name(engine_name)
            standardized_engines[std_name] = engine_config
        config_data["engines"] = standardized_engines

        # Initialize the model
        super().__init__(**config_data)

    def _merge_config(self, target: dict[str, Any], source: dict[str, Any]) -> None:
        """Recursively merge source configuration into target.

        Args:
            target: Target configuration to update
            source: Source configuration to merge from
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
        """Add or update an engine configuration.

        Args:
            engine_name: Name of the engine
            enabled: Whether the engine is enabled
            api_key: API key for the engine (if required)
            default_params: Default parameters for the engine
        """
        std_engine_name = standardize_engine_name(engine_name)
        self.engines[std_engine_name] = EngineConfig(
            enabled=enabled,
            api_key=api_key,
            default_params=default_params or {},
        )


def _apply_env_overrides(self, config_data: dict[str, Any]) -> None:
    """Apply configuration overrides from environment variables.

    Args:
        config_data: Configuration data to update
    """
    engine_settings = config_data.get("engines", {})

    # Get list of available engine implementations
    try:
        from twat_search.web.engines.base import get_registered_engines

        registered_engines = get_registered_engines()
    except ImportError:
        registered_engines = {}

    # Look for API keys in environment variables
    for engine_name in engine_settings:
        std_engine_name = standardize_engine_name(engine_name)

        # Try to get engine-specific environment variable names if available
        engine_class = registered_engines.get(std_engine_name)
        api_key_vars = []

        # Append engine-specific env variable names if available
        if engine_class and hasattr(engine_class, "env_api_key_names"):
            api_key_vars.extend(engine_class.env_api_key_names)

        # Add standard patterns for API key environment variables
        api_key_vars.extend(
            [
                f"{std_engine_name.upper()}_API_KEY",
                # Original name for backward compatibility
                f"{engine_name.upper()}_API_KEY",
                f"TWAT_SEARCH_{std_engine_name.upper()}_API_KEY",
            ],
        )

        # Add name variations (handle case sensitivity issues)
        api_key_vars.extend(
            [
                f"{std_engine_name}_API_KEY",
                f"{std_engine_name}_KEY",
                f"{std_engine_name.upper()}_KEY",
            ],
        )

        # Remove duplicates while preserving order
        api_key_vars = list(dict.fromkeys(api_key_vars))

        # Debug logging to help diagnose API key detection issues
        logger.debug(
            f"Looking for API keys in environment variables: {api_key_vars}",
        )
        logger.debug(
            f"Available environment variables: {[k for k in os.environ.keys() if 'KEY' in k or 'API' in k]}",
        )

        for env_var in api_key_vars:
            if env_var in os.environ:
                if std_engine_name not in engine_settings:
                    engine_settings[std_engine_name] = {}
                engine_settings[std_engine_name]["api_key"] = os.environ[env_var]
                engine_settings[std_engine_name]["enabled"] = True
                logger.debug(
                    f"Found API key for {std_engine_name} in {env_var}",
                )
                break

        # Enabled flag environment variables
        enabled_vars = []

        # Append engine-specific env variable names if available
        if engine_class and hasattr(engine_class, "env_enabled_names"):
            enabled_vars.extend(engine_class.env_enabled_names)

        # Add standard patterns
        enabled_vars.extend(
            [
                f"{std_engine_name.upper()}_ENABLED",
                # Original name for backward compatibility
                f"{engine_name.upper()}_ENABLED",
                f"TWAT_SEARCH_{std_engine_name.upper()}_ENABLED",
            ],
        )

        # Remove duplicates while preserving order
        enabled_vars = list(dict.fromkeys(enabled_vars))

        for env_var in enabled_vars:
            if env_var in os.environ:
                if std_engine_name not in engine_settings:
                    engine_settings[std_engine_name] = {}
                engine_settings[std_engine_name]["enabled"] = os.environ[env_var].lower() in ("true", "1", "yes", "y")
                break

        # Default parameters from environment variables
        params_vars = []

        # Append engine-specific env variable names if available
        if engine_class and hasattr(engine_class, "env_params_names"):
            params_vars.extend(engine_class.env_params_names)

        # Add standard patterns
        params_vars.extend(
            [
                f"{std_engine_name.upper()}_DEFAULT_PARAMS",
                # Original name for backward compatibility
                f"{engine_name.upper()}_DEFAULT_PARAMS",
                f"TWAT_SEARCH_{std_engine_name.upper()}_DEFAULT_PARAMS",
            ],
        )

        # Remove duplicates while preserving order
        params_vars = list(dict.fromkeys(params_vars))

        for env_var in params_vars:
            if env_var in os.environ:
                try:
                    if std_engine_name not in engine_settings:
                        engine_settings[std_engine_name] = {}
                    if "default_params" not in engine_settings[std_engine_name]:
                        engine_settings[std_engine_name]["default_params"] = {}
                    params = json.loads(os.environ[env_var])
                    if isinstance(params, dict):
                        engine_settings[std_engine_name]["default_params"].update(
                            params,
                        )
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse JSON from environment variable {env_var}",
                    )
                break
