---
this_file: README.md
---

# twat-search 2.0

`twat-search` is the search layer for the `twat` toolchain: one Python package
and CLI for API search, browser search, scraper search, LLM-assisted search,
metasearch, enrichment, deduplication, and evidence capture.

Version 2.0 treats search as a routing problem. A query can fan out through
official APIs, unofficial endpoints, browser automation, direct HTML scrapers,
and LLM research providers, then return one normalized result stream with
source provenance, ranking metadata, raw payloads, and reproducible diagnostics.

## Install

```bash
uv pip install "twat-search[all]"
```

For local development:

```bash
uv sync --all-extras
uvx hatch test
```

## CLI

```bash
twat-search web q "Adam Twardoch" -e brave,serpapi,duckduckgo -n 5 --json
twat-search web info --plain
twat-search web providers --json
twat-search web routes --json
twat-search web doctor --json
twat-search web fetch https://example.com --json
twat search web q "font engineering news" --route resilient --json
twat-search web q "font tooling" --route plugins --json
twat-search web q "agent search" --route resilient --jsonl --explain
```

The `twat` host package exposes this plugin as `twat search`. JSONL output is
newline-delimited and includes request, engine, result, failure, answer, and
optional explain records for streaming consumers.

## Python API

```python
import asyncio

from twat_search.web.api import search, search_detailed


async def main() -> None:
    results = await search(
        "best current browser automation anti-bot patterns",
        engines=["brave", "google_serpapi", "duckduckgo"],
        num_results=5,
    )
    for result in results:
        print(result.source, result.title, result.url)

    detailed = await search_detailed("same query", route="resilient")
    for failure in detailed.failures:
        print(failure.engine, failure.kind, failure.message)


asyncio.run(main())
```

## Engines

2.0 supports four backend families:

- API engines: Brave, Brave News, SerpAPI, HasData, Tavily, You.com, You.com
  News, Perplexity, Critique, Google CSE, Serper, DataForSEO, Exa, Firecrawl,
  Jina, Search1API, Gensearch, and other configured providers.
- Scraper engines: DuckDuckGo, Google, Bing, qbittorrent-style plugin scrapers,
  GitHub/code search providers, and specialized dork engines.
- Plugin engines: template-based adapters that turn a query into external
  search URLs, including GitHub code/repository search and user-configured
  dork-style query expansions.
- Browser engines: Playwright-controlled Google, Bing, Qwant, Yahoo, Yandex,
  Mojeek, Gibiru, and future browser-to-API adapters.
- LLM engines: user-selected OpenAI-compatible models for query planning,
  reranking, source critique, summary extraction, and answer synthesis.

Engines are independent adapters behind a common `SearchEngine` contract. A
failure in one adapter is reported as data and does not poison the whole run.

## Configuration

Configuration is loaded from `.env`, environment variables, optional JSON
config, and explicit Python arguments. API keys are discovered from provider
specific names when possible.

Key providers already visible in `/Users/adam/.env.anon.txt` and targeted for
2.0 integration include:

- `BRAVE_API_KEY`
- `SERPAPI_API_KEY`
- `TAVILY_API_KEY`
- `HASDATA_API_KEY`
- `GOOGLE_CSE_API_KEY` and `GOOGLE_CSE_ID`
- `DATAFORSEO_API_KEY`
- `SERPER_API_KEY`
- `EXAAI_API_KEY`
- `FIRECRAWL_API_KEY`
- `JINA_API_KEY`
- `GENSEE_SEARCH_API_KEY`
- `SEARCH1API_KEY`
- `AISEARCH_API_KEY`
- `APIFY_API_KEY`
- `BRIGHTDATA_API_KEY`, `DECODO_API_KEY`, and Webshare proxy variables

### Rotating Proxies

`twat-search` understands Webshare-style rotating proxy variables:

```bash
export WEBSHARE_PROXY_USER="user"
export WEBSHARE_PROXY_PASS="pass"
export WEBSHARE_DOMAIN_NAME="p.webshare.io"
export WEBSHARE_PROXY_PORT="80"
```

When configured, HTTP and browser engines can use the proxy URL for resilient
scraping, relaxed pacing, and parallel browser sessions. Proxy use is explicit
per route or engine so API-backed searches remain clean by default.

### LLM Routing

LLM use is provider-neutral. Any OpenAI-compatible endpoint can be selected for
query rewriting, provider choice, result reranking, or synthesis:

```bash
export TWAT_SEARCH_LLM_PROVIDER="openai-compatible"
export TWAT_SEARCH_LLM_MODEL="gpt-5-mini"
export TWAT_SEARCH_LLM_API_KEY="$OPENAI_API_KEY"
export TWAT_SEARCH_LLM_BASE_URL="https://api.openai.com/v1"
export TWAT_SEARCH_LLM_QUERY_REWRITE="true"
export TWAT_SEARCH_LLM_RESULT_RERANK="true"
export TWAT_SEARCH_LLM_ANSWER_SYNTHESIS="true"
```

The package stores LLM decisions as provenance, not hidden magic. A result set
can show whether a title/snippet came from the source, an extractor, or a model.
Callers can override configured query rewriting per request with
`rewrite_query=True` or `rewrite_query=False`, and result reranking with
`rerank_results=True` or `rerank_results=False`. Answer synthesis is similarly
explicit via `synthesize_answer=True` or `synthesize_answer=False`; synthesized
answers cite result URLs and keep provider failures visible.

### Browser Runtime

Browser-backed engines share one runtime configuration so Playwright adapters,
browser-to-API probes, stealth settings, persistent profiles, proxy injection,
and failure evidence all use the same contract:

```bash
export TWAT_SEARCH_BROWSER_ENABLED="true"
export TWAT_SEARCH_BROWSER_TYPE="chromium"
export TWAT_SEARCH_BROWSER_HEADLESS="true"
export TWAT_SEARCH_BROWSER_STEALTH="true"
export TWAT_SEARCH_BROWSER_PERSISTENT_CONTEXT="false"
export TWAT_SEARCH_BROWSER_LOCALE="en-US"
export TWAT_SEARCH_BROWSER_TIMEZONE="America/New_York"
export TWAT_SEARCH_BROWSER_SCREENSHOTS="true"
export TWAT_SEARCH_BROWSER_SAVE_HTML="true"
export TWAT_SEARCH_BROWSER_NETWORK_LOG="false"
```

The browser config can produce Playwright launch/context kwargs without
importing Playwright, which keeps unit tests offline and lets future browser
engines opt into the same proxy and evidence-capture behavior.

Browser diagnostics are shared as well. Browser engines can classify captured
HTML as CAPTCHA, bot challenge, consent interstitial, rate limit, login wall, or
generic block, then write configured HTML and screenshot artifacts under a
single evidence contract. Local fixture tests cover these states before live
search pages are exercised.

### Search Plugins

The `plugin_search` engine is a small adapter format for experimental search
targets. A plugin declares a code, name, URL template, and optional query
template. It can expand a normal query into a site-specific search URL without
adding dependencies or executing untrusted plugin code:

```python
from twat_search.web.config import Config, EngineConfig

config = Config(
    engines={
        "plugin_search": EngineConfig(
            enabled=True,
            default_params={
                "plugins": [
                    {
                        "code": "github-env",
                        "name": "GitHub env files",
                        "query_template": "{query} filename:.env",
                        "url_template": "https://github.com/search?q={query_url}&type=code",
                    }
                ]
            },
        )
    }
)
```

This is the first step toward qBittorrent-style external adapters, GitHub dork
packs, and project-local search plugins that can live outside the core package.

## Result Model

Every result carries:

- normalized `title`, `url`, `snippet`, `source`, and `rank`
- optional raw provider payload
- detailed `SearchResponse` data with the parsed `SearchRequest`, per-engine
  `EngineOutcome` records, and structured `SearchFailure` objects
- browser failure details for CAPTCHA, consent, rate-limit, bot-challenge, and
  artifact paths when a browser engine reports a challenge
- future engine timing, proxy, and route metadata
- future content artifacts such as fetched HTML, extracted text, screenshots,
  citations, and LLM summaries

## Reference Integrations

The 2.0 design borrows from the local `private/` reference projects instead of
adding dependencies blindly:

- `private/ytrix`: Webshare proxy URL construction, proxy-aware pacing, and
  parallelism decisions.
- `private/crapi`: browser lifecycle, stealth, browser-to-API, and proxy manager
  patterns.
- `private/abersetz`: OpenAI-compatible provider catalog and local/offline LLM
  selection patterns.
- `private/flchimp`: explicit validation, dirty-data handling, and operational
  CLI ergonomics.
- `private/TO_INTEGRATE.md`: external search project ideas including plugin
  search, deep search, GitHub search, dorks, and open deep research.

## Development Contract

2.0 is allowed to break compatibility with the current 0.x code. The priority
is a smaller, typed, testable core:

- clean engine registry
- strict provider capability metadata
- explicit proxy and browser configuration
- normalized result and error data
- no obsolete browser-scraper internals leaking into the public API
- tests for each adapter boundary before live provider tests

Run the normal check before handing off changes:

```bash
uvx hatch test
```
