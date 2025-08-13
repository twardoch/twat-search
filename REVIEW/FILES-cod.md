---
this_file: REVIEW/FILES-cod.md
title: Repository File Catalog and Tree
description: Catalog of all files/folders with a filesystem tree and short descriptions
---

# Repository Files Catalog

This document contains a complete dump of the repository tree and a concise description for every folder and file.

## Filesystem Tree

```
./.pre-commit-config.yaml
./CHANGELOG.md
./CLEANUP.txt
./LICENSE
./README.md
./REFACTOR_FILELIST.txt
./REPO_CONTENT.txt
./SETUP_CI_CD.md
./TODO.md
./VERSION.txt
./cleanup.py
./debug_fetch.py
./falla_search.py
./google_debug_Python_programming_language.html
./google_debug_test_query.html
./pyproject.toml
./pyproject_next.md
./pyproject_next.toml
./requirements.txt
./test_async_falla.py
./test_falla.py
./test_google_falla_debug.py
./test_simple.py
./test_sync_falla.py
./uv.lock
./resources
./resources/pricing.md
./resources/brave
./resources/brave/brave.md
./resources/brave/brave_image.md
./resources/brave/brave_news.md
./resources/brave/brave_video.md
./resources/pplx
./resources/pplx/pplx.md
./resources/pplx/pplx_urls.txt
./resources/you
./resources/you/you.md
./resources/you/you.txt
./resources/you/you_news.md
./resources/you/you_news.txt
./scripts
./scripts/build.sh
./scripts/release.sh
./scripts/test.sh
./src
./src/twat_search
./src/twat_search/__init__.py
./src/twat_search/__main__.py
./src/twat_search/paths.py
./src/twat_search/web
./src/twat_search/web/__init__.py
./src/twat_search/web/api.py
./src/twat_search/web/cli.py
./src/twat_search/web/config.py
./src/twat_search/web/engine_constants.py
./src/twat_search/web/exceptions.py
./src/twat_search/web/models.py
./src/twat_search/web/utils.py
./src/twat_search/web/engines
./src/twat_search/web/engines/__init__.py
./src/twat_search/web/engines/base.py
./src/twat_search/web/engines/bing_scraper.py
./src/twat_search/web/engines/brave.py
./src/twat_search/web/engines/critique.py
./src/twat_search/web/engines/duckduckgo.py
./src/twat_search/web/engines/falla.py
./src/twat_search/web/engines/google_scraper.py
./src/twat_search/web/engines/hasdata.py
./src/twat_search/web/engines/pplx.py
./src/twat_search/web/engines/serpapi.py
./src/twat_search/web/engines/tavily.py
./src/twat_search/web/engines/you.py
./src/twat_search/web/engines/lib_falla
./src/twat_search/web/engines/lib_falla/__init__.py
./src/twat_search/web/engines/lib_falla/main.py
./src/twat_search/web/engines/lib_falla/requirements.txt
./src/twat_search/web/engines/lib_falla/settings.py
./src/twat_search/web/engines/lib_falla/utils.py
./src/twat_search/web/engines/lib_falla/core
./src/twat_search/web/engines/lib_falla/core/__init__.py
./src/twat_search/web/engines/lib_falla/core/aol.py
./src/twat_search/web/engines/lib_falla/core/ask.py
./src/twat_search/web/engines/lib_falla/core/bing.py
./src/twat_search/web/engines/lib_falla/core/dogpile.py
./src/twat_search/web/engines/lib_falla/core/duckduckgo.py
./src/twat_search/web/engines/lib_falla/core/falla.py
./src/twat_search/web/engines/lib_falla/core/fetch_page.py
./src/twat_search/web/engines/lib_falla/core/gibiru.py
./src/twat_search/web/engines/lib_falla/core/google.py
./src/twat_search/web/engines/lib_falla/core/mojeek.py
./src/twat_search/web/engines/lib_falla/core/qwant.py
./src/twat_search/web/engines/lib_falla/core/searchencrypt.py
./src/twat_search/web/engines/lib_falla/core/startpage.py
./src/twat_search/web/engines/lib_falla/core/yahoo.py
./src/twat_search/web/engines/lib_falla/core/yandex.py
./tests
./tests/conftest.py
./tests/test_twat_search.py
./tests/unit
./tests/unit/__init__.py
./tests/unit/mock_engine.py
./tests/unit/web
./tests/unit/web/__init__.py
./tests/unit/web/test_api.py
./tests/unit/web/test_config.py
./tests/unit/web/test_exceptions.py
./tests/unit/web/test_models.py
./tests/unit/web/test_utils.py
./tests/unit/web/engines
./tests/unit/web/engines/__init__.py
./tests/unit/web/engines/test_base.py
```

## Catalog: Folders and Files

- .pre-commit-config.yaml: Pre-commit hooks configuration for formatting, linting and quality checks.
- CHANGELOG.md: Accumulated release notes and change history for the project.
- CLEANUP.txt: Notes/checklist for repository cleanup and maintenance tasks.
- LICENSE: Project license (permissive OSS license file).
- README.md: Main project documentation with usage, features, and technical overview.
- REFACTOR_FILELIST.txt: Helper list of files that were or should be refactored; planning aid.
- REPO_CONTENT.txt: Snapshot of repository contents for reference and auditing.
- SETUP_CI_CD.md: Documentation on CI/CD setup and GitHub Actions workflows.
- TODO.md: Top-level backlog and task list for future work.
- VERSION.txt: Plain-text version marker of the package.
- cleanup.py: Utility script to clean or normalize files in the repo (housekeeping tasks).
- debug_fetch.py: Debug helper to fetch/test responses during development.
- falla_search.py: Script for running Falla-based search (Playwright/scraping demo or debug).
- google_debug_Python_programming_language.html: Saved debug HTML result for Google testing.
- google_debug_test_query.html: Saved debug HTML for Google test queries (diagnostics).
- pyproject.toml: Python packaging, dependencies, and tool configuration (primary project config).
- pyproject_next.md: Narrative of the “next” pyproject iteration and rationale.
- pyproject_next.toml: Alternative/next-generation pyproject configuration proposal.
- requirements.txt: Pinned or minimal requirements for environments not using extras.
- test_async_falla.py: Legacy/standalone test targeting Falla async behavior.
- test_falla.py: Legacy test for Falla engine behavior.
- test_google_falla_debug.py: Debug/integration test for Google Falla flows.
- test_simple.py: Simple smoke/behavior test.
- test_sync_falla.py: Legacy synchronous Falla engine test.
- uv.lock: UV dependency lockfile.

- resources/: Project resources and reference docs for engines and pricing.
  - resources/pricing.md: Pricing notes for external services/APIs.
  - resources/brave/: Brave engine references and format notes.
    - resources/brave/brave.md: Brave web search API reference/notes.
    - resources/brave/brave_image.md: Brave image search API notes.
    - resources/brave/brave_news.md: Brave news search API notes.
    - resources/brave/brave_video.md: Brave video search API notes.
  - resources/pplx/: Perplexity engine references.
    - resources/pplx/pplx.md: Perplexity API usage and examples.
    - resources/pplx/pplx_urls.txt: Example URLs/inputs for Perplexity.
  - resources/you/: You.com engine references.
    - resources/you/you.md: You.com API usage and behavior.
    - resources/you/you.txt: Example queries/outputs for You.com.
    - resources/you/you_news.md: You.com news search documentation.
    - resources/you/you_news.txt: Example inputs/outputs for You.com news.

- scripts/: Utility shell scripts for common tasks.
  - scripts/build.sh: Build the package artifacts.
  - scripts/release.sh: Release helper for tagging and publishing.
  - scripts/test.sh: Run test suite locally/CI.

- src/: Python package source root.
  - src/twat_search/: Top-level package namespace.
    - src/twat_search/__init__.py: Package metadata and exposure of top-level symbols.
    - src/twat_search/__main__.py: Entry-point to run the package as a module (CLI bootstrap).
    - src/twat_search/paths.py: Shared path utilities/constants for locating resources.
    - src/twat_search/web/: Web search functionality (CLI, API, config, engines, models).
      - src/twat_search/web/__init__.py: Web subpackage initializer.
      - src/twat_search/web/api.py: High-level async search aggregator coordinating engines and results.
      - src/twat_search/web/cli.py: CLI implementation using Fire/Rich; exposes `twat-search web`.
      - src/twat_search/web/config.py: Pydantic settings and engine configuration management.
      - src/twat_search/web/engine_constants.py: Constants and identifiers for engines and defaults.
      - src/twat_search/web/exceptions.py: Custom exceptions for search/config errors.
      - src/twat_search/web/models.py: Pydantic data models, notably `SearchResult`.
      - src/twat_search/web/utils.py: Helpers for normalization, formatting, timing, etc.
      - src/twat_search/web/engines/: Pluggable engine implementations and registry.
        - src/twat_search/web/engines/__init__.py: Engine registry, discovery, standardization helpers.
        - src/twat_search/web/engines/base.py: Abstract base class and engine lifecycle logic.
        - src/twat_search/web/engines/bing_scraper.py: Bing results via scraping.
        - src/twat_search/web/engines/brave.py: Brave Search API engine.
        - src/twat_search/web/engines/critique.py: Critique engine (visual/textual search capability).
        - src/twat_search/web/engines/duckduckgo.py: DuckDuckGo engine (no API key required).
        - src/twat_search/web/engines/falla.py: Google Falla Playwright-based engine wrapper.
        - src/twat_search/web/engines/google_scraper.py: Direct Google scraping engine.
        - src/twat_search/web/engines/hasdata.py: HasData-powered Google engines.
        - src/twat_search/web/engines/pplx.py: Perplexity AI engine.
        - src/twat_search/web/engines/serpapi.py: SerpAPI-backed Google engine.
        - src/twat_search/web/engines/tavily.py: Tavily research-focused search API engine.
        - src/twat_search/web/engines/you.py: You.com web and news engines.
        - src/twat_search/web/engines/lib_falla/: Embedded Falla library for scraping support.
          - src/twat_search/web/engines/lib_falla/__init__.py: Falla package initializer.
          - src/twat_search/web/engines/lib_falla/main.py: Falla orchestrator/runner entry.
          - src/twat_search/web/engines/lib_falla/requirements.txt: Falla-specific dependency list.
          - src/twat_search/web/engines/lib_falla/settings.py: Falla settings and defaults.
          - src/twat_search/web/engines/lib_falla/utils.py: Falla utility functions.
          - src/twat_search/web/engines/lib_falla/core/: Falla core per-engine scrapers.
            - src/twat_search/web/engines/lib_falla/core/__init__.py: Core package initializer.
            - src/twat_search/web/engines/lib_falla/core/aol.py: AOL search scraper.
            - src/twat_search/web/engines/lib_falla/core/ask.py: Ask.com search scraper.
            - src/twat_search/web/engines/lib_falla/core/bing.py: Bing search scraper.
            - src/twat_search/web/engines/lib_falla/core/dogpile.py: Dogpile search scraper.
            - src/twat_search/web/engines/lib_falla/core/duckduckgo.py: DuckDuckGo scraper.
            - src/twat_search/web/engines/lib_falla/core/falla.py: Core helpers/flow for Falla.
            - src/twat_search/web/engines/lib_falla/core/fetch_page.py: Fetching and browser/page utilities.
            - src/twat_search/web/engines/lib_falla/core/gibiru.py: Gibiru search scraper.
            - src/twat_search/web/engines/lib_falla/core/google.py: Google search scraper logic.
            - src/twat_search/web/engines/lib_falla/core/mojeek.py: Mojeek search scraper.
            - src/twat_search/web/engines/lib_falla/core/qwant.py: Qwant search scraper.
            - src/twat_search/web/engines/lib_falla/core/searchencrypt.py: SearchEncrypt scraper.
            - src/twat_search/web/engines/lib_falla/core/startpage.py: Startpage scraper.
            - src/twat_search/web/engines/lib_falla/core/yahoo.py: Yahoo search scraper.
            - src/twat_search/web/engines/lib_falla/core/yandex.py: Yandex search scraper.

- tests/: Test suite for package-level and unit tests.
  - tests/conftest.py: Pytest fixtures and configuration.
  - tests/test_twat_search.py: High-level integration tests for `twat_search` package.
  - tests/unit/: Unit tests by module.
    - tests/unit/__init__.py: Marks unit test package.
    - tests/unit/mock_engine.py: Mock engine for testing engine interfaces.
    - tests/unit/web/: Unit tests for `web` subpackage.
      - tests/unit/web/__init__.py: Marks tests package.
      - tests/unit/web/test_api.py: Tests for search aggregation and concurrency.
      - tests/unit/web/test_config.py: Tests for configuration loading and validation.
      - tests/unit/web/test_exceptions.py: Tests for custom exception behavior.
      - tests/unit/web/test_models.py: Tests for data models and serialization.
      - tests/unit/web/test_utils.py: Tests for utility helpers.
      - tests/unit/web/engines/: Engine base/tests.
        - tests/unit/web/engines/__init__.py: Marks tests package.
        - tests/unit/web/engines/test_base.py: Tests for engine base class and lifecycle.

## Notes

- The `.github/workflows/` directory contains CI workflows (push/release templates and active push/release) to test, build, and publish the package. They integrate UV, pytest, coverage, and release steps.
- Top-level `test_*.py` files appear to be legacy/debug tests focused on Falla engines; the canonical tests live under `tests/`.
- `resources/` stores human-readable references for external engine APIs and behaviors used by the code in `src/twat_search/web/engines/`.

