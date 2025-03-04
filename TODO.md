--- 
this_file: TODO.md
--- 

# TODO

Tip: Periodically run `./cleanup.py status` to see results of lints and tests.

This is the test command that we are targeting: 

```bash
for engine in $(twat-search web info --plain); do echo; echo; echo; echo ">>> $engine"; twat-search web q -e $engine "Adam Twardoch" -n 1 --json --verbose; done;
```

## High Priority

### Phase 1: Fix Falla-based Search Engines

- [ ] Fix Yahoo and Qwant search engines
  - [ ] Update selectors in Yahoo implementation to match current page structure
  - [ ] Update selectors in Qwant implementation to match current page structure
  - [ ] Test with various search queries to ensure reliability
  - [ ] Handle consent pages and other interactive elements

- [ ] Fix Google and DuckDuckGo search engines
  - [ ] Update selectors in Google implementation to match current page structure
  - [ ] Update selectors in DuckDuckGo implementation to match current page structure
  - [ ] Implement proper handling of CAPTCHA challenges
  - [ ] Test with various search queries to ensure reliability

- [ ] Fix type errors in `google.py`:
  - [ ] Fix type error in `wait_for_selector` where `self.wait_for_selector` could be `None`
  - [ ] Fix type error in `find_all` where `attrs` parameter has incompatible type
  - [ ] Fix type error in `get_title`, `get_link`, and `get_snippet` where `elem` parameter has incompatible type
  - [ ] Fix type error in `elem.find` where `PageElement` has no attribute `find`

- [ ] Improve Falla integration with Playwright:
  - [ ] Ensure proper browser and context management for efficient resource usage
  - [ ] Implement specific exception handling for common Playwright errors
  - [ ] Return empty results on failure instead of raising exceptions
  - [ ] Add comprehensive type hinting throughout the codebase
  - [ ] Improve method docstrings for better code documentation

### Phase 2: Fix Critical Engine Failures

- [ ] Improve `get_engine` function and error handling
  - [ ] Add descriptive error messages when engines are not found or disabled
  - [ ] Handle engine initialization failures gracefully
  - [ ] Add comprehensive tests for engine initialization

- [ ] Fix engines returning empty results
  - [ ] Identify and address common failure patterns
  - [ ] Add detailed logging for debugging
  - [ ] Create test script to isolate issues

## Medium Priority

### Improve Code Quality

- [ ] Implement comprehensive error handling:
  - [ ] Add try-except blocks for all external API calls
  - [ ] Implement proper error logging with context information
  - [ ] Create custom exception classes for different error scenarios
  - [ ] Add graceful fallbacks for common error cases

- [ ] Improve test coverage:
  - [ ] Add unit tests for all search engine implementations
  - [ ] Add integration tests for the entire search pipeline
  - [ ] Implement mock responses for external API calls in tests
  - [ ] Add performance benchmarks for search operations

- [ ] Enhance documentation:
  - [ ] Add detailed docstrings to all classes and methods
  - [ ] Create comprehensive API documentation
  - [ ] Add usage examples for all search engines
  - [ ] Document configuration options and environment variables

### Standardize JSON Output Format

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

## Low Priority

### Feature Enhancements

- [ ] Add support for additional search engines:
  - [ ] Implement Ecosia search
  - [ ] Implement Startpage search
  - [ ] Implement other alternative search engines
  - [ ] Implement Qwant AI engine using the QwantAI package (https://pypi.org/project/QwantAI/)

- [ ] Enhance result processing:
  - [ ] Implement result deduplication across engines
  - [ ] Add result ranking based on relevance
  - [ ] Implement result filtering options
  - [ ] Add support for different result formats (HTML, Markdown, etc.)

- [ ] Improve CLI functionality:
  - [ ] Add interactive mode for search operations
  - [ ] Implement result pagination in CLI output
  - [ ] Add support for saving search results to file
  - [ ] Implement search history functionality

- [ ] Add advanced search features:
  - [ ] Implement image search capabilities
  - [ ] Add support for news search
  - [ ] Implement video search functionality
  - [ ] Add support for academic/scholarly search

- [ ] Optimize performance:
  - [ ] Implement caching for search results
  - [ ] Optimize concurrent search operations
  - [ ] Reduce memory usage during search operations
  - [ ] Implement timeout handling for slow search engines

## Completed Tasks

- [x] Setup and dependencies
  - [x] Create new module `src/twat_search/web/engines/falla.py`
  - [x] Add necessary dependencies to `pyproject.toml`
  - [x] Define engine constants in `src/twat_search/web/engine_constants.py`
  - [x] Update `src/twat_search/web/engines/__init__.py` to import and register new engines
  - [x] Create utility function to check if Falla is installed and accessible

- [x] Create base `FallaSearchEngine` class
  - [x] Inherit from `SearchEngine`
  - [x] Implement `search` method with proper error handling and retries
  - [x] Create fallback implementation for when Falla is not available

- [x] Implement specific Falla-based engines
  - [x] `google-falla`: Google search using Falla
  - [x] `bing-falla`: Bing search using Falla
  - [x] `duckduckgo-falla`: DuckDuckGo search using Falla
  - [x] `yahoo-falla`: Yahoo search using Falla
  - [x] `qwant-falla`: Qwant search using Falla
  - [x] And other engines (Aol, Ask, Dogpile, Gibiru, Mojeek, Yandex)

- [x] Fix linting errors in the codebase:
  - [x] Replace `os.path.abspath()` with `Path.resolve()` in `google.py`
  - [x] Replace `os.path.exists()` with `Path.exists()` in `google.py`
  - [x] Replace insecure usage of temporary file directory `/tmp` with `tempfile.gettempdir()` in `test_google_falla_debug.py`
  - [x] Replace `os.path.join()` with `Path` and the `/` operator in `test_google_falla_debug.py`
  - [x] Remove unused imports (`os` and `NavigableString`) from `google.py`

