---
this_file: PROGRESS.md
---

# twat-search Progress Report

## Project Status

The basic implementation of the `twat-search` web package is complete. This multi-provider search tool now supports multiple search engines and has a functional CLI interface.

## Completed
- [x] Defined common parameters in base `SearchEngine` class
- [x] Updated search engines to use unified parameters
- [x] Added support for multiple search engines (Brave, Tavily, Perplexity, You.com, SerpAPI, Critique, DuckDuckGo)
- [x] Implemented initial version of Bing Scraper engine
- [x] Created basic testing infrastructure
- [x] Fixed linting issues (`ruff check` now reports "All checks passed!")

## In Progress
- [ ] Fixing type checking issues identified by mypy (84 errors in 19 files)
  - Main issues include:
    - Missing positional arguments in function calls
    - Missing type annotations in function definitions
    - Attribute errors in RateLimiter class (no attributes 'call_timestamps', 'wait_if_needed')
    - Function call issues in config module (`_apply_env_overrides()` missing 'config_data' argument)
- [ ] Resolving critical issues with engines and parameter handling
  - `num_results` parameter not being respected across engines
  - API key detection issues in multiple engines
  - Failing scrapers returning no results
  - Unexpected engine fallback behavior
  - SearchEngine attribute inconsistencies
  - Config implementation test failures
- [ ] Addressing failing tests in test suite (13 failed, 30 passed, 6 errors)
- [ ] Fixing CLI functionality issues
  - `twat-search web info` command doesn't print any engines
  - Search commands fail with parameter errors

## Upcoming
- [ ] Adding comprehensive error handling
- [ ] Improving engine initialization process
- [ ] Standardizing parameter handling across all engines
- [ ] Enhancing testing and reliability
- [ ] Improving CLI usability and output formats
- [ ] Implementing configuration workflow for better user experience
- [ ] Addressing engine-specific fixes

## Critical Issues (From TODO.md)
1. **Fix `num_results` parameter not being respected**
   - Currently, specifying `-n 1` or `--num_results=1` is ignored and engines fetch more results
   - Root cause: Inconsistent parameter handling across engines

2. **Fix API key detection issues**
   - Multiple engines fail despite environment variables being set
   - Affected engines: `brave_anyws`, `brave_news`, `critique`, `google_serpapi`, `pplx`, `you`, `you_news`
   - Root cause: The `_apply_env_overrides()` function in config.py has a signature issue:
     - It's defined as `def _apply_env_overrides(self, config_data: dict[str, Any])` (with `self` parameter)
     - But it's called as `_apply_env_overrides(config_data)` (without `self`)
     - This prevents environment variables from being properly loaded into the config

3. **Fix failing scrapers with no results**
   - Several engines return no results: `bing_anyws`, `bing_searchit`, `google_anyws`, `google_searchit`, `qwant_anyws`, `qwant_searchit`

4. **Eliminate unexpected engine fallback behavior**
   - When a specified engine fails, the code sometimes falls back to other engines
   - Creates confusing output for users who expect specific engines

5. **Fix SearchEngine attribute inconsistencies**
   - Tests failing due to `name` attribute being expected but `engine_code` is used instead

6. **Resolve test failures in Config implementation**
   - Tests failing around default config values and environment variable loading
   - Key error: `_apply_env_overrides()` missing 1 required positional argument: 'config_data'
   - Same core issue as the API key detection problem - the function has incorrectly defined parameters

## Current Test Status
- **Total Tests**: 49 tests
- **Passed**: 30 tests
- **Failed**: 13 tests 
- **Errors**: 6 tests
- **Main Issues**:
  - Config initialization errors due to parameter issues in `_apply_env_overrides()`
  - RateLimiter class missing expected attributes/methods
  - Multiple parameter handling inconsistencies across engines

## CLI Issues
The following CLI commands are currently broken:

1. **Engine information not displayed**:
   ```
   twat-search web info 
   ```
   - The command doesn't print the engines at all

2. **Search functionality failing**:
   ```
   twat-search web q -e all "Adam Twardoch" -n 1 --json
   ```
   - Error trace shows multiple parameter issues:
     - `_apply_env_overrides() missing 1 required positional argument: 'config_data'`
     - `_display_errors() missing 1 required positional argument: 'error_messages'`
     - `_process_results() missing 1 required positional argument: 'results'`

These errors align with the mypy analysis showing missing parameters in function calls throughout the codebase.

## Development Notes
- Uses `uv` for Python package management
- Quality tools: ruff, mypy, pytest
- Clear provider protocol for adding new search backends
- Strong typing and runtime checks throughout

See [TODO.md](TODO.md) for the detailed task breakdown and implementation plans.

## Last Updated
2025-02-26
