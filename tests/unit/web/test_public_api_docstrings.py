#!/usr/bin/env python
# this_file: tests/unit/web/test_public_api_docstrings.py
"""Public API docstring checks for the web search boundary models."""

from __future__ import annotations

from collections.abc import Callable

from twat_search.web.browser import BrowserBlockSignal, BrowserEvidence
from twat_search.web.config import BrowserConfig, Config, EngineConfig, LLMConfig, ProxyConfig
from twat_search.web.engines.plugin_search import SearchPluginSpec
from twat_search.web.models import EngineOutcome, EngineRequest, SearchFailure, SearchRequest, SearchResponse, SearchResult


PUBLIC_CLASSES = [
    BrowserBlockSignal,
    BrowserConfig,
    BrowserEvidence,
    Config,
    EngineConfig,
    LLMConfig,
    ProxyConfig,
    SearchPluginSpec,
    EngineOutcome,
    EngineRequest,
    SearchFailure,
    SearchRequest,
    SearchResponse,
    SearchResult,
]


def _public_methods_defined_on(cls: type) -> list[tuple[str, Callable[..., object]]]:
    """Return public callables declared directly on a class."""
    methods: list[tuple[str, Callable[..., object]]] = []
    for name, value in cls.__dict__.items():
        if name.startswith("_"):
            continue
        if isinstance(value, classmethod | staticmethod):
            candidate = value.__func__
        else:
            candidate = value
        if callable(candidate):
            methods.append((name, candidate))
    return methods


def test_public_config_and_model_classes_have_docstrings() -> None:
    """Public boundary classes should explain their role."""
    for cls in PUBLIC_CLASSES:
        assert cls.__doc__ and len(cls.__doc__.strip()) > 20, f"{cls.__name__} needs a useful docstring"


def test_public_config_and_model_methods_have_docstrings() -> None:
    """Public methods declared in this package should explain their boundary contract."""
    for cls in PUBLIC_CLASSES:
        for name, method in _public_methods_defined_on(cls):
            assert method.__doc__ and len(method.__doc__.strip()) > 20, f"{cls.__name__}.{name} needs a docstring"
