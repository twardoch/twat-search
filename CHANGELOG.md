---
this_file: CHANGELOG.md
---

# Changelog

All notable changes to this project will be documented in this file.

## Unreleased Changes

### Added
- Added an OpenAI-compatible LLM helper that posts chat completion requests for opt-in query rewriting without adding a new SDK dependency.
- Added LLM query-rewrite and result-rerank configuration for feature flags, temperature, token limit, and custom system prompts.
- Added optional pre-fan-out query rewriting in `search_detailed()` with original-query preservation and request provenance.
- Added optional LLM query decomposition before provider fan-out with capped, deduplicated subqueries and per-result query provenance.
- Added CLI `--explain` output for selected engines, skipped engines, proxy policy, retries, provider errors, and LLM step provenance.
- Added CLI `--jsonl` output for newline-delimited request, engine, result, failure, answer, and optional explain records.
- Added explicit CLI `providers`, `routes`, `doctor`, and proxy-aware `fetch` commands for catalog inspection and local readiness checks.
- Added missing `this_file` headers across tracked Python source and test modules.
- Removed stale generated review artifacts and the superseded Google Falla debug runner.
- Replaced Falla-first public comments and docs with provider-neutral browser-engine language while preserving legacy aliases.
- Added typed browser runtime configuration inspired by `private/crapi`, including backend/type/headless/stealth/profile/locale/timezone/viewport/failure-evidence settings.
- Added browser runtime environment variables and offline tests for Playwright launch/context kwargs with shared proxy injection.
- Added offline browser-engine coverage for Playwright launch kwargs, context proxy injection, and explicit browser/context teardown.
- Recorded the current verification result: `uvx hatch test` passed with 262 passed and 6 skipped after browser lifecycle coverage.
- Recorded the focused verification result: `uvx ruff check tests/unit/web/test_browser.py && uvx hatch test tests/unit/web/test_browser.py` passed with 7 passed and 1 skipped after browser lifecycle coverage.
- Added a `private/flchimp`-style public API docstring gate for web config and response model boundary classes.
- Added `plugin_search`, a template-driven plugin engine inspired by qBittorrent search plugins and GitHub dork tooling.
- Added provider metadata and a `plugins` route preset for template search plugins.
- Added offline plugin-search tests for registry integration, template validation, dork-style query expansion, result limiting, and route selection.
- Completed the stale Phase 3 GitHub/code search and plugin-style adapter checklist items after verifying the existing GitHub REST engine, code/issue/repository tests, plugin-search adapter, dork-style template expansion, and plugins route coverage.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/engines/test_github_search.py tests/unit/web/engines/test_plugin_search.py tests/unit/web/test_routes.py::test_plugins_route_selects_plugin_engines` passed with 14 passed after closing stale GitHub/plugin checklist items.
- Added provider-neutral browser diagnostics for CAPTCHA, bot challenge, rate limit, generic block, consent, and login detection.
- Added browser failure evidence helpers that write configured HTML and screenshot artifacts under a shared evidence contract.
- Added local browser HTML fixtures for CAPTCHA and consent states so browser handling can be tested before live search pages.
- Added `SearchFailure.details` and browser challenge error handling so `search_detailed()` preserves browser evidence as structured failure data.
- Fixed public browser engine wrappers so `BrowserChallengeError` propagates intact instead of being collapsed into a generic `EngineError`.
- Completed the Phase 3 browser-engine checklist item after verifying Playwright context creation, proxy injection, block/consent evidence, failure artifacts, structured API failures, and teardown coverage.
- Recorded the current verification result: `uvx hatch test` passed with 263 passed and 6 skipped after public browser challenge evidence propagation.
- Recorded the focused verification result: `uvx ruff check src/twat_search/web/engines/falla.py tests/unit/web/test_browser.py && uvx hatch test tests/unit/web/test_browser.py tests/unit/web/test_api.py::test_search_detailed_preserves_browser_failure_evidence` passed with 9 passed and 1 skipped after preserving public browser challenge evidence.
- Wired legacy Falla Playwright fetch paths into browser challenge evidence so CAPTCHA, bot challenge, rate-limit, and consent pages raise structured `BrowserChallengeError` failures instead of silent empty results.
- Added API-level failure-kind tests for auth, timeout, block/CAPTCHA, parse, schema drift, and generic provider errors.
- Added regression coverage proving `twat search web info --json` and `twat-search web info --json` return equivalent provider metadata.
- Added an explicitly gated live Brave CLI smoke test for `twat-search web q -e brave "Adam Twardoch" -n 1 --json --verbose`.
- Added provider sweep command coverage using `twat-search web info --plain` as the authoritative engine list.
- Added mocked response coverage for the remaining legacy/current API engines: Brave web/news, Critique, HasData full/light, SerpAPI, Perplexity, Tavily, and You web/news.
- Added a provider-catalog guard requiring every implemented API engine to appear in mocked-response coverage.
- Added shared proxy-policy wiring for request-mode bundled Falla scrapers so Mojeek-style adapters pass configured timeout, retries, and Webshare-compatible proxies into `requests`.
- Added typed provider `route_priority` metadata and made route selection order engines by provider metadata instead of catalog/string order.
- Added typed route-selection decisions with shared skip reasons for CLI route records and `--explain` output.
- Added typed `EngineRequest` provenance to each `EngineOutcome`, including fan-out query and parsed engine params.
- Added provider-catalog transport context enrichment for `EngineRequest`, exposing transport kind, proxy policy, proxy transports, browser requirement, and result kinds on detailed engine outcomes.
- Added a frozen typed `RoutePolicy` request model and exposed parsed route-policy metadata through `SearchRequest`, CLI route records, and `--explain` output.
- Added typed `EngineExecutionContext` provenance for final provider params and per-param source classification on detailed engine requests and CLI explain outcomes.
- Added typed `RequestPolicy`/`RequestPolicyConfig` for shared timeout, retry, delay, max-parallelism, random user-agent, and proxy override behavior across provider requests.
- Added typed `ResultProcessingPolicy`/`ResultProcessingConfig` for aggregate result deduplication, normalized duplicate keys, max-result limits, response provenance, and CLI explain metadata.
- Added typed `EngineRegistryEntry` records so the engine registry now joins concrete engine classes with provider catalog metadata, auth env vars, transport, proxy policy, result kinds, and catalog status.
- Added typed `EngineParameterSet` parsing so each provider attempt carries grouped common, engine-specific, and passthrough params with provenance through `EngineExecutionContext`, `EngineRequest`, and CLI explain output.
- Added dedicated API, scraper, browser, and LLM transport modules so provider execution is no longer concentrated in the neutral transport-context module.
- Added shared HTTPX API transport execution so API and scraper-compatible engines use one timeout, retry, delay, random user-agent, and proxy request path.
- Completed the Phase 3 current/API-key provider items after verifying implemented provider metadata and mocked-response coverage for current API engines plus Google CSE, Serper, DataForSEO, Exa, Firecrawl, Jina, Search1API, AISearch, Apify, and Gensee.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_provider_catalog.py tests/unit/web/engines/test_api_engine_fixtures.py` passed with 21 passed after closing stale Phase 3 API checklist items.
- Added canonical `*_browser` provider codes for bundled browser scrapers, with old `*_falla` spellings retained only as catalog aliases.
- Added shared request-policy proxy handoff for standalone DuckDuckGo and Google scraper engines.
- Added shared scraper-transport proxy routing for Bing scraper searches when a Webshare-style or explicit proxy URL is configured.
- Completed the proxy-aware scraper Phase 3 item for DuckDuckGo, Bing, Google, and bundled Qwant/Yahoo/Mojeek/Yandex request-mode scrapers.
- Recorded the current verification result: `uvx hatch test` passed with 261 passed and 6 skipped after Bing scraper proxy routing.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/engines/test_scraper_proxy.py` passed with 3 passed after Bing scraper proxy routing.
- Recorded the current verification result: `uvx hatch test` passed with 260 passed and 6 skipped after standalone scraper proxy wiring.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/engines/test_scraper_proxy.py tests/unit/web/test_config.py::test_request_policy_config_builds_effective_policy tests/unit/web/engines/test_base.py::test_make_http_request_uses_proxy_request_policy tests/unit/web/test_browser.py::test_falla_requests_fetch_uses_proxy_policy` passed with 5 passed after standalone scraper proxy wiring.
- Recorded the current verification result: `uvx hatch test` passed with 258 passed and 6 skipped after canonicalizing browser provider codes.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_provider_catalog.py tests/unit/web/test_routes.py tests/unit/web/test_cli_engine_info.py tests/unit/web/test_transports.py tests/unit/web/test_browser.py tests/unit/web/engines/test_base.py tests/unit/web/test_api.py` passed with 85 passed and 1 skipped after canonicalizing browser provider codes.
- Recorded the current verification result: `uvx hatch test` passed with 257 passed and 6 skipped after splitting API, scraper, browser, and LLM transport modules.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_transports.py tests/unit/web/engines/test_base.py tests/unit/web/test_llm.py tests/unit/web/test_browser.py tests/unit/web/engines/test_api_engine_fixtures.py::test_serpapi_search_converts_mocked_response` passed with 35 passed and 1 skipped after splitting API, scraper, browser, and LLM transport modules.
- Recorded the current verification result: `uvx hatch test` passed with 257 passed and 6 skipped after migrating SerpAPI to the shared transport-backed request path.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/engines/test_api_engine_fixtures.py::test_serpapi_search_converts_mocked_response tests/unit/web/test_transports.py tests/unit/web/engines/test_base.py` passed with 15 passed after migrating SerpAPI to the shared transport-backed request path.
- Recorded the current verification result: `uvx hatch test` passed with 257 passed and 6 skipped after shared HTTP transport extraction.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_transports.py tests/unit/web/engines/test_base.py` passed with 14 passed after shared HTTP transport extraction.
- Recorded the current verification result: `uvx hatch test` passed with 256 passed and 6 skipped after removing non-strict route fallback broadening.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_api.py` passed with 38 passed after removing non-strict route fallback broadening.
- Recorded the current verification result: `uvx hatch test` passed with 255 passed and 6 skipped after raw noncanonical engine-name fallback removal.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_api.py tests/unit/web/engines/test_base.py` passed with 47 passed after removing raw noncanonical engine-name fallbacks.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_api.py tests/unit/web/test_models.py tests/unit/web/test_cli_engine_info.py` passed with 56 passed after typed engine parameter parsing.
- Recorded the current verification result: `uvx hatch test` passed with 252 passed and 6 skipped after typed engine registry metadata.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/engines/test_base.py tests/unit/web/test_provider_catalog.py tests/unit/web/test_cli_engine_info.py` passed with 27 passed after typed engine registry metadata.
- Recorded the current verification result: `uvx hatch test` passed with 249 passed and 6 skipped after typed result-processing configuration.
- Recorded the focused verification result: `uvx hatch test tests/unit/web/test_config.py tests/unit/web/test_models.py tests/unit/web/test_api.py tests/unit/web/test_cli_engine_info.py` passed with 73 passed after typed result-processing configuration.
- Recorded the current verification result: `uvx hatch test` passed with 245 passed and 6 skipped after typed shared request-policy configuration.
- Recorded the current verification result: `uvx hatch test` passed with 243 passed and 6 skipped after typed engine execution context provenance.
- Recorded the current verification result: `uvx hatch test` passed with 241 passed and 6 skipped after typed route-policy request provenance.
- Recorded the current verification result: `uvx hatch test` passed with 239 passed and 6 skipped after provider transport context enrichment.
- Recorded the current verification result: `uvx hatch test` passed with 235 passed and 6 skipped after per-engine request provenance.
- Recorded the current verification result: `uvx hatch test` passed with 235 passed and 6 skipped after typed route-selection decisions.
- Recorded the current verification result: `uvx hatch test` passed with 234 passed and 6 skipped after provider route-priority metadata.
- Recorded the current verification result: `uvx hatch test` passed with 234 passed and 6 skipped after request-mode bundled scraper proxy wiring.
- Added optional post-fan-out LLM result reranking with per-result model, prompt-version, input-result, score, and rationale provenance.
- Added optional LLM answer synthesis with result URL citations and explicit source-failure preservation.
- Added offline fake-client tests for LLM chat request shape, response parsing, rewrite/rerank/synthesis fallback behavior, and search API wiring.
- Added injected fake-client tests for LLM rewrite/decomposition helpers so model-assisted search can be tested without patching HTTPX or touching the network.
- Added planned provider metadata for env-discovered LangSearch, MapleSERP, Search Cans, Bright Data, Browse AI, CaptureKit, and Decodo.
- Added a LangSearch Web Search API engine using `LANGSEARCH_API_KEY` and the shared HTTP request/proxy path.
- Added mocked LangSearch tests for registration, documented payload construction, result conversion, provider errors, and parse failures.
- Added a MapleSERP SERP API engine using `MAPLESERP_API_KEY` and the shared HTTP request/proxy path.
- Added mocked MapleSERP tests for registration, documented GET params, result conversion, auth failure, and parse failures.
- Added a SearchCans SERP API engine using `SEARCH_CANS_API_KEY` and the shared HTTP request/proxy path.
- Added mocked SearchCans tests for registration, documented payload construction, result conversion, provider errors, and parse failures.
- Added a Gensee Search Agent API engine using `GENSEE_SEARCH_API_KEY` and the shared HTTP request/proxy path.
- Added mocked Gensee tests for registration, documented GET params, result conversion, auth failure, and parse failures.
- Documented the `/Users/adam/.env.anon.txt` search-adjacent key classification in the 2.0 TODO.
- Added proxy-aware HTTP request policy wiring inspired by `private/ytrix`: configured proxies now pass timeout, retry count, retry delay, and jittered minimum request delay through the shared engine request path.
- Added environment overrides for proxy pacing: `TWAT_SEARCH_PROXY_TIMEOUT`, `TWAT_SEARCH_PROXY_RETRIES`, `TWAT_SEARCH_PROXY_RETRY_DELAY`, `TWAT_SEARCH_PROXY_MIN_DELAY`, and `TWAT_SEARCH_PROXY_MAX_PARALLELISM`.
- Added a GitHub REST API search engine using `GITHUB_API_TOKEN`/`GITHUB_TOKEN`-style credentials and the shared HTTP request/proxy path.
- Added mocked GitHub search tests for registration, repository/code/issue endpoints, request headers, result conversion, and parse failures.
- Added an Apify Google Search Scraper engine using `APIFY_API_KEY` and the shared HTTP request/proxy path.
- Added mocked Apify tests for registration, sync actor URL construction, actor input payloads, nested organic results, flat dataset items, and parse failures.
- Added an AISearch web-summary engine using `AISEARCH_API_KEY` and the shared HTTP request/proxy path.
- Added mocked AISearch tests for registration, documented payload construction, context validation, source-backed result conversion, and parse failures.
- Added a Search1API engine using `SEARCH1API_KEY` and the shared HTTP request/proxy path.
- Added mocked Search1API tests for registration, documented payload construction, bearer auth, result conversion, content snippets, and parse failures.
- Added a Jina AI search engine using `JINA_API_KEY` and the shared HTTP request/proxy path.
- Added mocked Jina tests for registration, encoded search URLs, bearer auth, flexible JSON wrappers, content snippets, and parse failures.
- Added a Firecrawl v2 Search API engine using `FIRECRAWL_API_KEY`/`FIRECRAWL_API_KEY_2` and the shared HTTP request/proxy path.
- Added mocked Firecrawl tests for registration, v2 search payloads, bearer auth, web result conversion, markdown snippets, and provider failures.
- Added `klepto` as a runtime dependency for persistent caching backend utilities.
- Added an Exa Search API engine using `EXAAI_API_KEY`/`EXA_API_KEY` and the shared HTTP request/proxy path.
- Added mocked Exa tests for registration, request payloads, result conversion, and parse failures.
- Added a DataForSEO live organic SERP engine using `DATAFORSEO_API_KEY` and the shared HTTP request/proxy path.
- Added mocked DataForSEO tests for registration, Basic auth, live SERP payloads, organic item conversion, and task failures.
- Added a Google Custom Search JSON API engine using `GOOGLE_CSE_API_KEY` plus `GOOGLE_CSE_ID`/`GOOGLE_CSE_CX`.
- Added mocked Google CSE engine tests for registration, required CSE ID, request params, item conversion, and parse failures.
- Added a Serper Google Search API engine using `SERPER_API_KEY` and the shared HTTP request/proxy path.
- Added mocked Serper engine tests for registration, auth failure, payload mapping, organic result conversion, and parse failures.
- Added `search_detailed()` with typed `SearchRequest`, `EngineRequest`, `SearchResponse`, `EngineOutcome`, and `SearchFailure` models.
- Added first-class provider failure data for empty results, initialization failures, provider exceptions, auth errors, timeouts, blocking, parse failures, and schema drift.
- Added catalog-backed route policies for `best`, `fast`, `cheap`, `resilient`, `deep`, `browser`, `api-only`, and `all`.
- Added route selection to programmatic search when `engines=None`.
- Added catalog-driven default engine configuration and generated engine env-var mappings.
- Added catalog selection helpers used by route/preset selection.
- Added a typed provider catalog with transport, status, credential, proxy, browser, rate, cost, stability, and result-kind metadata.
- Added planned 2.0 provider metadata for Gensee and Browser Use.
- Added catalog-backed CLI engine JSON metadata output.
- Added typed proxy and LLM configuration foundations for the 2.0 search refactor.
- Added Webshare-style proxy environment loading and URL builders for HTTPX and Playwright.
- Added HTTPX proxy handoff from global search configuration into engine requests.
- Added focused tests for proxy configuration, LLM readiness, and config environment loading.
- Recorded the current verification result: `uvx hatch test` passed with 233 passed and 6 skipped after the full API-engine mocked-response coverage slice.
- Added error handling in `init_engine_task` to prevent task cancellation issues
- Improved error messages for better debugging
- Added detailed logging for search engine initialization and execution
- Added check for empty engines list in `search` function, raising a `SearchError` with appropriate message
- Added proper handling of mock engine parameters, ensuring correct result count

### Changed
- Promoted LangSearch from planned provider metadata to an implemented, config-backed API engine.
- Promoted MapleSERP from planned provider metadata to an implemented, config-backed API engine.
- Promoted SearchCans from planned provider metadata to an implemented, config-backed API engine.
- Promoted Gensee from planned provider metadata to an implemented, config-backed API engine.
- Promoted GitHub search from planned provider metadata to an implemented, config-backed REST API engine.
- Promoted Apify from planned provider metadata to an implemented, config-backed actor API engine.
- Promoted AISearch from planned provider metadata to an implemented, config-backed API engine.
- Promoted Search1API from planned provider metadata to an implemented, config-backed API engine.
- Promoted Jina from planned provider metadata to an implemented, config-backed API engine.
- Promoted Firecrawl from planned provider metadata to an implemented, config-backed API engine.
- Promoted Exa from planned provider metadata to an implemented, config-backed API engine.
- Promoted DataForSEO from planned provider metadata to an implemented, config-backed API engine.
- Promoted Google CSE from planned provider metadata to an implemented, config-backed API engine.
- Promoted Serper from planned provider metadata to an implemented, config-backed API engine.
- Refactored `search()` to delegate through the detailed multi-engine response and flatten results only at the compatibility boundary.
- Removed raw noncanonical engine-name fallbacks from engine config lookup and registry lookup; hyphen-to-underscore normalization remains as the useful CLI alias path.
- Removed non-strict route fallback broadening so failed route initialization no longer silently queries arbitrary registered engines outside the selected route policy.
- Renamed public bundled browser engine classes, constants, route metadata, and helper functions from Falla-specific names to provider-neutral browser names.
- Moved shared HTTP request execution out of the base engine class and into the provider-neutral transport module.
- Split shared execution into dedicated transport modules: API HTTPX execution, synchronous scraper fetches, browser failure evidence, and OpenAI-compatible LLM chat transport.
- Migrated the SerpAPI engine from direct `httpx.AsyncClient` usage to the shared transport-backed `make_http_request()` path.
- Replaced config-time engine-registry imports with provider-catalog API-key metadata so CLI startup does not trigger optional engine circular imports.
- Updated CLI engine parsing so route names use catalog-backed route selection.
- Replaced hard-coded CLI `free` and `best` engine presets with catalog/availability filters.
- Derived legacy engine constants and friendly names from the provider catalog.
- Merged provider-catalog credential environment variables into registered engine classes.
- Rewrote `README.md` as the intended 2.0 package contract.
- Replaced legacy `TODO.md` with an actionable 2.0 cleanup, research, refactor, integration, and verification plan.
- Enhanced error handling in `get_engine` function to raise `SearchError` with correct message
- Improved mock engine handling in `search` function to properly set `result_count`
- Modified `Config` class to check for `_TEST_ENGINE` environment variable
- Enhanced `_parse_env_value` function to handle JSON strings for engine default parameters
- Added `BRAVE_DEFAULT_PARAMS` to `ENV_VAR_MAP` for proper configuration
- Standardized engine names for more consistent lookups
- Improved error handling patterns across the codebase

### Fixed
- Fixed optional scraper/browser import paths so missing optional dependencies no longer emit warnings during normal CLI startup.
- Fixed provider registry credential leakage by giving each registered engine subclass its own `env_api_key_names` list before catalog env vars are merged.
- Removed generated Python, pytest, ruff, and mypy cache directories from the repository tree.
- Fixed obsolete Falla/browser debug tests so missing optional Playwright dependencies skip instead of breaking collection.
- Fixed the Hatch test environment so async tests load `pytest-asyncio`.
- Fixed module help smoke coverage to accept Fire help output from stderr.
- Fixed issue with environment variable parsing for engine default parameters
- Fixed handling of empty engines list in search function
- Fixed mock engine result count handling
- Fixed error handling in `get_engine` function to use the correct exception type
- Fixed environment variable application to engine configurations

## 0.1.2 (2024-05-15)

### Fixed
- Fixed linting errors in `google.py` and `test_google_falla_debug.py`
- Replaced insecure usage of temporary file directory `/tmp` with `tempfile.gettempdir()`
- Replaced `os.path` functions with `pathlib.Path` methods for better path handling
- Removed unused imports (`os` and `NavigableString`) from `google.py`

## 0.1.1 (2024-05-10)

### Added
- Added support for Falla-based search engines
- Added refactored search engine initialization
- Added wrapper coroutine to handle exceptions during search process
- Added detailed logging for engine initialization and search processes

### Changed
- Improved error handling for search engines
- Enhanced configuration system
- Standardized engine names for more consistent lookups

## 0.1.0 (2024-05-01)

### Added
- Initial release
- Support for multiple search engines
- Asynchronous search capabilities
- Rate limiting
- Strong typing with Pydantic validation

### Changed
- Updated the `config.py` file to correctly import BaseSettings from the pydantic-settings package
- Updated the `pyproject.toml` file to add pydantic-settings as a dependency
- Updated the example usage in `example.py`
- Completed the implementation of the web search functionality as specified in TODO.md
- Planned comprehensive tests for the package

### 2024-02-25 - Initial Development

- Created initial project structure and files
- Created a preliminary TODO.md, PROGRESS.md, and research.txt

---
