---
this_file: PROGRESS.md
---

Consult @TODO.md for the detailed plan. Work through these items, checking them off as you complete them. Once a large part has been completed, update @TODO.md to reflect the progress.

# Task List

## 1. Fix Critical Engine Failures

- [x] Enhance `base.SearchEngine` class to enforce API key requirements
  - [x] Modify to require subclasses to define `env_api_key_names` as a class variable
  - [x] Add proper validation for engine code and API key requirements
  - [x] Centralize HTTP request handling with retries and error management

- [x] Enhance `config.py` for better API key handling
  - [x] Update `EngineConfig` to validate and require API keys as needed
  - [x] Improve error messages for missing API keys
  - [x] Add field validation for API keys

- [x] Update engine implementations correctly
  - [x] Fix You.com engines (`you` and `you_news`)
  - [x] Fix Perplexity (`pplx`) implementation
  - [ ] Fix SerpAPI integration
  - [ ] Ensure all engines implement proper API key handling

- [ ] Improve `get_engine` function and error handling
  - [ ] Add descriptive error messages when engines are not found or disabled
  - [ ] Handle engine initialization failures gracefully

- [ ] Add comprehensive tests for engine initialization
  - [ ] Test API key requirements
  - [ ] Test engine availability detection
  - [ ] Test disabled engine handling

## 2. Fix Data Integrity and Consistency Issues

- [!] Fix inconsistent `num_results` parameter handling
  - [x] Implement `_get_num_results` method in base class
  - [!] Implement proper result limiting in working engines (currently `-n 1` returns multiple results)
  - [!] Fix broken engines failing with "`object has no attribute 'get_num_results'`" error
    - [!] Fix `brave` engine implementation
    - [!] Fix `brave_news` engine implementation
    - [ ] Fix `critique` engine implementation
  - [ ] Ensure all engines properly handle and respect `num_results`
  - [ ] Add result limiting logic to all engine implementations

- [ ] Fix source attribution in search results
  - [ ] Ensure all engines use `self.engine_code` when creating `SearchResult` objects
  - [ ] Fix typos in result keys (e.g., `"snippetHighlitedWords"`)

- [!] Fix unwanted result combination in Google engines
  - [!] Fix `google_hasdata` engine returning results from other engines
  - [!] Fix `google_hasdata_full` engine returning results from other engines

## 3. Address Engine Reliability Issues (Empty Results)

- [!] Fix `searchit`-based engines
  - [!] Fix `bing_searchit` returning empty results
  - [!] Fix `google_searchit` returning empty results
  - [!] Fix `qwant_searchit` returning empty results
  - [!] Fix `yandex_searchit` returning empty results
  - [ ] Verify proper installation and dependencies
  - [ ] Create test script to isolate issues
  - [ ] Add detailed logging for debugging
  - [ ] Fix implementation issues or remove if necessary

- [!] Fix API key-based engines with initialization failures
  - [!] Fix `pplx` engine initialization
  - [!] Fix `you` engine initialization 
  - [!] Fix `you_news` engine initialization
  - [ ] Debug initialization failures and API key handling

- [ ] Test and fix other engines with empty results
  - [ ] Identify and address common failure patterns

## 4. Codebase Cleanup

- [ ] Remove all `anywebsearch` engines
  - [ ] Delete `src/twat_search/web/engines/anywebsearch.py`
  - [ ] Remove related imports from all files
  - [ ] Update engine constants and registration

- [x] Fix code duplication in `base.SearchEngine`
  - [x] Centralize common functionality
  - [x] Improve error handling consistency

## 5. Improve CLI Interface

- [ ] Update the `q` command in the CLI
  - [ ] Remove engine-specific parameters
  - [ ] Only use common parameters
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

## 8. Final Verification

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
