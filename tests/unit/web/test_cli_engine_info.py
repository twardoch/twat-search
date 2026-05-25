#!/usr/bin/env python
# this_file: tests/unit/web/test_cli_engine_info.py
"""Unit tests for CLI engine metadata helpers."""

from __future__ import annotations

from pytest import MonkeyPatch

from twat_search.web.cli import _get_engine_info
from twat_search.web.config import EngineConfig


def test_engine_info_includes_provider_metadata() -> None:
    """Engine info exposes provider-catalog fields used by route planning."""
    info = _get_engine_info(
        "brave",
        EngineConfig(enabled=True),
        registered_engines={},
    )

    assert info["transport"] == "api"
    assert info["status"] == "implemented"
    assert info["api_key_required"] is True
    assert info["proxy_support"] is False
    assert info["proxy_policy"] == "none"
    assert info["cost_class"] == "metered"
    assert info["stability"] == "stable"
    assert info["planned"] is False


def test_engine_info_handles_browser_provider_metadata() -> None:
    """Browser engines expose browser and proxy capability metadata."""
    info = _get_engine_info(
        "google_falla",
        EngineConfig(enabled=True),
        registered_engines={},
    )

    assert info["transport"] == "browser"
    assert info["browser_required"] is True
    assert info["proxy_support"] is True
    assert info["proxy_policy"] == "optional"
    assert info["proxy_transports"] == ["playwright", "httpx"]
    assert info["api_key_required"] is False


def test_engine_info_marks_env_key_as_set(monkeypatch: MonkeyPatch) -> None:
    """Engine info checks provider env vars even without registered classes."""
    monkeypatch.setenv("GENSEE_SEARCH_API_KEY", "test-key")

    info = _get_engine_info(
        "gensee",
        EngineConfig(enabled=False),
        registered_engines={},
    )

    assert info["planned"] is True
    assert info["api_key_required"] is True
    assert info["api_key_set"] is True
    assert info["env_vars"] == [{"name": "GENSEE_SEARCH_API_KEY", "set": True}]
