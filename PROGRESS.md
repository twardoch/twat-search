---
this_file: PROGRESS.md
---

Consult @TODO.md for the detailed plan. Work through these items, checking them off as you complete them. Once a large part has been completed, update @TODO.md to reflect the progress.

# Task List

## 1. Implement Falla-based Search Engines

- [ ] Setup and dependencies
  - [ ] Create new module `src/twat_search/web/engines/falla.py`
  - [ ] Add necessary dependencies to `pyproject.toml` (selenium, lxml, requests)
  - [ ] Define engine constants in `src/twat_search/web/engine_constants.py`
  - [ ] Update `src/twat_search/web/engines/__init__.py` to import and register new engines
  - [ ] Create utility function to check if Falla is installed and accessible

- [ ] Create base `FallaSearchEngine` class
  - [ ] Inherit from `SearchEngine`
  - [ ] Define `FallaResult` Pydantic model for result validation
  - [ ] Implement abstract `_initialize_falla_engine` method
  - [ ] Create `_convert_result` method to convert Falla results to `SearchResult` objects
  - [ ] Implement `search` method with proper error handling and retries
  - [ ] Create fallback implementation for when Falla is not available

- [ ] Implement specific Falla-based engines
  - [ ] `google-falla`: Google search using Falla
    - [ ] Create `GoogleFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `bing-falla`: Bing search using Falla
    - [ ] Create `BingFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `duckduckgo-falla`: DuckDuckGo search using Falla
    - [ ] Create `DuckDuckGoFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `aol-falla`: AOL search using Falla
    - [ ] Create `AolFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `ask-falla`: Ask.com search using Falla
    - [ ] Create `AskFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `dogpile-falla`: DogPile search using Falla
    - [ ] Create `DogpileFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `gibiru-falla`: Gibiru search using Falla
    - [ ] Create `GibiruFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `mojeek-falla`: Mojeek search using Falla
    - [ ] Create `MojeekFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `qwant-falla`: Qwant search using Falla
    - [ ] Create `QwantFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `yahoo-falla`: Yahoo search using Falla
    - [ ] Create `YahooFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator
  - [ ] `yandex-falla`: Yandex search using Falla
    - [ ] Create `YandexFallaEngine` class
    - [ ] Implement `_initialize_falla_engine` method
    - [ ] Register with `@register_engine` decorator

- [ ] Implement robust error handling
  - [ ] Handle network errors gracefully
  - [ ] Detect and handle captchas
  - [ ] Implement rate limiting protection
  - [ ] Add fallback mechanisms for failed engines
  - [ ] Handle case when Falla is not available

- [ ] Implement Falla integration approach
  - [ ] Decide on integration approach (embedded vs. dependency)
  - [ ] If embedded:
    - [ ] Create simplified implementation of Falla core functionality
    - [ ] Implement key scraping methods
    - [ ] Ensure proper attribution and licensing
  - [ ] If dependency:
    - [ ] Add Falla as optional dependency in pyproject.toml
    - [ ] Create fallback for when Falla is not installed
    - [ ] Document installation requirements

## 2. Fix Critical Engine Failures

- [ ] Improve `get_engine` function and error handling
  - [ ] Add descriptive error messages when engines are not found or disabled
  - [ ] Handle engine initialization failures gracefully

- [ ] Add comprehensive tests for engine initialization
  - [ ] Test API key requirements
  - [ ] Test engine availability detection
  - [ ] Test disabled engine handling

## 3. Fix Data Integrity and Consistency Issues

- [ ] Fix source attribution in search results
  - [ ] Ensure all engines use `self.engine_code` when creating `SearchResult` objects
  - [ ] Fix typos in result keys (e.g., `"snippetHighlitedWords"`)

## 4. Address Empty Results

- [!] Fix `searchit`-based engines
  - [!] Fix `bing_searchit` returning empty results
  - [!] Fix `google_searchit` returning empty results
  - [!] Fix `qwant_searchit` returning empty results
  - [!] Fix `yandex_searchit` returning empty results
  - [ ] Verify proper installation and dependencies
  - [ ] Create test script to isolate issues
  - [ ] Add detailed logging for debugging
  - [ ] Fix implementation issues or remove if necessary

- [ ] Test and fix other engines with empty results
  - [ ] Identify and address common failure patterns

## 5. Improve CLI Interface

- [ ] Update the `q` command in the CLI
  - [ ] Test CLI with various parameter combinations

## 6. Enforce Consistent JSON Output Format

- [ ] Standardize JSON output across all engines
  - [ ] Utilize the existing `SearchResult` model consistently
  - [ ] Remove utility functions like `_process_results` and `_display_json_results`
  - [ ] Remove `CustomJSONEncoder` class
  - [ ] Update engine `search` methods to return list of `SearchResult` objects

- [ ] Update API function return types
  - [ ] Change return type to `list[SearchResult]`
  - [ ] Ensure proper handling of results from engines

- [ ] Update CLI display functions
  - [ ] Use `model_dump` for JSON serialization
  - [ ] Implement simplified result display

## 7. Testing and Documentation

- [!] Fix failing tests
  - [ ] Address test failures in `test_api.py`
  - [ ] Address test failures in `test_config.py`
  - [ ] Address test failures in `test_bing_scraper.py`

- [ ] Create comprehensive test suite
  - [ ] Test each engine individually
  - [ ] Test parameter handling
  - [ ] Test error conditions and recovery

- [ ] Enhance debug logging throughout the codebase
  - [ ] Add consistent logging in all engines
  - [ ] Improve error messages for common failure cases

- [ ] Update documentation
  - [ ] Document engine-specific requirements
  - [ ] Add troubleshooting guidelines
  - [ ] Document parameter handling

## 8. Tests

- [ ] Create comprehensive tests
  - [ ] Create unit tests for base `FallaSearchEngine` class
    - [ ] Test initialization
    - [ ] Test result conversion
    - [ ] Test error handling
  - [ ] Create unit tests for each Falla-based engine
    - [ ] Test initialization
    - [ ] Test search functionality with mocked responses
    - [ ] Test error handling
  - [ ] Create integration tests with limited scope
    - [ ] Test actual search functionality (skipped if Falla not available)
    - [ ] Test result formatting
  - [ ] Create test utility to verify all engines
    - [ ] Test all engines with a simple query
    - [ ] Verify results format

- [ ] Documentation and examples
  - [ ] Document installation requirements for Falla engines
  - [ ] Add usage examples to README
  - [ ] Document limitations and considerations
  - [ ] Add appropriate disclaimers regarding web scraping
  - [ ] Update CLI help text to include new engines

## 9. Final Verification

- [ ] Run test command on all engines
  - [ ] Verify correct output format
  - [ ] Verify proper parameter handling
  - [ ] Check for consistent error handling

- [x] Run linters and code quality tools
  - [x] Address all Ruff and Mypy issues
  - [ ] Run `cleanup.py status` regularly during development

- [ ] Verify full system functionality
  - [ ] Test with the problem case command
  - [ ] Ensure all engines return proper results
