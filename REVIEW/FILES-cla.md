# FILES-cla.md
# File Catalog for twat-search Repository

This document provides a comprehensive catalog of all files and folders in the twat-search repository, organized by purpose and functionality.

## Repository Structure Overview

The `twat-search` is a Python package that provides web search capabilities as a plugin for the twat framework. It implements a multi-engine search aggregator with support for various search engines including Brave, DuckDuckGo, Google, Bing, and others through different integration methods (APIs, scraping, browser automation).

## Root Level Files

### Configuration & Setup Files
- **`pyproject.toml`** - Main project configuration file using modern Python packaging standards (Hatch). Defines dependencies, build system, development environments, optional engine dependencies, and tool configurations for linting/testing.
- **`requirements.txt`** - Legacy requirements file (likely for backward compatibility).
- **`uv.lock`** - Lock file for uv package manager ensuring reproducible builds.

### Documentation Files
- **`README.md`** - Comprehensive project documentation including installation, usage examples, API documentation, architecture overview, and contribution guidelines.
- **`CHANGELOG.md`** - Version history and release notes documenting changes over time.
- **`TODO.md`** - Detailed task tracking with phases for fixing Falla engines, type errors, code quality improvements, and feature enhancements.
- **`LICENSE`** - MIT license file.

### Project Management Files
- **`VERSION.txt`** - Simple version tracking file.
- **`CLEANUP.txt`** - Instructions or notes about code cleanup processes.
- **`REFACTOR_FILELIST.txt`** - List of files that may need refactoring.
- **`REPO_CONTENT.txt`** - Repository content overview or manifest.
- **`SETUP_CI_CD.md`** - CI/CD setup documentation and configuration notes.

### Utility Scripts
- **`cleanup.py`** - Python utility script for code cleanup and maintenance tasks.
- **`debug_fetch.py`** - Debug utility for testing fetch operations.
- **`falla_search.py`** - Standalone script for testing Falla search functionality.

### Test Files (Root Level)
- **`test_async_falla.py`** - Asynchronous tests for Falla search engines.
- **`test_falla.py`** - General tests for Falla functionality.
- **`test_google_falla_debug.py`** - Specific debug tests for Google Falla implementation.
- **`test_simple.py`** - Simple/basic functionality tests.
- **`test_sync_falla.py`** - Synchronous tests for Falla search engines.

### Debug Output Files
- **`google_debug_Python_programming_language.html`** - HTML debug output from Google search testing.
- **`google_debug_test_query.html`** - HTML debug output from test query execution.

### Legacy Configuration
- **`pyproject_next.md`** - Documentation for next version of pyproject.toml.
- **`pyproject_next.toml`** - Next version configuration file (development/planning).

## Main Source Code (`src/twat_search/`)

### Package Root
- **`__init__.py`** - Package initialization with version handling and twat_cache configuration.
- **`__main__.py`** - Entry point for running the package as a module (`python -m twat_search`).
- **`paths.py`** - Path utilities for cache directories and file management.

### Web Search Module (`src/twat_search/web/`)

#### Core API & Configuration
- **`api.py`** - Main search API implementation with async search orchestration, engine management, and result aggregation.
- **`cli.py`** - Command-line interface implementation using Fire and Rich for user interaction.
- **`config.py`** - Configuration management using Pydantic for settings, environment variables, and engine configuration.
- **`models.py`** - Pydantic data models for search results and API responses.
- **`utils.py`** - Utility functions for the web search module.
- **`exceptions.py`** - Custom exception classes for error handling.
- **`engine_constants.py`** - Constants and mappings for all supported search engines.

#### Search Engines (`src/twat_search/web/engines/`)

##### Core Engine Framework
- **`__init__.py`** - Engine discovery, registration, and availability checking with graceful import handling.
- **`base.py`** - Abstract base class defining the SearchEngine interface and registration system.

##### API-Based Engines
- **`brave.py`** - Brave Search API integration (web and news search).
- **`tavily.py`** - Tavily AI-powered search API integration.
- **`pplx.py`** - Perplexity AI search API integration.
- **`you.py`** - You.com search API integration (web and news).
- **`critique.py`** - Critique search API integration.
- **`serpapi.py`** - Google search via SerpAPI integration.
- **`hasdata.py`** - HasData API integration for Google search.

##### Scraping-Based Engines
- **`duckduckgo.py`** - DuckDuckGo search using duckduckgo-search library.
- **`bing_scraper.py`** - Bing search using scrape-bing library.
- **`google_scraper.py`** - Direct Google search scraping (less reliable).

##### Browser Automation Engines (`lib_falla/`)
- **`falla.py`** - Main Falla implementation using Playwright for browser automation.

###### Falla Core (`lib_falla/core/`)
- **`__init__.py`** - Core Falla module initialization.
- **`falla.py`** - Main Falla search engine implementation.
- **`fetch_page.py`** - Page fetching utilities for browser automation.

###### Individual Search Engine Implementations
- **`google.py`** - Google search via browser automation.
- **`bing.py`** - Bing search via browser automation.
- **`duckduckgo.py`** - DuckDuckGo search via browser automation.
- **`yahoo.py`** - Yahoo search via browser automation.
- **`qwant.py`** - Qwant search via browser automation.
- **`aol.py`** - AOL search via browser automation.
- **`ask.py`** - Ask.com search via browser automation.
- **`dogpile.py`** - Dogpile search via browser automation.
- **`gibiru.py`** - Gibiru search via browser automation.
- **`mojeek.py`** - Mojeek search via browser automation.
- **`searchencrypt.py`** - SearchEncrypt via browser automation.
- **`startpage.py`** - Startpage search via browser automation.
- **`yandex.py`** - Yandex search via browser automation.

###### Falla Configuration & Utilities
- **`main.py`** - Main Falla execution entry point.
- **`requirements.txt`** - Falla-specific dependencies.
- **`settings.py`** - Falla configuration settings.
- **`utils.py`** - Falla utility functions.

## Testing Infrastructure (`tests/`)

### Test Configuration
- **`conftest.py`** - Pytest configuration and shared fixtures.

### Main Tests
- **`test_twat_search.py`** - Main integration tests for the package.

### Unit Tests (`tests/unit/`)
- **`__init__.py`** - Unit test package initialization.
- **`mock_engine.py`** - Mock search engine for testing purposes.

#### Web Module Unit Tests (`tests/unit/web/`)
- **`__init__.py`** - Web unit tests initialization.
- **`test_api.py`** - API function unit tests.
- **`test_config.py`** - Configuration management tests.
- **`test_exceptions.py`** - Exception handling tests.
- **`test_models.py`** - Data model tests.
- **`test_utils.py`** - Utility function tests.

#### Engine Unit Tests (`tests/unit/web/engines/`)
- **`__init__.py`** - Engine tests initialization.
- **`test_base.py`** - Base engine class tests.

## Build & Development Scripts (`scripts/`)

### Development Automation
- **`build.sh`** - Comprehensive build script with quality checks, testing, and packaging.
- **`test.sh`** - Advanced testing script with parallel execution, coverage, and benchmarking.
- **`release.sh`** - Release automation with version management and publishing.

## Resources & Documentation (`resources/`)

### Search Engine Documentation
- **`pricing.md`** - Pricing information for various search APIs.

#### Engine-Specific Resources
- **`brave/`** - Brave Search API documentation and examples.
  - **`brave.md`** - General Brave Search documentation.
  - **`brave_image.md`** - Brave Image Search documentation.
  - **`brave_news.md`** - Brave News Search documentation.
  - **`brave_video.md`** - Brave Video Search documentation.

- **`pplx/`** - Perplexity AI documentation.
  - **`pplx.md`** - Perplexity API documentation.
  - **`pplx_urls.txt`** - List of relevant Perplexity URLs.

- **`you/`** - You.com search documentation.
  - **`you.md`** - You.com API documentation.
  - **`you.txt`** - Additional You.com notes.
  - **`you_news.md`** - You.com News API documentation.
  - **`you_news.txt`** - You.com News notes.

## Debug Output (`debug_output/`)

### Search Engine Debug Files
- **`qwant_analysis.txt`** - Analysis output from Qwant search testing.
- **`qwant_content.html`** - Raw HTML content from Qwant search.
- **`qwant_screenshot.png`** - Screenshot from Qwant search testing.
- **`yahoo_analysis.txt`** - Analysis output from Yahoo search testing.
- **`yahoo_content.html`** - Raw HTML content from Yahoo search.
- **`yahoo_screenshot.png`** - Screenshot from Yahoo search testing.

## Architecture Summary

### Multi-Engine Design
The repository implements a sophisticated multi-engine search architecture with three main integration approaches:
1. **API-based engines** - Direct API integration with services like Brave, Tavily, SerpAPI
2. **Library-based scraping** - Using specialized libraries like duckduckgo-search
3. **Browser automation** - Using Playwright through the Falla framework for complex scraping

### Modular Structure
- Clean separation between API, CLI, configuration, and engine implementations
- Plugin-based architecture allowing easy addition of new search engines
- Comprehensive error handling and graceful fallbacks
- Async/await patterns for efficient concurrent searching

### Development Infrastructure
- Modern Python packaging with Hatch and uv
- Comprehensive testing with pytest, coverage, and benchmarking
- Code quality enforcement with Ruff, mypy, and pre-commit hooks
- CI/CD pipeline with multi-platform testing and automated releases

This architecture demonstrates professional Python development practices with emphasis on maintainability, extensibility, and robustness.