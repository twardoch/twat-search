# this_file: src/twat_search/web/routes.py
"""Catalog-backed search route selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from twat_search.web.models import RouteName, RoutePolicy
from twat_search.web.provider_catalog import (
    ProviderMetadata,
    canonical_provider_code,
    get_provider_metadata,
    list_provider_metadata,
)

if TYPE_CHECKING:
    from twat_search.web.config import Config

RouteDecisionReason = Literal[
    "selected",
    "missing_config",
    "unavailable",
    "transport",
    "cost_class",
    "proxy_support",
    "stability",
    "keyed_excluded",
    "unkeyed_excluded",
    "disabled",
    "missing_api_key",
    "max_engines",
]


@dataclass(frozen=True)
class RouteDecision:
    """Selection outcome for one provider under a route policy."""

    engine: str
    selected: bool
    reason: RouteDecisionReason


@dataclass(frozen=True)
class RouteSelection:
    """Full route-selection result with selected engines and skip reasons."""

    policy: RoutePolicy
    selected_engines: list[str]
    decisions: list[RouteDecision]

    @property
    def skipped(self) -> list[RouteDecision]:
        """Return decisions that did not select an engine."""
        return [decision for decision in self.decisions if not decision.selected]


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
        transports=("api", "scraper", "browser", "plugin"),
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
    "plugins": RoutePolicy(
        name="plugins",
        transports=("plugin",),
        include_unkeyed=True,
        include_keyed=True,
        stability=("stable", "beta", "experimental", "fragile"),
    ),
    "all": RoutePolicy(
        name="all",
        transports=("api", "scraper", "browser", "plugin"),
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


def select_route_engines(
    config: Config,
    route: str | None = "best",
    available_engines: set[str] | None = None,
) -> list[str]:
    """Select runnable engine codes for a route using catalog and config state."""
    return explain_route_selection(
        config=config,
        route=route,
        available_engines=available_engines,
    ).selected_engines


def explain_route_selection(
    config: Config,
    route: str | None = "best",
    available_engines: set[str] | None = None,
) -> RouteSelection:
    """Select engines for a route and retain typed reasons for skipped providers."""
    policy = get_route_policy(route)
    selected: list[str] = []
    decisions: list[RouteDecision] = []
    normalized_available = (
        {canonical_provider_code(engine) for engine in available_engines} if available_engines is not None else None
    )

    providers = sorted(
        list_provider_metadata(include_planned=False),
        key=lambda provider: (provider.route_priority, provider.code),
    )
    for provider in providers:
        if provider.code not in config.engines:
            decisions.append(RouteDecision(provider.code, selected=False, reason="missing_config"))
            continue
        engine_config = config.engines[provider.code]
        if not engine_config.enabled:
            decisions.append(RouteDecision(provider.code, selected=False, reason="disabled"))
            continue
        if provider.requires_api_key and not engine_config.api_key:
            decisions.append(RouteDecision(provider.code, selected=False, reason="missing_api_key"))
            continue
        if normalized_available is not None and provider.code not in normalized_available:
            decisions.append(RouteDecision(provider.code, selected=False, reason="unavailable"))
            continue
        if policy.transports and provider.transport not in policy.transports:
            decisions.append(RouteDecision(provider.code, selected=False, reason="transport"))
            continue
        if policy.cost_classes and provider.cost_class not in policy.cost_classes:
            decisions.append(RouteDecision(provider.code, selected=False, reason="cost_class"))
            continue
        if policy.require_proxy_support is not None and provider.proxy_support != policy.require_proxy_support:
            decisions.append(RouteDecision(provider.code, selected=False, reason="proxy_support"))
            continue
        if provider.stability not in policy.stability:
            decisions.append(RouteDecision(provider.code, selected=False, reason="stability"))
            continue
        if provider.requires_api_key and not policy.include_keyed:
            decisions.append(RouteDecision(provider.code, selected=False, reason="keyed_excluded"))
            continue
        if not provider.requires_api_key and not policy.include_unkeyed:
            decisions.append(RouteDecision(provider.code, selected=False, reason="unkeyed_excluded"))
            continue
        if policy.max_engines is not None and len(selected) >= policy.max_engines:
            decisions.append(RouteDecision(provider.code, selected=False, reason="max_engines"))
            continue

        selected.append(provider.code)
        decisions.append(RouteDecision(provider.code, selected=True, reason="selected"))

    return RouteSelection(policy=policy, selected_engines=selected, decisions=decisions)


def route_names() -> list[str]:
    """Return available route names."""
    return sorted(ROUTE_POLICIES)


def provider_for_engine(engine_name: str) -> ProviderMetadata | None:
    """Return provider metadata for an engine name after CLI normalization."""
    return get_provider_metadata(engine_name)
