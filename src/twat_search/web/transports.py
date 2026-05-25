# this_file: src/twat_search/web/transports.py
"""Transport context helpers for per-provider search execution."""

from __future__ import annotations

from dataclasses import dataclass

from twat_search.web.models import EngineRequest
from twat_search.web.provider_catalog import (
    ProxyPolicy,
    ProxyTransport,
    TransportKind,
    get_provider_metadata,
)


@dataclass(frozen=True)
class TransportContext:
    """Execution transport facts derived from provider metadata."""

    engine: str
    transport: TransportKind | None
    proxy_policy: ProxyPolicy
    proxy_transports: tuple[ProxyTransport, ...]
    browser_required: bool
    result_kinds: tuple[str, ...]

    @property
    def proxy_supported(self) -> bool:
        """Return True when the provider has any proxy-capable transport."""
        return self.proxy_policy != "none"


def get_transport_context(engine_code: str) -> TransportContext:
    """Return transport context for a provider code, or neutral defaults."""
    provider = get_provider_metadata(engine_code)
    if provider is None:
        return TransportContext(
            engine=engine_code.replace("-", "_"),
            transport=None,
            proxy_policy="none",
            proxy_transports=(),
            browser_required=False,
            result_kinds=(),
        )
    return TransportContext(
        engine=provider.code,
        transport=provider.transport,
        proxy_policy=provider.proxy_policy,
        proxy_transports=provider.proxy_transports,
        browser_required=provider.browser_required,
        result_kinds=provider.result_kinds,
    )


def enrich_engine_request(request: EngineRequest) -> EngineRequest:
    """Attach provider transport metadata without changing provider params."""
    context = get_transport_context(request.engine)
    return request.model_copy(
        update={
            "engine": context.engine,
            "transport": context.transport,
            "proxy_policy": context.proxy_policy,
            "proxy_transports": context.proxy_transports,
            "browser_required": context.browser_required,
            "result_kinds": context.result_kinds,
        },
    )
