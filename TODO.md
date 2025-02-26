---
this_file: TODO.md
---

# twat-search Web Package - Future Tasks

The basic implementation of the `twat-search` web package is complete.

Tip: Periodically run `./cleanup.py status` to see results of lints and tests.

Edit the detailed plan in this file @TODO.md. Based on the plan, write an itemized list of tasks in @PROGRESS.md and then, as you work, check off your @PROGRESS.md.  

## 1. TODO

## 2. Project Status

The basic implementation of the `twat-search` web package is complete. This multi-provider search tool now supports multiple search engines and has a functional CLI interface.

## 3. Problem case

Based on the test command:
```bash
for engine in $(twat-search web info --plain); do echo; echo; echo; echo ">>> $engine"; twat-search web q -e $engine "Adam Twardoch" -n 1 --json; done;
```

## 4. JSON test results

----



----

## 5. Updated Summary Based on Latest Test Results

After implementing several fixes, the following issues remain:

1. **Remove anywebsearch engines**: All anywebsearch-based engines (bing_anyws, brave_anyws, google_anyws, qwant_anyws, yandex_anyws) need to be completely removed from the codebase as they're not functioning and are returning empty results.

2. **num_results parameter not respected**: Several engines still don't respect the `-n 1` parameter:
   - ~~bing_scraper~~ FIXED: Now properly respects num_results parameter
   - brave: still returns multiple results despite our fixes
   - ~~duckduckgo~~ FIXED: Now properly respects num_results parameter

3. **Failing engines**: Some engines that previously worked are now failing:
   - google_serpapi: Returns "No search engines could be initialized"
   - SerpAPI integration needs to be fixed
   - you and you_news engines are not working

4. **~~Fallback issues~~**: 
   - ~~google_hasdata is still showing fallback results~~ FIXED: Now uses direct engine calls to prevent fallbacks

5. **searchit engines**: The searchit-based engines (bing_searchit, google_searchit, qwant_searchit, yandex_searchit) are returning empty results and may need review or removal.

## 6. 5.1 Revised Plan

Based on the tests and fixes so far, here is a revised, prioritized plan:

1. **Critical fixes first**
   - ✅ Fix SerpAPI integration (_convert_safe function fixed)
   - ✅ Fix Bing Scraper to respect num_results
   - ✅ Modify main search function to use strict_mode=True by default
   - ✅ Update convenience functions to use direct engine calls

2. **Cleanup unnecessary code**
   - 🔄 Remove all anywebsearch-based engines
   - 🔄 Review searchit engines and either fix or remove them

3. **Fix remaining engine issues**
   - 🔄 Debug and fix You.com engines
   - ✅ Fix Google HasData engines to prevent fallbacks
   - 🔄 Fix Brave engine to respect num_results
   - 🔄 Debug and fix Perplexity (pplx) implementation
   - 🔄 Debug and fix Brave News implementation

4. **Testing and verification**
   - 🔄 Add tests for num_results parameter
   - 🔄 Add tests for proper source attribution
   - 🔄 Add tests for checking no fallbacks occur

5. **Documentation**
   - 🔄 Update documentation with known issues and solutions
   - 🔄 Document engine-specific requirements and limitations

Legend:
- ✅ Completed
- 🔄 In progress/pending

## 7. Detailed plan

### 7.1. Fix non-functioning engines

1. **Investigate Module Import Issues**
   - Check engine module import process in `src/twat_search/web/engines/__init__.py`
   - Verify that all required dependencies are being handled properly
   - Fix error handling in imports to provide better debug information

2. **Review API Key and Authentication**
   - Verify environment variable handling for API keys in `config.py`
   - Improve error messaging when API keys are missing
   - Add debug logs to show which API keys are being loaded

3. **Fix Engine-Specific Implementation Issues**
   - Review and fix implementation of anywebsearch engines (bing_anyws, brave_anyws, etc.)
   - Fix searchit engines implementation (bing_searchit, google_searchit, etc.)
   - Review and fix Perplexity (pplx) implementation

### 7.2. Fix num_results parameter handling

1. **Fix parameter passing in main API**
   - Review `search()` function in `api.py` to ensure num_results is correctly passed to engines
   - Fix parameter extraction in `get_engine_params()` function

2. **Fix parameter handling in individual engines**
   - ✅ Review and fix DuckDuckGo engine's num_results handling
   - Fix Google Scraper implementation to properly limit results
   - ✅ Ensure Tavily engine respects the num_results parameter

### 7.3. Fix unintended fallback behavior

1. **Review search fallback logic**
   - ✅ Analyze fallback mechanism in `api.py` that might be causing unintended behavior
   - ✅ Fix google_hasdata and google_hasdata_full implementations to prevent implicit fallbacks
   - ✅ Add option to explicitly disable fallbacks

### 7.4. Fix source attribution in results

1. **Fix engine source in result objects**
   - Review result creation in engines to ensure correct source attribution
   - Fix You.com and SerpAPI engines to return correct source in results
   - Add verification step to ensure engine_code is properly set

### 7.5. Add comprehensive tests

1. **Develop specific tests for each issue**
   - Create test for num_results parameter handling across all engines
   - Develop test for proper source attribution in results
   - Implement test for verifying no unintended fallbacks occur

### 7.6. Documentation and logging improvements

1. **Enhance logging**
   - Add more verbose logging to help diagnose engine issues
   - Improve error messages for common failure cases

2. **Update documentation**
   - Document common issues and solutions
   - Update engine-specific documentation with requirements and limitations

This plan addresses all the identified issues while improving the overall robustness and usability of the package.
