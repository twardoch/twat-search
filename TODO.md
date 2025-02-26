# twat-search Web Package - Future Tasks

The basic implementation of the `twat-search` web package is complete.

Tip: Periodically run `./cleanup.py status` to see results of lints and tests.

## TODO

### Critical Issues

1. **Fix `num_results` parameter not being respected**
   - Currently, specifying `-n 1` or `--num_results=1` is ignored and engines fetch more results
   - Root cause: In `api.py`, the `num_results` param is passed to engine constructors, but many engines:
     - Override with their own defaults
     - Use different parameter names (`max_results`, `count`, etc.)
     - Have hardcoded minimums that override user preference
   - Fix:
     - Standardize parameter handling across all engines
     - Make sure constructors respect the passed `num_results` value
     - Update engine implementations to respect the limit even when calling external libraries

2. **Fix API key detection issues**
   - Multiple engines fail despite environment variables being set
   - Affected engines: `brave_anyws`, `brave_news`, `critique`, `google_serpapi`, `pplx`, `you`, `you_news`
   - Root cause: Likely incorrect environment variable loading or case sensitivity issues (note: we want to use load_dotenv() from python-dotenv)
   - Fix:
     - Debug environment variable loading in `config.py`
     - Add more logging to show which environment variables are detected/loaded
     - Ensure case sensitivity is handled correctly
     - Add explicit fallbacks for common API key name variations

3. **Fix failing scrapers with no results**
   - Several engines return no results: `bing_anyws`, `bing_searchit`, `google_anyws`, `google_searchit`, `qwant_anyws`, `qwant_searchit`
   - Root cause: Library-specific issues, timeouts, or blocking
   - Fix:
     - Add better error handling and diagnostics
     - Try using different timeouts, headers, or user agents
     - Improve robustness against temporary blocking
     - Implement circuit breakers for consistently failing engines

4. **Eliminate unexpected engine fallback behavior**
   - When a specified engine fails, the code sometimes falls back to other engines
   - This creates confusing output for users who expect specific engines
   - Fix:
     - Remove automatic fallback when a specific engine is requested
     - Only use fallbacks when no engine is explicitly specified
     - Add clear messages when specified engines fail

5. **Fix SearchEngine attribute inconsistencies**
   - Tests are failing due to `name` attribute being expected but `engine_code` is used instead
   - Root cause: Inconsistency between test expectations and implementation
   - Fix:
     - Either add `name` attribute to SearchEngine or update tests to use `engine_code`
     - Ensure consistency between base and derived classes
     - Fix MockSearchEngine implementation for tests

6. **Resolve test failures in Config implementation**
   - Tests failing around default config values and environment variable loading
   - Root cause: Tests expect empty engines by default, but code provides populated defaults
   - Fix:
     - Update tests to match actual implementation behavior
     - Fix environment variable parameter merging (env vars should replace, not merge with defaults)
     - Improve test isolation for environment variables

### Implementation Tasks

7. **Add comprehensive error handling**
   - Improve error messages to clearly indicate why an engine failed
   - Add more fine-grained error types that distinguish between:
     - API key issues
     - Network/connection problems
     - Rate limiting/blocking
     - Empty results (which may be legitimate)
   - Create a standard approach to logging that's consistent across engines

8. **Improve engine initialization process**
   - Create a more robust engine discovery and initialization process
   - Add capability tests for engines during initialization
   - Add a verbose debug mode that shows detailed initialization steps
   - Consider implementing a cache for engine availability status

9. **Standardize parameter handling**
   - Create consistent parameter names across all engines
   - Establish clear precedence rules for parameters:
     - Command line arguments
     - Environment variables
     - Config file defaults
   - Document each engine's parameter support and quirks

10. **Enhance testing and reliability**
    - Add automated tests for each engine
    - Create mock responses for offline testing
    - Implement retries with backoff for transient failures
    - Add circuit breaker patterns to fail fast for consistently failing engines
    - Fix existing test failures identified in test suite (7 failures)

### Code Quality Improvements

11. **Address linting issues**
    - Fix 263 errors reported by ruff
    - Remove unused imports throughout the codebase
    - Fix boolean parameter declarations (FBT001, FBT002 warnings)
    - Reduce function complexity and branches
    - Replace magic values with constants (PLR2004)
    - Fix parameter naming consistency (ARG002 unused arguments)

12. **Resolve type checking errors**
    - Fix 30 errors found by mypy
    - Add missing type annotations
    - Resolve attribute errors (`no attribute 'name'`, etc.)
    - Fix stubs for external libraries
    - Add proper typing for library imports

13. **Improve exception handling**
    - Use `raise ... from error` pattern for better error traceability
    - Ensure proper exception hierarchy is maintained
    - Add contextual information to exceptions
    - Implement consistent error messages across engines

### User Experience Improvements

14. **Improve CLI usability**
    - Add clearer error messages for common issues
    - Improve help text with more examples
    - Add command to test an engine's configuration
    - Implement a "dry run" mode that validates settings without performing searches

15. **Enhance output formats**
    - Fix JSON mode to properly handle errors
    - Add more structured output formats (CSV, YAML, etc.)
    - Improve the default display format for better readability
    - Add highlighting options for search terms

16. **Add configuration workflow**
    - Create a command to guide users through setting up API keys
    - Add a validation command to check which engines are properly configured
    - Implement a configuration wizard for new users
    - Add configuration profiles for different use cases

### Engine-Specific Fixes

17. **Brave API fix**
    - Debug why `BRAVE_API_KEY` isn't being recognized
    - Add clearer error messaging specific to Brave setup

18. **Fix scrapers**
    - Troubleshoot each failing scraper individually
    - Consider alternative libraries or approaches for consistently failing scrapers
    - Add custom user agents and request headers for problematic engines

19. **API key management**
    - Improve how API keys are discovered and validated
    - Add a command to test API keys without performing a search
    - Consider secure local storage options for API keys
    - Add key rotation support for services with usage limits
