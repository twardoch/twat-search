--- 
this_file: TODO.md
--- 

# twat-search 

Tip: Periodically run `./cleanup.py status` to see results of lints and tests.

Edit the detailed plan in this file @TODO.md. Based on the plan, write an itemized list of tasks in @PROGRESS.md and then, as you work, check off your @PROGRESS.md.  

This is the test command that we are targeting: 

```bash
for engine in $(twat-search web info --plain); do echo; echo; echo; echo ">>> $engine"; twat-search web q -e $engine "Adam Twardoch" -n 1 --json --verbose; done;
```

`twat-search` is an asynchronous Python package designed to query multiple search engines simultaneously, aggregate their results, and present them through a unified API and command-line interface (CLI). It aims for:

* **Multi-Engine Support:**  Integrate with various search providers (Brave, Google, Tavily, etc.).
* **Asynchronous Operation:** Utilize `asyncio` for concurrent requests and improved performance.
* **Configurability:** Allow users to configure engines, API keys, and search parameters via environment variables or configuration files.
* **Extensibility:**  Make it easy to add new search engine integrations.
* **Robustness:**  Handle errors gracefully, including API limits and network issues.
* **Consistency:**  Provide a consistent JSON output format for all engines.

## 1. Implementing Falla-based Search Engines

Based on the NEXTENGINES.md file, we've implemented search engines based on the [Falla project](https://github.com/Sanix-Darker/falla), which is a search engine scraper supporting multiple search engines.

### 1.1. Current Implementation Status

We have successfully integrated Falla-based search engines into the twat-search project. Key accomplishments include:

1. Created a `lib_falla` directory in `src/twat_search/web/engines/` containing the embedded Falla code
2. Developed a base `FallaSearchEngine` class and specific engine implementations for multiple search providers (Google, Bing, DuckDuckGo, etc.)
3. Added proper engine registration and configuration
4. Added necessary constants and imports for Falla engines
5. Fixed compatibility issues with the embedded Falla code

### 1.2. Remaining Implementation Tasks

#### 1.2.1. Fix Linting and Type Issues

1. Address remaining linter errors in the Falla implementation:
   - Fix type annotation issues with TypeVar usage in the `falla.py` file
   - Simplify the type system to avoid TypeVar complexity
   - Ensure proper type annotations throughout all Falla-based implementations

#### 1.2.2. Resolve Search Result Issues

1. Debug and fix issues with search results:
   - Implement better error logging for Falla engines returning empty results
   - Add detailed debugging for common failure patterns
   - Test each engine individually to identify specific issues

## 2. Fix Critical Engine Failures

### 2.1. Improve Error Handling and Reporting

1. Enhance `get_engine` function in `engines/__init__.py`:
   - Add descriptive error messages when engines fail to initialize
   - Improve error context for API key requirements
   - Implement better handling of disabled engines

2. Implement robust error handling for search operations:
   - Add proper retries with exponential backoff
   - Improve timeout handling
   - Better detection of rate limiting and captchas

### 2.2. Fix Failing Tests

1. Fix failing tests identified in PROGRESS.md:
   - Address test failures in `test_api.py`
   - Address test failures in `test_config.py` 
   - Address test failures in `test_bing_scraper.py`

## 3. Fix Data Integrity and Consistency Issues

### 3.1. Standardize Result Format

1. Ensure consistent source attribution in all search results:
   - Fix all engines to use `self.engine_code` when creating `SearchResult` objects
   - Correct typos in result keys (e.g., `"snippetHighlitedWords"`)
   - Standardize field names across all engines

## 4. Address Empty Results

### 4.1. Fix Searchit-based Engines

1. Debug and fix engines returning empty results:
   - `bing_searchit`
   - `google_searchit`
   - `qwant_searchit`
   - `yandex_searchit`

2. Improve implementation:
   - Create test script to isolate specific issues
   - Add detailed logging for debugging
   - Verify proper installation and dependencies

### 4.2. Implement Fallback Mechanisms

1. Create fallback mechanisms for unreliable engines:
   - Implement alternative parsing methods
   - Add fallbacks when primary parsing fails
   - Consider caching successful results for improved reliability

## 5. Improve CLI Interface

### 5.1. Enhance User Experience

1. Update and improve the `q` command in the CLI:
   - Add better progress indicators
   - Improve error messaging
   - Test all parameter combinations

### 5.2. Add Engine Management

1. Implement engine management commands:
   - Add commands to test specific engines
   - Add commands to enable/disable engines
   - Add commands to view detailed engine status

## 6. Enforce Consistent JSON Output Format

### 6.1. Standardize JSON Output

1. Enforce consistent JSON format across all engines:
   - Use `SearchResult` model consistently
   - Remove utility functions like `_process_results` and `_display_json_results`
   - Remove `CustomJSONEncoder` class
   - Update all engine `search` methods to return properly formatted results

2. Update API function return types:
   - Change return type to `list[SearchResult]`
   - Ensure proper handling of results from all engines

## 7. Testing and Documentation

### 7.1. Expand Test Coverage

1. Implement comprehensive tests:
   - Add unit tests for all `FallaSearchEngine` implementations
   - Create integration tests for end-to-end functionality
   - Add tests for error handling and recovery

### 7.2. Enhance Documentation

1. Improve documentation:
   - Document installation requirements for all engines
   - Add troubleshooting guidelines
   - Update CLI help text to include new engines
   - Add appropriate disclaimers for web scraping

## 8. Final Verification

1. Run verification on all engines:
   - Test with the problem case command
   - Verify correct output format
   - Ensure proper parameter handling
   - Check for consistent error handling
