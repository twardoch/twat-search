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
    route_priority: int = 1000
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
        route_priority=260,
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
        route_priority=10,
    ),
    "brave_news": ProviderMetadata(
        code="brave_news",
        display_name="Brave News API",
        transport="api",
        env_api_key_names=("BRAVE_API_KEY",),
        default_params={"country": "US", "language": "en-US", "freshness": "last7days"},
        cost_class="metered",
        stability="stable",
        route_priority=20,
        result_kinds=("news",),
    ),
    "brightdata": ProviderMetadata(
        code="brightdata",
        display_name="Bright Data SERP/browser platform",
        transport="api",
        env_api_key_names=("BRIGHTDATA_API_KEY",),
        default_enabled=False,
        proxy_policy="recommended",
        proxy_transports=("httpx", "playwright"),
        cost_class="paid",
        stability="stable",
        status="planned",
        result_kinds=("web", "serp", "browser"),
        notes="Available key suggests SERP, browser, or proxy-backed search can be integrated after endpoint verification.",
    ),
    "browseai": ProviderMetadata(
        code="browseai",
        display_name="Browse AI",
        transport="browser",
        env_api_key_names=("BROWSEAI_API_KEY",),
        default_enabled=False,
        proxy_policy="optional",
        browser_required=True,
        cost_class="paid",
        stability="beta",
        status="planned",
        result_kinds=("web", "extraction"),
        notes="Candidate for browser automation or extraction workflows after API docs verification.",
    ),
    "capturekit": ProviderMetadata(
        code="capturekit",
        display_name="CaptureKit",
        transport="api",
        env_api_key_names=("CAPTUREKIT_API_KEY",),
        default_enabled=False,
        proxy_policy="optional",
        cost_class="paid",
        stability="beta",
        status="planned",
        result_kinds=("screenshot", "web"),
        notes="Candidate for screenshot-on-failure or rendered-page capture support.",
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
        route_priority=200,
        package_extra="duckduckgo",
    ),
    "decodo": ProviderMetadata(
        code="decodo",
        display_name="Decodo proxy/SERP platform",
        transport="api",
        env_api_key_names=("DECODO_API_KEY",),
        default_enabled=False,
        proxy_policy="recommended",
        proxy_transports=("httpx", "playwright"),
        cost_class="paid",
        stability="beta",
        status="planned",
        result_kinds=("web", "serp", "proxy"),
        notes="Available key suggests proxy or SERP integration should be evaluated after official docs verification.",
    ),
    "google_hasdata": ProviderMetadata(
        code="google_hasdata",
        display_name="Google via HasData Light API",
        transport="api",
        env_api_key_names=("HASDATA_API_KEY",),
        default_params={"num_results": 5, "language": "en"},
        cost_class="paid",
        stability="stable",
        route_priority=35,
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
        route_priority=34,
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
        route_priority=250,
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
        route_priority=60,
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
        route_priority=45,
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
        route_priority=30,
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
        route_priority=40,
    ),
    "you_news": ProviderMetadata(
        code="you_news",
        display_name="You.com News API",
        transport="api",
        env_api_key_names=("YOUCOM_API_KEY", "YOU_API_KEY"),
        default_params={"num_results": 5, "country_code": "us", "safe_search": True},
        cost_class="paid",
        stability="stable",
        route_priority=42,
        result_kinds=("news",),
    ),
    # Browser-backed engines backed by the bundled Playwright scraper adapter.
    "google_browser": ProviderMetadata(
        code="google_browser",
        display_name="Google browser search",
        transport="browser",
        aliases=("google_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=300,
        package_extra="falla",
    ),
    "bing_browser": ProviderMetadata(
        code="bing_browser",
        display_name="Bing browser search",
        transport="browser",
        aliases=("bing_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=310,
        package_extra="falla",
    ),
    "duckduckgo_browser": ProviderMetadata(
        code="duckduckgo_browser",
        display_name="DuckDuckGo browser search",
        transport="browser",
        aliases=("duckduckgo_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=320,
        package_extra="falla",
    ),
    "aol_browser": ProviderMetadata(
        code="aol_browser",
        display_name="AOL browser search",
        transport="browser",
        aliases=("aol_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=390,
        package_extra="falla",
    ),
    "ask_browser": ProviderMetadata(
        code="ask_browser",
        display_name="Ask.com browser search",
        transport="browser",
        aliases=("ask_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=380,
        package_extra="falla",
    ),
    "dogpile_browser": ProviderMetadata(
        code="dogpile_browser",
        display_name="Dogpile browser search",
        transport="browser",
        aliases=("dogpile_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=370,
        package_extra="falla",
    ),
    "gibiru_browser": ProviderMetadata(
        code="gibiru_browser",
        display_name="Gibiru browser search",
        transport="browser",
        aliases=("gibiru_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=360,
        package_extra="falla",
    ),
    "mojeek_browser": ProviderMetadata(
        code="mojeek_browser",
        display_name="Mojeek browser search",
        transport="browser",
        aliases=("mojeek_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=350,
        package_extra="falla",
    ),
    "qwant_browser": ProviderMetadata(
        code="qwant_browser",
        display_name="Qwant browser search",
        transport="browser",
        aliases=("qwant_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=330,
        package_extra="falla",
    ),
    "yahoo_browser": ProviderMetadata(
        code="yahoo_browser",
        display_name="Yahoo browser search",
        transport="browser",
        aliases=("yahoo_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=340,
        package_extra="falla",
    ),
    "yandex_browser": ProviderMetadata(
        code="yandex_browser",
        display_name="Yandex browser search",
        transport="browser",
        aliases=("yandex_falla",),
        default_params={"num_results": 5},
        proxy_policy="optional",
        browser_required=True,
        cost_class="free",
        stability="fragile",
        route_priority=400,
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
        route_priority=65,
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
        route_priority=55,
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
        route_priority=70,
    ),
    "exa": ProviderMetadata(
        code="exa",
        display_name="Exa Search API",
        transport="api",
        env_api_key_names=("EXAAI_API_KEY",),
        default_params={"num_results": 5, "search_type": "auto", "include_text": False, "include_highlights": True},
        cost_class="paid",
        stability="stable",
        route_priority=25,
    ),
    "firecrawl": ProviderMetadata(
        code="firecrawl",
        display_name="Firecrawl Search and Extract API",
        transport="api",
        env_api_key_names=("FIRECRAWL_API_KEY", "FIRECRAWL_API_KEY_2"),
        default_params={"num_results": 5, "country": "US", "include_markdown": False},
        cost_class="paid",
        stability="stable",
        route_priority=32,
    ),
    "jina": ProviderMetadata(
        code="jina",
        display_name="Jina Reader/Search API",
        transport="api",
        env_api_key_names=("JINA_API_KEY",),
        default_params={"num_results": 5, "include_content": True},
        cost_class="paid",
        stability="stable",
        route_priority=50,
    ),
    "langsearch": ProviderMetadata(
        code="langsearch",
        display_name="LangSearch API",
        transport="api",
        env_api_key_names=("LANGSEARCH_API_KEY",),
        default_params={"num_results": 5, "freshness": "noLimit", "summary": True},
        cost_class="paid",
        stability="beta",
        route_priority=75,
        result_kinds=("web", "answer"),
    ),
    "mapleserp": ProviderMetadata(
        code="mapleserp",
        display_name="MapleSERP API",
        transport="api",
        env_api_key_names=("MAPLESERP_API_KEY",),
        default_params={"num_results": 5, "engine": "google"},
        cost_class="paid",
        stability="beta",
        route_priority=80,
        result_kinds=("web", "serp"),
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
        route_priority=85,
    ),
    "search_cans": ProviderMetadata(
        code="search_cans",
        display_name="Search Cans API",
        transport="api",
        env_api_key_names=("SEARCH_CANS_API_KEY",),
        default_params={"num_results": 5, "engine": "google", "timeout_ms": 20000, "page": 1},
        cost_class="paid",
        stability="beta",
        route_priority=90,
        result_kinds=("web", "serp"),
    ),
    "gensee": ProviderMetadata(
        code="gensee",
        display_name="Gensee Search API",
        transport="api",
        env_api_key_names=("GENSEE_SEARCH_API_KEY",),
        default_params={"num_results": 5, "multilingual": False},
        cost_class="paid",
        stability="beta",
        route_priority=95,
        result_kinds=("web", "answer"),
    ),
    "plugin_search": ProviderMetadata(
        code="plugin_search",
        display_name="Template search plugins",
        transport="plugin",
        default_enabled=False,
        default_params={
            "plugins": [
                {
                    "code": "github-code",
                    "name": "GitHub code search",
                    "url_template": "https://github.com/search?q={query_url}&type=code",
                    "title_template": "GitHub code: {query}",
                    "snippet_template": "Open GitHub code search for {query}",
                },
                {
                    "code": "github-repositories",
                    "name": "GitHub repositories",
                    "url_template": "https://github.com/search?q={query_url}&type=repositories",
                    "title_template": "GitHub repositories: {query}",
                    "snippet_template": "Open GitHub repository search for {query}",
                },
            ],
        },
        cost_class="free",
        stability="experimental",
        route_priority=500,
        result_kinds=("web", "code", "repository"),
        notes="Query-template adapter inspired by qBittorrent search plugins and GitHub dork tooling.",
    ),
    "aisearch": ProviderMetadata(
        code="aisearch",
        display_name="AISearch API",
        transport="api",
        env_api_key_names=("AISEARCH_API_KEY",),
        default_params={"num_results": 5, "response_type": "markdown", "context": []},
        cost_class="paid",
        stability="beta",
        route_priority=100,
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
        route_priority=110,
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
        env_api_key_names=("GITHUB_API_TOKEN", "GITHUB_TOKEN", "HOMEBREW_GITHUB_API_TOKEN", "ZENCLI_GITHUBAUTHTOKEN"),
        default_params={"num_results": 5, "search_type": "repositories", "sort": None, "order": "desc"},
        cost_class="metered",
        stability="stable",
        route_priority=120,
        result_kinds=("code", "repository", "issue"),
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
    return PROVIDER_CATALOG.get(canonical_provider_code(code))


def canonical_provider_code(code: str) -> str:
    """Return the canonical provider code for a code or useful alias."""
    normalized = code.replace("-", "_")
    if normalized in PROVIDER_CATALOG:
        return normalized
    for provider in PROVIDER_CATALOG.values():
        if normalized in provider.aliases:
            return provider.code
    return normalized


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
