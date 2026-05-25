---
this_file: TODO.md
---

# TODO: twat-search 2.0

Goal: rebuild `twat-search` into a powerful, provider-neutral search package
that can use APIs, scrapers, browser automation, rotating proxies, unofficial
endpoints, and user-selected LLMs without preserving 0.x compatibility.

## Phase 0: Current-State Cleanup

- [x] Delete obsolete generated caches from the repo tree: `__pycache__`,
  `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `dist/`, and local databases
  unless deliberately kept outside version control.
- [ ] Remove stale review artifacts that do not describe the 2.0 target:
  `REVIEW/FILES-*`, `REVIEW/TODO-*`, and superseded Falla debug notes.
- [ ] Replace Falla-first language in code comments and docs with provider
  neutral terms: API engine, scraper engine, browser engine, LLM engine.
- [ ] Audit every source file for the required `this_file` header and fix
  missing or incorrect paths.
- [ ] Run the baseline verification command and record failures in
  `CHANGELOG.md`:
  `uvx hatch test`.

## Phase 1: Reference Research

- [ ] `private/ytrix`: extract Webshare proxy construction, proxy-enabled pacing,
  retry timeout, and parallelism policy from `ytrix/info.py`.
- [ ] `private/crapi`: inspect `private-tldr.txt` and targeted browser/proxy
  projects for reusable browser lifecycle, stealth, session, and proxy manager
  patterns.
- [ ] `private/abersetz`: inspect provider catalog, OpenAI-compatible endpoint
  selection, local discovery, and offline test patterns.
- [ ] `private/flchimp`: inspect validation, dirty-data cleanup, CLI failure
  messages, and public API docstring tests.
- [ ] `private/TO_INTEGRATE.md`: review listed projects and record borrowable
  ideas from qbittorrent search plugins, deep searchers, GitHub search, and
  dork tooling.
- [ ] `/Users/adam/.env.anon.txt`: classify available keys into API search,
  browser/proxy, LLM, crawling/extraction, and unrelated services.

## Phase 2: 2.0 Core Refactor

- [ ] Replace the current engine registry with typed provider metadata:
  capabilities, auth variables, cost class, transport type, proxy support,
  result types, and stability.
- [ ] Introduce typed config sections for proxies, LLM routing, browser runtime,
  API providers, request policy, and result processing.
- [ ] Replace stringly engine params with parsed request objects:
  `SearchRequest`, `EngineRequest`, `RoutePolicy`, and `SearchResponse`.
- [ ] Make errors first-class result data: initialization failure, auth failure,
  timeout, block/CAPTCHA, empty result, parse failure, and provider schema drift.
- [ ] Remove backwards-compatibility branches that preserve old engine names or
  Falla-specific call shapes unless they are useful aliases.
- [ ] Split execution into API, scraper, browser, and LLM transport modules.

## Phase 3: Provider Integrations

- [ ] Keep and harden current API engines: Brave, Brave News, Tavily, You.com,
  You.com News, Perplexity, SerpAPI, HasData, and Critique.
- [ ] Add API engines indicated by available keys: Google CSE, Serper, DataForSEO,
  Exa, Firecrawl, Jina, Search1API, Gensearch, AISearch, and Apify.
- [ ] Add proxy-aware scraper engines for DuckDuckGo, Bing, Google, Qwant, Yahoo,
  Mojeek, and Yandex using shared request policy.
- [ ] Add browser engines with Playwright contexts, proxy injection, block
  detection, consent handling, screenshots on failure, and clear teardown.
- [ ] Add GitHub/code search engines based on `github-search` and `github-dorks`
  references.
- [ ] Add plugin-style search adapters inspired by qbittorrent search plugins so
  experimental engines can live outside the core package.

## Phase 4: LLM Search Layer

- [ ] Add LLM provider config for OpenAI-compatible endpoints, model names, API
  keys, base URLs, and feature flags.
- [ ] Implement optional query rewriting and decomposition before fan-out.
- [ ] Implement result reranking with provenance showing model, prompt version,
  input result IDs, and score rationale.
- [ ] Implement answer synthesis that cites result URLs and never hides source
  engine failures.
- [ ] Add offline tests with fake LLM clients from the `abersetz` pattern.

## Phase 5: CLI and API

- [ ] Replace the Fire CLI surface if needed with a smaller explicit command
  layer: `q`, `info`, `providers`, `routes`, `doctor`, and `fetch`.
- [ ] Add route presets: `fast`, `cheap`, `resilient`, `deep`, `browser`, and
  `api-only`.
- [ ] Support JSONL output for streaming multi-engine results.
- [ ] Add `--explain` output that shows selected engines, skipped engines, proxy
  use, retries, errors, and LLM steps.
- [ ] Ensure `twat search ...` and `twat-search ...` expose the same behavior.

## Phase 6: Verification

- [ ] Unit-test config parsing, provider metadata, proxy URL creation, request
  parsing, result normalization, error typing, and route selection.
- [ ] Mock-test every API engine with captured responses or fixtures.
- [ ] Add live tests gated by explicit environment variables so real keys are
  never used accidentally.
- [ ] Add browser tests with local HTML fixtures before live search pages.
- [ ] Add one smoke command:
  `twat-search web q -e brave "Adam Twardoch" -n 1 --json --verbose`.
- [ ] Add a provider sweep command:
  `for engine in $(twat-search web info --plain); do twat-search web q -e "$engine" "Adam Twardoch" -n 1 --json --verbose; done`.

## Implemented in This 2.0 Rewrite

- [x] Rewrote `README.md` as the intended 2.0 package contract.
- [x] Replaced the legacy TODO with this actionable 2.0 plan.
- [x] Added typed proxy configuration with Webshare-style env loading.
- [x] Added typed LLM configuration for later model-assisted search stages.
- [x] Passed configured HTTPX proxy URLs into engine request execution.
- [x] Converted obsolete Falla/browser tests to skip cleanly when Playwright is absent.
- [x] Fixed the Hatch test environment so async tests run under `pytest-asyncio`.
- [x] Added a typed provider catalog for implemented and planned 2.0 providers.
- [x] Rebased legacy engine constants and friendly names on provider metadata.
- [x] Added provider transport/status/proxy/browser/rate metadata to CLI JSON engine info.
- [x] Generated default engine config and engine env-var mappings from provider metadata.
- [x] Replaced hard-coded CLI `free` and `best` presets with provider-catalog filters.
- [x] Added catalog-backed route policies for `best`, `fast`, `cheap`, `resilient`, `deep`, `browser`, `api-only`, and `all`.
- [x] Made `api.search(..., engines=None)` select implemented, enabled, available, credentialed route engines.
- [x] Added typed request/response/outcome/failure models for detailed multi-engine search runs.
- [x] Added `search_detailed()` so provider failures and empty responses are returned as first-class data.
- [x] Removed generated Python/test/lint cache directories from the working tree.
- [x] Promoted Serper from planned metadata to an implemented API engine using `SERPER_API_KEY`.
- [x] Added mocked Serper tests for registration, request payloads, result conversion, auth failure, and parse failure.
- [x] Promoted Google CSE from planned metadata to an implemented API engine using `GOOGLE_CSE_API_KEY` plus `GOOGLE_CSE_ID`/`GOOGLE_CSE_CX`.
- [x] Added mocked Google CSE tests for registration, request params, result conversion, CSE ID failure, and parse failure.
- [x] Promoted DataForSEO from planned metadata to an implemented live organic SERP engine using `DATAFORSEO_API_KEY`.
- [x] Added mocked DataForSEO tests for registration, Basic auth, live payloads, result conversion, and task failure.
- [x] Promoted Exa from planned metadata to an implemented search API engine using `EXAAI_API_KEY`/`EXA_API_KEY`.
- [x] Added mocked Exa tests for registration, request payloads, result conversion, and parse failure.
- [x] Added `klepto` to runtime dependencies for persistent caching backend utilities.
- [x] Promoted Firecrawl from planned metadata to an implemented v2 search/extract API engine using `FIRECRAWL_API_KEY`/`FIRECRAWL_API_KEY_2`.
- [x] Added mocked Firecrawl tests for registration, v2 payloads, result conversion, markdown snippets, and provider failure.
- [x] Promoted Jina from planned metadata to an implemented search/reader API engine using `JINA_API_KEY`.
- [x] Added mocked Jina tests for registration, URL encoding, result conversion, content fallback, and parse failure.
- [x] Promoted Search1API from planned metadata to an implemented multi-service search API engine using `SEARCH1API_KEY`.
- [x] Added mocked Search1API tests for registration, documented payload construction, result conversion, content fallback, and parse failure.
- [x] Promoted AISearch from planned metadata to an implemented web-summary API engine using `AISEARCH_API_KEY`.
- [x] Added mocked AISearch tests for registration, documented payload construction, context validation, source-backed result conversion, and parse failure.
- [x] Promoted Apify from planned metadata to an implemented Google Search Scraper actor engine using `APIFY_API_KEY`.
- [x] Added mocked Apify tests for registration, sync actor URLs, actor input payloads, nested organic results, flat dataset items, and parse failure.
