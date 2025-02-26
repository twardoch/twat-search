---
this_file: PROGRESS.md
---

Consult @TODO.md for the detailed plan. Work through these items, checking them off as you complete them. Once a large part has been completed, update @TODO.md to reflect the progress.

# Task List

## 1. Fix non-functioning engines

- [ ] Fix API key and authentication issues
  - [ ] Review environment variable handling in `config.py`
  - [ ] Improve error messages for missing API keys
  - [ ] Add debug logging for API key loading process

- [ ] Address anywebsearch engines
  - [ ] Remove all anywebsearch-based engines from the codebase (bing_anyws, brave_anyws, google_anyws, qwant_anyws, yandex_anyws)
  - [ ] Update all relevant files to remove imports and references
  - [ ] Remove from engine constants and registration

- [ ] Fix searchit engines
  - [ ] Diagnose bing_searchit implementation issues
  - [ ] Diagnose google_searchit implementation issues
  - [ ] Diagnose qwant_searchit implementation issues
  - [ ] Diagnose yandex_searchit implementation issues

- [ ] Fix SerpAPI integration
  - [ ] Ensure proper initialization and API key handling
  - [ ] Test with valid API key

- [ ] Fix You.com engines
  - [ ] Debug you engine initialization issues
  - [ ] Debug you_news engine initialization issues
  - [ ] Verify API key handling

- [ ] Fix Perplexity (pplx) implementation
  - [ ] Review authentication process
  - [ ] Debug query handling and response parsing

- [ ] Fix Brave News implementation
  - [ ] Diagnose why results are not being returned

## 2. Fix num_results parameter handling

- [ ] Fix parameter handling in individual engines
  - [ ] Fix Brave engine's num_results handling

## 3. Add comprehensive tests

- [ ] Create test for num_results parameter handling
- [ ] Create test for proper source attribution in results
- [ ] Create test for verifying no unintended fallbacks
- [ ] Add test to verify engine availability detection

## 4. Documentation and logging improvements

- [ ] Enhance debug logging throughout the codebase
- [ ] Improve error messages for common failure cases
- [ ] Update documentation with common issues and solutions
- [ ] Document engine-specific requirements and limitations

## 5. Cleanup & Final Verification

- [ ] Run tests to ensure all engines are working properly
- [ ] Verify that each engine respects the num_results parameter
- [ ] Ensure no unintended fallbacks are occurring
- [ ] Update documentation to reflect changes
