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
- Added optional post-fan-out LLM result reranking with per-result model, prompt-version, input-result, score, and rationale provenance.
- Added optional LLM answer synthesis with result URL citations and explicit source-failure preservation.
- Added offline fake-client tests for LLM chat request shape, response parsing, rewrite/rerank/synthesis fallback behavior, and search API wiring.
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
