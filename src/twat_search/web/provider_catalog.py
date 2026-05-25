# this_file: src/twat_search/web/provider_catalog.py
"""Typed provider metadata for search engine routing and configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

TransportKind = Literal["api", "scraper", "browser", "llm", "plugin"]
CostClass = Literal["free", "metered", "paid", "unknown"]
StabilityClass = Literal["stable", "beta", "experimental", "fragile"]
ProviderStatus = Literal["implemented", "planned", "deprecated"]
ProxyPolicy = Literal["none", "optional", "recommended", "required"]
ProxyTransport = Literal["httpx", "playwright", "curl_cffi", "yt_dlp"]


@dataclass(frozen=True)
class RatePolicy:
    """Provider pacing defaults, with optional relaxed values for proxies."""

    timeout: float = 10.0
    retries: int = 2
    min_delay: float = 0.0
    max_parallelism: int = 1
    proxy_timeout: float = 30.0
    proxy_retries: int = 3
    proxy_min_delay: float = 0.1
    proxy_max_parallelism: int = 6


@dataclass(frozen=True)
class BrowserPolicy:
    """Browser runtime defaults for browser-backed providers."""

    persistent_context: bool = False
    headless_default: bool = True
    locale: str = "en-US"
    timezone: str = "America/New_York"
    supports_profile_proxy: bool = True


@dataclass(frozen=True)
class ProviderMetadata:
    """Static capabilities for a search provider or planned provider."""

    code: str
    display_name: str
    transport: TransportKind
    aliases: tuple[str, ...] = ()
    family: str | None = None
    status: ProviderStatus = "implemented"
    env_api_key_names: tuple[str, ...] = ()
    default_enabled: bool = True
    default_params: dict[str, Any] = field(default_factory=dict)
    proxy_policy: ProxyPolicy = "none"
    proxy_transports: tuple[ProxyTransport, ...] = ()
    browser_required: bool = False
    browser_policy: BrowserPolicy | None = None
    rate_policy: RatePolicy = field(default_factory=RatePolicy)
    cost_class: CostClass = "unknown"
    stability: StabilityClass = "beta"
    result_kinds: tuple[str, ...] = ("web",)
    package_extra: str | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        """Fill derived immutable defaults that depend on other fields."""
        if self.family is None:
            object.__setattr__(self, "family", self.transport)
        if self.proxy_policy != "none" and not self.proxy_transports:
            proxy_transports: tuple[ProxyTransport, ...] = (
                ("playwright", "httpx") if self.browser_required else ("httpx",)
            )
            object.__setattr__(self, "proxy_transports", proxy_transports)
        if self.browser_required and self.browser_policy is None:
            object.__setattr__(self, "browser_policy", BrowserPolicy())

    @property
    def requires_api_key(self) -> bool:
        """Return True when this provider has configured API-key env vars."""
        return bool(self.env_api_key_names)

    @property
    def planned(self) -> bool:
        """Return True when this provider is known but not implemented yet."""
        return self.status == "planned"

    @property
    def proxy_support(self) -> bool:
        """Return True when this provider can use a proxy."""
        return self.proxy_policy != "none"


PROVIDER_CATALOG: dict[str, ProviderMetadata] = {
    "bing_scraper": ProviderMetadata(
        code="bing_scraper",
        display_name="Bing scraper",
        transport="scraper",
        default_params={"num_pages": 1, "delay": 0.5},
        proxy_policy="optional",
        cost_class="free",
        stability="fragile",
        package_extra="bing_scraper",
    ),
    "brave": ProviderMetadata(
        code="brave",
        display_name="Brave Search API",
        transport="api",
        env_api_key_names=("BRAVE_API_KEY",),
        default_params={"country": "US", "language": "en-US", "safe_search": True},
        cost_class="metered",
        stability="stable",
    ),
    "brave_news": ProviderMetadata(
        code="brave_news",
        display_name="Brave News API",
        transport="api",
        env_api_key_names=("BRAVE_API_KEY",),
        default_params={"country": "US", "language": "en-US", "freshness": "last7days"},
        cost_class="metered",
        stability="stable",
        result_kinds=("news",),
    ),
    "critique": ProviderMetadata(
        code="critique",
        display_name="Critique Labs API",
        transport="api",
        env_api_key_names=("CRITIQUE_API_KEY", "CRITIQUE_LABS_API_KEY"),
        default_params={"num_results": 5, "relevance_adjustment": 0.5},
        cost_class="paid",
        stability="beta",
    ),
    "duckduckgo": ProviderMetadata(
        code="duckduckgo",
        display_name="DuckDuckGo",
        transport="scraper",
        default_params={"region": "us-en", "safesearch": "moderate", "timelimit": "y", "num_results": 20},
        proxy_policy="optional",
        cost_class="free",
        stability="fragile",
        package_extra="duckduckgo",
    ),
    "google_hasdata": ProviderMetadata(
        code="google_hasdata",
        display_name="Google via HasData Light API",
        transport="api",
        env_api_key_names=("HASDATA_API_KEY",),
        default_params={"num_results": 5, "language": "en"},
        cost_class="paid",
        stability="stable",
        package_extra="hasdata",
    ),
    "google_hasdata_full": ProviderMetadata(
        code="google_hasdata_full",
        display_name="Google via HasData Full API",
        transport="api",
        env_api_key_names=("HASDATA_API_KEY",),
        default_params={"num_results": 5, "language": "en"},
        cost_class="paid",
        stability="stable",
        package_extra="hasdata",
    ),
    "google_scraper": ProviderMetadata(
        code="google_scraper",
        display_name="Google scraper",
        transport="scraper",
        default_params={"num_results": 5, "language": "en", "safe": True},
        proxy_policy="optional",
        cost_class="free",
        stability="fragile",
        package_extra="google_scraper",
    ),
    "google_serpapi": ProviderMetadata(
        code="google_serpapi",
        display_name="Google via SerpAPI",
        transport="api",
        env_api_key_names=("SERPAPI_API_KEY",),
        default_params={"country": "us", "language": "en", "safe_search": True},
        cost_class="paid",
        stability="stable",
        package_extra="serpapi",
    ),
    "pplx": ProviderMetadata(
        code="pplx",
        display_name="Perplexity API",
        transport="api",
        env_api_key_names=("PPLX_API_KEY", "PERPLEXITY_API_KEY"),
        default_params={"num_results": 5, "focus": None},
        cost_class="paid",
        stability="stable",
    ),
    "tavily": ProviderMetadata(
        code="tavily",
        display_name="Tavily API",
        transport="api",
        env_api_key_names=("TAVILY_API_KEY",),
        default_params={
            "num_results": 5,
            "search_depth": "basic",
            "include_domains": [],
            "exclude_domains": [],
            "include_answer": False,
            "include_raw_content": False,
            "include_images": False,
        },
        cost_class="paid",
        stability="stable",
        package_extra="tavily",
    ),
    "you": ProviderMetadata(
        code="you",
        display_name="You.com API",
        transport="api",
        env_api_key_names=("YOUCOM_API_KEY", "YOU_API_KEY"),
        default_params={"num_results": 5, "country_code": "us", "safe_search": True},
        cost_class="paid",
        stability="stable",
    ),
    "you_news": ProviderMetadata(
        code="you_news",
        display_name="You.com News API",
        transport="api",
        env_api_key_names=("YOUCOM_API_KEY", "YOU_API_KEY"),
        default_params={"num_results": 5, "country_code": "us", "safe_search": True},
        cost_class="paid",
        stability="stable",
        result_kinds=("news",),
    ),
    # Browser-backed engines. These replace the old Falla-first mental model.
    "google_falla": ProviderMetadata(
        code="google_falla",
        display_name="Google browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "bing_falla": ProviderMetadata(
        code="bing_falla",
        display_name="Bing browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "duckduckgo_falla": ProviderMetadata(
        code="duckduckgo_falla",
        display_name="DuckDuckGo browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "aol_falla": ProviderMetadata(
        code="aol_falla",
        display_name="AOL browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "ask_falla": ProviderMetadata(
        code="ask_falla",
        display_name="Ask.com browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "dogpile_falla": ProviderMetadata(
        code="dogpile_falla",
        display_name="Dogpile browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "gibiru_falla": ProviderMetadata(
        code="gibiru_falla",
        display_name="Gibiru browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "mojeek_falla": ProviderMetadata(
        code="mojeek_falla",
        display_name="Mojeek browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "qwant_falla": ProviderMetadata(
        code="qwant_falla",
        display_name="Qwant browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "yahoo_falla": ProviderMetadata(
        code="yahoo_falla",
        display_name="Yahoo browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    "yandex_falla": ProviderMetadata(
        code="yandex_falla",
        display_name="Yandex browser search",
        transport="browser",
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        package_extra="falla",
    ),
    # Planned API/search providers discovered from /Users/adam/.env.anon.txt.
    "google_cse": ProviderMetadata(
        code="google_cse",
        display_name="Google Custom Search JSON API",
        transport="api",
        env_api_key_names=("GOOGLE_CSE_API_KEY",),
        default_params={"num_results": 5, "gl": "us", "hl": "en"},
        cost_class="metered",
        stability="stable",
        notes="Requires GOOGLE_CSE_ID or GOOGLE_CSE_CX for the search engine ID.",
    ),
    "serper": ProviderMetadata(
        code="serper",
        display_name="Serper Google Search API",
        transport="api",
        env_api_key_names=("SERPER_API_KEY",),
        default_params={"num_results": 5, "gl": "us", "hl": "en"},
        cost_class="paid",
        stability="stable",
    ),
    "dataforseo": ProviderMetadata(
        code="dataforseo",
        display_name="DataForSEO SERP API",
        transport="api",
        env_api_key_names=("DATAFORSEO_API_KEY",),
        default_params={
            "num_results": 5,
            "search_engine": "google",
            "location_code": 2840,
            "language_code": "en",
        },
        cost_class="paid",
        stability="stable",
    ),
    "exa": ProviderMetadata(
        code="exa",
        display_name="Exa Search API",
        transport="api",
        env_api_key_names=("EXAAI_API_KEY",),
        default_params={"num_results": 5, "search_type": "auto", "include_text": False, "include_highlights": True},
        cost_class="paid",
        stability="stable",
    ),
    "firecrawl": ProviderMetadata(
        code="firecrawl",
        display_name="Firecrawl Search and Extract API",
        transport="api",
        env_api_key_names=("FIRECRAWL_API_KEY", "FIRECRAWL_API_KEY_2"),
        default_params={"num_results": 5, "country": "US", "include_markdown": False},
        cost_class="paid",
        stability="stable",
    ),
    "jina": ProviderMetadata(
        code="jina",
        display_name="Jina Reader/Search API",
        transport="api",
        env_api_key_names=("JINA_API_KEY",),
        default_params={"num_results": 5, "include_content": True},
        cost_class="paid",
        stability="stable",
    ),
    "search1api": ProviderMetadata(
        code="search1api",
        display_name="Search1API",
        transport="api",
        env_api_key_names=("SEARCH1API_KEY",),
        default_params={
            "num_results": 5,
            "search_service": "google",
            "crawl_results": 0,
            "include_content": True,
            "image": False,
        },
        cost_class="paid",
        stability="beta",
    ),
    "gensee": ProviderMetadata(
        code="gensee",
        display_name="Gensee Search API",
        transport="api",
        env_api_key_names=("GENSEE_SEARCH_API_KEY",),
        default_enabled=False,
        cost_class="paid",
        stability="beta",
        status="planned",
    ),
    "aisearch": ProviderMetadata(
        code="aisearch",
        display_name="AISearch API",
        transport="api",
        env_api_key_names=("AISEARCH_API_KEY",),
        default_params={"num_results": 5, "response_type": "markdown", "context": []},
        cost_class="paid",
        stability="beta",
        result_kinds=("answer", "web"),
    ),
    "apify": ProviderMetadata(
        code="apify",
        display_name="Apify Google Search Scraper",
        transport="api",
        env_api_key_names=("APIFY_API_KEY",),
        default_params={
            "num_results": 5,
            "actor_id": "apify/google-search-scraper",
            "country_code": "us",
            "language_code": "en",
        },
        proxy_policy="optional",
        cost_class="paid",
        stability="stable",
    ),
    "browser_use": ProviderMetadata(
        code="browser_use",
        display_name="Browser Use API",
        transport="browser",
        env_api_key_names=("BROWSER_USE_API_KEY",),
        default_enabled=False,
        proxy_policy="optional",
        browser_required=True,
        cost_class="paid",
        stability="beta",
        status="planned",
    ),
    "github_search": ProviderMetadata(
        code="github_search",
        display_name="GitHub code and repository search",
        transport="api",
        env_api_key_names=("GITHUB_API_TOKEN",),
        default_enabled=False,
        cost_class="metered",
        stability="stable",
        result_kinds=("code", "repository", "issue"),
        status="planned",
    ),
}


def list_provider_metadata(include_planned: bool = True) -> list[ProviderMetadata]:
    """Return provider metadata sorted by provider code."""
    providers = PROVIDER_CATALOG.values()
    if not include_planned:
        providers = [provider for provider in providers if not provider.planned]
    return sorted(providers, key=lambda provider: provider.code)


def list_known_provider_codes(include_planned: bool = True) -> list[str]:
    """Return known provider codes sorted by provider code."""
    return [provider.code for provider in list_provider_metadata(include_planned=include_planned)]


def get_provider_metadata(code: str) -> ProviderMetadata | None:
    """Return provider metadata by normalized provider code."""
    return PROVIDER_CATALOG.get(code.replace("-", "_"))


def get_friendly_name(code: str) -> str:
    """Return the display name for a provider code."""
    provider = get_provider_metadata(code)
    return provider.display_name if provider else code


def get_api_key_env_names(code: str) -> tuple[str, ...]:
    """Return API-key environment variable names for a provider code."""
    provider = get_provider_metadata(code)
    return provider.env_api_key_names if provider else ()


def select_provider_codes(
    *,
    include_planned: bool = False,
    transport: TransportKind | None = None,
    cost_class: CostClass | None = None,
    requires_api_key: bool | None = None,
    proxy_support: bool | None = None,
) -> list[str]:
    """Select provider codes by catalog metadata."""
    providers = list_provider_metadata(include_planned=include_planned)
    selected = []
    for provider in providers:
        if transport is not None and provider.transport != transport:
            continue
        if cost_class is not None and provider.cost_class != cost_class:
            continue
        if requires_api_key is not None and provider.requires_api_key != requires_api_key:
            continue
        if proxy_support is not None and provider.proxy_support != proxy_support:
            continue
        selected.append(provider.code)
    return selected
