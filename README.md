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
twat search web q "font engineering news" --route resilient --json
```

The `twat` host package exposes this plugin as `twat search`.

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

## Result Model

Every result carries:

- normalized `title`, `url`, `snippet`, `source`, and `rank`
- optional raw provider payload
- detailed `SearchResponse` data with the parsed `SearchRequest`, per-engine
  `EngineOutcome` records, and structured `SearchFailure` objects
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
- no obsolete Falla-specific mess in the public API
- tests for each adapter boundary before live provider tests

Run the normal check before handing off changes:

```bash
uvx hatch test
```
