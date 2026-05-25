# this_file: src/twat_search/web/routes.py
"""Catalog-backed search route selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from twat_search.web.provider_catalog import ProviderMetadata, get_provider_metadata, list_provider_metadata

if TYPE_CHECKING:
    from twat_search.web.config import Config

RouteName = Literal["best", "fast", "cheap", "resilient", "deep", "browser", "api-only", "all"]


@dataclass(frozen=True)
class RoutePolicy:
    """A named engine-selection policy."""

    name: RouteName
    transports: tuple[str, ...] = ()
    cost_classes: tuple[str, ...] = ()
    require_proxy_support: bool | None = None
    include_unkeyed: bool = True
    include_keyed: bool = True
    max_engines: int | None = None
    stability: tuple[str, ...] = ("stable", "beta", "experimental", "fragile")


ROUTE_POLICIES: dict[str, RoutePolicy] = {
    "best": RoutePolicy(
        name="best",
        transports=("api", "scraper"),
        include_unkeyed=True,
        include_keyed=True,
        max_engines=3,
        stability=("stable", "beta"),
    ),
    "fast": RoutePolicy(
        name="fast",
        transports=("api", "scraper"),
        include_unkeyed=True,
        include_keyed=True,
        max_engines=3,
        stability=("stable", "beta"),
    ),
    "cheap": RoutePolicy(
        name="cheap",
        cost_classes=("free",),
        include_unkeyed=True,
        include_keyed=False,
        max_engines=5,
    ),
    "resilient": RoutePolicy(
        name="resilient",
        transports=("api", "scraper", "browser"),
        include_unkeyed=True,
        include_keyed=True,
        stability=("stable", "beta", "experimental", "fragile"),
    ),
    "deep": RoutePolicy(
        name="deep",
        transports=("api", "scraper", "browser"),
        include_unkeyed=True,
        include_keyed=True,
        stability=("stable", "beta", "experimental", "fragile"),
    ),
    "browser": RoutePolicy(
        name="browser",
        transports=("browser",),
        include_unkeyed=True,
        include_keyed=True,
        stability=("stable", "beta", "experimental", "fragile"),
    ),
    "api-only": RoutePolicy(
        name="api-only",
        transports=("api",),
        include_unkeyed=False,
        include_keyed=True,
        stability=("stable", "beta", "experimental", "fragile"),
    ),
    "all": RoutePolicy(
        name="all",
        transports=("api", "scraper", "browser"),
        include_unkeyed=True,
        include_keyed=True,
        stability=("stable", "beta", "experimental", "fragile"),
    ),
}


def get_route_policy(route: str | None) -> RoutePolicy:
    """Return a route policy by name, defaulting to best."""
    route_name = (route or "best").replace("_", "-")
    try:
        return ROUTE_POLICIES[route_name]
    except KeyError as err:
        available = ", ".join(sorted(ROUTE_POLICIES))
        msg = f"Unknown search route '{route_name}'. Available routes: {available}"
        raise ValueError(msg) from err


def _provider_is_configured(provider: ProviderMetadata, config: Config) -> bool:
    """Return True when the provider is enabled and has required credentials."""
    engine_config = config.engines.get(provider.code)
    if engine_config is None or not engine_config.enabled:
        return False
    if provider.requires_api_key and not engine_config.api_key:
        return False
    return True


def select_route_engines(
    config: Config,
    route: str | None = "best",
    available_engines: set[str] | None = None,
) -> list[str]:
    """Select runnable engine codes for a route using catalog and config state."""
    policy = get_route_policy(route)
    selected: list[str] = []

    for provider in list_provider_metadata(include_planned=False):
        if provider.code not in config.engines:
            continue
        if available_engines is not None and provider.code not in available_engines:
            continue
        if policy.transports and provider.transport not in policy.transports:
            continue
        if policy.cost_classes and provider.cost_class not in policy.cost_classes:
            continue
        if policy.require_proxy_support is not None and provider.proxy_support != policy.require_proxy_support:
            continue
        if provider.stability not in policy.stability:
            continue
        if provider.requires_api_key and not policy.include_keyed:
            continue
        if not provider.requires_api_key and not policy.include_unkeyed:
            continue
        if not _provider_is_configured(provider, config):
            continue

        selected.append(provider.code)
        if policy.max_engines is not None and len(selected) >= policy.max_engines:
            break

    return selected


def route_names() -> list[str]:
    """Return available route names."""
    return sorted(ROUTE_POLICIES)


def provider_for_engine(engine_name: str) -> ProviderMetadata | None:
    """Return provider metadata for an engine name after CLI normalization."""
    return get_provider_metadata(engine_name)
