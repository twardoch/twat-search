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
- [x] Remove stale review artifacts that do not describe the 2.0 target:
  `REVIEW/FILES-*`, `REVIEW/TODO-*`, and superseded Falla debug notes.
- [x] Replace Falla-first language in code comments and docs with provider
  neutral terms: API engine, scraper engine, browser engine, LLM engine.
- [x] Audit every source file for the required `this_file` header and fix
  missing or incorrect paths.
- [x] Run the baseline verification command and record failures in
  `CHANGELOG.md`:
  `uvx hatch test`.

## Phase 1: Reference Research

- [x] `private/ytrix`: extract Webshare proxy construction, proxy-enabled pacing,
  retry timeout, and parallelism policy from `ytrix/info.py`.
- [x] `private/crapi`: inspect `private-tldr.txt` and targeted browser/proxy
  projects for reusable browser lifecycle, stealth, session, and proxy manager
  patterns.
- [x] `private/abersetz`: inspect provider catalog, OpenAI-compatible endpoint
  selection, local discovery, and offline test patterns.
- [x] `private/flchimp`: inspect validation, dirty-data cleanup, CLI failure
  messages, and public API docstring tests.
- [x] `private/TO_INTEGRATE.md`: review listed projects and record borrowable
  ideas from qbittorrent search plugins, deep searchers, GitHub search, and
  dork tooling.
- [x] `/Users/adam/.env.anon.txt`: classify available keys into API search,
  browser/proxy, LLM, crawling/extraction, and unrelated services.

## Phase 2: 2.0 Core Refactor

- [x] Replace the current engine registry with typed provider metadata:
  capabilities, auth variables, cost class, transport type, proxy support,
  result types, and stability.
- [x] Introduce typed config sections for proxies, LLM routing, browser runtime,
  API providers, request policy, and result processing.
- [x] Replace stringly engine params with parsed request objects:
  `SearchRequest`, `EngineRequest`, `RoutePolicy`, and `SearchResponse`.
- [x] Make errors first-class result data: initialization failure, auth failure,
  timeout, block/CAPTCHA, empty result, parse failure, and provider schema drift.
- [x] Remove backwards-compatibility branches that preserve old engine names or
  Falla-specific call shapes unless they are useful aliases.
- [x] Split execution into API, scraper, browser, and LLM transport modules.

## Phase 3: Provider Integrations

- [x] Keep and harden current API engines: Brave, Brave News, Tavily, You.com,
  You.com News, Perplexity, SerpAPI, HasData, and Critique.
- [x] Add API engines indicated by available keys: Google CSE, Serper, DataForSEO,
  Exa, Firecrawl, Jina, Search1API, AISearch, Apify, and Gensee.
- [x] Add proxy-aware scraper engines for DuckDuckGo, Bing, Google, Qwant, Yahoo,
  Mojeek, and Yandex using shared request policy.
- [x] Add browser engines with Playwright contexts, proxy injection, block
  detection, consent handling, screenshots on failure, and clear teardown.
- [x] Add GitHub/code search engines based on `github-search` and `github-dorks`
  references.
- [x] Add plugin-style search adapters inspired by qbittorrent search plugins so
  experimental engines can live outside the core package.

## Phase 4: LLM Search Layer

- [x] Add LLM provider config for OpenAI-compatible endpoints, model names, API
  keys, base URLs, and feature flags.
- [x] Implement optional query rewriting and decomposition before fan-out.
- [x] Implement result reranking with provenance showing model, prompt version,
  input result IDs, and score rationale.
- [x] Implement answer synthesis that cites result URLs and never hides source
  engine failures.
- [x] Add offline tests with fake LLM clients from the `abersetz` pattern.

## Phase 5: CLI and API

- [x] Replace the Fire CLI surface if needed with a smaller explicit command
  layer: `q`, `info`, `providers`, `routes`, `doctor`, and `fetch`.
- [x] Add route presets: `fast`, `cheap`, `resilient`, `deep`, `browser`, and
  `api-only`.
- [x] Support JSONL output for streaming multi-engine results.
- [x] Add `--explain` output that shows selected engines, skipped engines, proxy
  use, retries, errors, and LLM steps.
- [x] Ensure `twat search ...` and `twat-search ...` expose the same behavior.

## Phase 6: Verification

- [x] Unit-test config parsing, provider metadata, proxy URL creation, request
  parsing, result normalization, error typing, and route selection.
- [x] Mock-test every API engine with captured responses or fixtures.
- [x] Add live tests gated by explicit environment variables so real keys are
  never used accidentally.
- [x] Add browser tests with local HTML fixtures before live search pages.
- [x] Add one smoke command:
  `twat-search web q -e brave "Adam Twardoch" -n 1 --json --verbose`.
- [x] Add a provider sweep command:
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
- [x] Added OpenAI-compatible LLM client helpers for opt-in query rewriting.
- [x] Wired optional query rewriting before provider fan-out while preserving the original query and rewrite provenance.
- [x] Wired optional query decomposition before provider fan-out with subquery provenance on results.
- [x] Added offline fake-client tests for LLM request shape, response parsing, fallback behavior, direct fake-client injection, and search API rewrite wiring.
- [x] Added optional LLM result reranking with per-result model, prompt-version, input-result, score, and rationale provenance.
- [x] Added optional LLM answer synthesis with URL citations and explicit source-failure preservation.
- [x] Classified `/Users/adam/.env.anon.txt` search-adjacent keys: implemented API/search keys include Brave, Critique, DataForSEO, Exa, Firecrawl, GitHub, Google CSE, HasData, Jina, LangSearch, MapleSERP, Perplexity, Search1API, SearchCans, SerpAPI, Serper, Tavily, AISearch, and Apify; planned API/search candidates include Gensee, Bright Data, Browse AI, Browser Use, CaptureKit, and Decodo; proxy/browser infrastructure includes Webshare, Bright Data, Decodo, Browser Use, Browse AI, CaptureKit, and Cliproxy; LLM endpoint keys are numerous OpenAI-compatible providers and are covered by the provider-neutral LLM config.
- [x] Added planned provider metadata for env-discovered LangSearch, MapleSERP, Search Cans, Bright Data, Browse AI, CaptureKit, and Decodo.
- [x] Promoted LangSearch from planned metadata to an implemented Web Search API engine using `LANGSEARCH_API_KEY`.
- [x] Added mocked LangSearch tests for registration, documented payload construction, result conversion, provider errors, and parse failure.
- [x] Promoted MapleSERP from planned metadata to an implemented SERP API engine using `MAPLESERP_API_KEY`.
- [x] Added mocked MapleSERP tests for registration, documented GET params, result conversion, auth failure, and parse failure.
- [x] Promoted SearchCans from planned metadata to an implemented SERP API engine using `SEARCH_CANS_API_KEY`.
- [x] Added mocked SearchCans tests for registration, documented payload construction, result conversion, provider errors, and parse failure.
- [x] Promoted Gensee from planned metadata to an implemented Search Agent API engine using `GENSEE_SEARCH_API_KEY`.
- [x] Added mocked Gensee tests for registration, documented GET params, result conversion, auth failure, and parse failure.
- [x] Added mocked Search1API tests for registration, documented payload construction, result conversion, content fallback, and parse failure.
- [x] Promoted AISearch from planned metadata to an implemented web-summary API engine using `AISEARCH_API_KEY`.
- [x] Added mocked AISearch tests for registration, documented payload construction, context validation, source-backed result conversion, and parse failure.
- [x] Promoted Apify from planned metadata to an implemented Google Search Scraper actor engine using `APIFY_API_KEY`.
- [x] Added mocked Apify tests for registration, sync actor URLs, actor input payloads, nested organic results, flat dataset items, and parse failure.
- [x] Promoted GitHub search from planned metadata to an implemented REST API engine using `GITHUB_API_TOKEN`/`GITHUB_TOKEN`-style credentials.
- [x] Added mocked GitHub search tests for registration, repository/code/issue endpoint selection, request headers, result conversion, and parse failure.
- [x] Borrowed `private/ytrix` Webshare pacing ideas into shared HTTP request policy: proxy-specific timeout, retries, retry delay, jittered minimum request delay, and max-parallelism configuration.
- [x] Fixed provider-registry credential leakage so catalog API-key env vars cannot bleed from one registered engine class into another.
- [x] Added CLI `--explain` metadata for selected/skipped engines, proxy policy, retries, provider errors, and LLM steps.
- [x] Added `twat-search web q --jsonl` output with request, engine, result,
  failure, answer, and optional explain records for streaming consumers.
- [x] Added explicit `providers`, `routes`, `doctor`, and proxy-aware `fetch`
  CLI commands over the provider catalog, route presets, local config readiness
  checks, and URL fetch diagnostics.
- [x] Audited tracked Python source and test files for matching `this_file` headers and fixed missing legacy headers.
- [x] Removed stale `REVIEW/` generated review artifacts and the superseded Google Falla debug runner.
- [x] Replaced Falla-first public comments/docs with provider-neutral browser-engine language while preserving legacy aliases.
- [x] Added typed browser runtime configuration inspired by `private/crapi` for backend/type/headless/stealth/profile/locale/timezone/viewport/failure-evidence settings.
- [x] Added browser config env-var loading and offline tests for Playwright launch/context kwargs with proxy injection.
- [x] Added offline browser-engine coverage for Playwright context proxy injection and explicit browser/context teardown.
- [x] Reused the `private/abersetz` offline-test pattern for browser runtime tests that do not import Playwright or touch the network.
- [x] Added a `private/flchimp`-style public API docstring gate for web config and response model boundary classes.
- [x] Reviewed `private/TO_INTEGRATE.md` targets and borrowed the safest immediate patterns: qBittorrent-style small external adapters, GitHub dork query templates, and deep-search routing as a future orchestration layer.
- [x] Added `plugin_search`, a template-driven plugin engine that expands configured query templates into normalized external search results without executing plugin code.
- [x] Added a `plugins` route preset and provider metadata for template search plugins.
- [x] Added offline plugin-search tests for registry integration, template validation, dork-style query expansion, result limiting, and route selection.
- [x] Added provider-neutral browser diagnostics for CAPTCHA, bot challenge, rate limit, generic block, consent, and login detection.
- [x] Added browser failure evidence helpers that respect configured HTML and screenshot capture settings.
- [x] Added local browser HTML fixtures for CAPTCHA and consent states so browser handling can be tested before live pages.
- [x] Carried browser challenge evidence through `search_detailed()` as structured `SearchFailure.details`.
- [x] Wired legacy Falla Playwright fetch paths into `BrowserChallengeError`
  evidence so real browser engines can report block/consent artifacts instead
  of returning silent empty results.
- [x] Added API-level failure-kind tests for auth, timeout, block/CAPTCHA,
  parse, schema drift, and generic provider errors.
- [x] Removed CLI startup warnings from optional scraper/browser import paths
  and added regression coverage that `twat search web info --json` matches
  `twat-search web info --json`.
- [x] Added an explicitly gated live Brave CLI smoke test using
  `RUN_TWAT_SEARCH_LIVE_TESTS=1` plus `BRAVE_API_KEY`.
- [x] Added provider sweep command coverage that uses `twat-search web
  info --plain` as the authoritative engine list for per-engine smoke commands.
- [x] Added mocked response coverage for the remaining legacy/current API
  engines: Brave web/news, Critique, HasData full/light, SerpAPI, Perplexity,
  Tavily, and You web/news.
- [x] Added a provider-catalog coverage guard so every implemented API engine
  must appear in the mocked-response coverage set.
- [x] Wired shared Webshare-style proxy settings into request-mode bundled
  scrapers so Mojeek-style Falla adapters use the same timeout, retry, and
  `requests` proxy policy as API engines.
- [x] Added typed provider `route_priority` metadata and made route selection
  order engines by provider metadata instead of catalog/string order.
- [x] Added typed route-selection decisions with shared skip reasons for CLI
  route records and `--explain` output.
- [x] Attached typed `EngineRequest` provenance to every `EngineOutcome` so
  each provider attempt records its concrete query, route, and parsed params.
- [x] Added provider-catalog transport context enrichment so detailed outcomes
  expose transport kind, proxy policy, proxy transport, browser requirement,
  and result-kind metadata without leaking those fields into provider kwargs.
- [x] Split executable transport concerns into dedicated API, scraper, browser,
  and LLM transport modules while preserving the existing engine request
  boundary.
- [x] Replaced public `*_falla` browser provider codes with canonical
  `*_browser` codes while retaining the old names only as useful catalog
  aliases.
- [x] Wired standalone DuckDuckGo and Google scraper engines to consume the
  shared request-policy `proxy_url` used by Webshare-style proxy config.
- [x] Routed Bing scraper HTML fetching through the shared scraper transport
  when a request-policy proxy URL is configured, while preserving the direct
  `scrape-bing` path for unproxied searches.
- [x] Promoted route presets into a frozen typed `RoutePolicy` request model so
  `SearchRequest`, CLI route records, and `--explain` output expose the parsed
  policy that selected provider engines.
- [x] Added typed `EngineExecutionContext` provenance so each engine attempt
  records final provider params and whether every param came from common,
  engine-specific, or passthrough inputs.
- [x] Added typed shared `RequestPolicy`/`RequestPolicyConfig` for non-proxy
  and proxy-overridden timeout, retry, delay, max-parallelism, user-agent, and
  proxy URL behavior across API/scraper engine calls.
- [x] Added typed `ResultProcessingPolicy`/`ResultProcessingConfig` for
  aggregate URL deduplication, normalized duplicate keys, max-result limits,
  response provenance, and CLI explain metadata.
- [x] Replaced the raw engine registry internals with typed
  `EngineRegistryEntry` records that attach provider catalog metadata,
  concrete engine classes, auth env vars, transport, proxy policy, result
  kinds, and catalog status while preserving compatibility class lookup.
- [x] Added typed `EngineParameterSet` parsing so each `EngineRequest`
  carries grouped common, engine-specific, and passthrough params with
  per-param provenance through `EngineExecutionContext` and CLI explain output.
- [x] Removed raw noncanonical engine-name fallbacks from engine config and
  registry lookup while preserving useful hyphen-to-underscore CLI aliases.
- [x] Removed the old non-strict fallback that broadened a failed route into
  arbitrary registered engines outside the selected route policy.
- [x] Moved shared HTTPX execution into `transports.py` so API and scraper
  engines share one timeout, retry, delay, user-agent, and proxy transport path.
- [x] Migrated the SerpAPI engine off direct `httpx.AsyncClient` usage and onto
  the shared transport-backed `make_http_request()` path.
