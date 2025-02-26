--- 
this_file: TODO.md
--- 

# twat-search 

Tip: Periodically run `./cleanup.py status` to see results of lints and tests.

Edit the detailed plan in this file @TODO.md. Based on the plan, write an itemized list of tasks in @PROGRESS.md and then, as you work, check off your @PROGRESS.md.  

## 1. Progress Update (2025-02-27)

### 1.1. 1.1 Completed Tasks

We have made significant progress in fixing several critical issues:

1. Enhanced the `base.SearchEngine` class:
   - Fixed API key handling with proper validation
   - Improved error handling in HTTP requests with retries and better error messages
   - Implemented type annotations to fix incompatible type errors
   - Added proper documentation

2. Updated engine implementations:
   - Fixed You.com engines (`you` and `you_news`) with proper API key handling
   - Fixed Perplexity (`pplx`) implementation with explicit string conversion in error messages
   - Fixed Ruff code style issues across multiple files

3. Fixed linter issues:
   - Replaced assert statements with conditional checks
   - Fixed string literals in exceptions
   - Added proper type annotations

### 1.2. Urgent TODOs

Based on testing all engines with the command:
```
for engine in $(twat-search web info --plain); do echo; echo; echo; echo ">>> $engine"; twat-search web q -e $engine "Adam Twardoch" -n 1; done;
```

We've identified the following critical issues that need urgent attention:

#### 1.2.1. Result Limiting Not Working
Even with `-n 1` parameter, multiple results are returned for working engines. This needs to be fixed to ensure the `num_results` parameter is respected.

#### 1.2.2. Engine Initialization Failures
Several engines fail to initialize with error about missing `get_num_results` method:
- `brave` - Object has no attribute 'get_num_results'
- `brave_news` - Object has no attribute 'get_num_results'
- `critique` - Initialization failure
- `pplx` - Fails to initialize (likely API key related)
- `you` - Fails to initialize (likely API key related)
- `you_news` - Fails to initialize (likely API key related)

#### 1.2.3. Empty Results from SearchIt-based Engines
These engines return empty results consistently:
- `bing_searchit`
- `google_searchit`
- `qwant_searchit`
- `yandex_searchit`

#### 1.2.4. Unwanted Result Combination
Some engines are incorrectly combining results from multiple sources:
- `google_hasdata` - Returns its own results plus results from other engines
- `google_hasdata_full` - Returns its own results plus results from other engines

#### 1.2.5. Working Engines
The following engines are working, but have the issue with not respecting `num_results`:
- `bing_scraper`
- `duckduckgo`
- `google_scraper`
- `google_serpapi`
- `tavily`

### 1.3. `brave`

twat-search web q "Adam Twardoch" -n 1 --verbose --json -e brave

[02/26/25 20:51:35] DEBUG    Using num_results=5                                                                                                            cli.py:295
                    DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['brave']                                                                                   cli.py:171
                    DEBUG    Search requested with num_results=5                                                                                            api.py:148
                    DEBUG    Initializing engine 'brave' with num_results=5                                                                                  api.py:71
                    WARNING  Failed to initialize engine 'brave': EngineError                                                                                api.py:92
                    ERROR    Error initializing engine 'brave': Engine 'brave': Failed to initialize engine 'brave': 'BraveSearchEngine' object has no       api.py:95
                             attribute 'get_num_results'                                                                                                              
                    WARNING  Failed to initialize engine 'brave': Engine 'brave': Failed to initialize engine 'brave': 'BraveSearchEngine' object has no    api.py:184
                             attribute 'get_num_results'                                                                                                              
                    WARNING  Failed to initialize engines: brave                                                                                            api.py:191
                    ERROR    No search engines could be initialized from requested engines: brave                                                           api.py:199
                    ERROR    Search failed: No search engines could be initialized from requested engines: brave                                            api.py:246
                    ERROR    Search failed: No search engines could be initialized from requested engines: brave                                            cli.py:177
                            ❌ Search Errors                            
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized from requested engines: brave │
└──────────────────────────────────────────────────────────────────────┘
{}


### 1.4. `brave_news`

```
twat-search web q "Adam Twardoch" -n 1 --verbose --json -e brave_news
```

[02/26/25 20:52:52] DEBUG    Using num_results=5                                                                                                            cli.py:295
                    DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['brave_news']                                                                              cli.py:171
                    DEBUG    Search requested with num_results=5                                                                                            api.py:148
                    DEBUG    Initializing engine 'brave_news' with num_results=5                                                                             api.py:71
                    WARNING  Failed to initialize engine 'brave_news': EngineError                                                                           api.py:92
                    ERROR    Error initializing engine 'brave_news': Engine 'brave_news': Failed to initialize engine 'brave_news': 'BraveNewsSearchEngine'  api.py:95
                             object has no attribute 'get_num_results'                                                                                                
                    WARNING  Failed to initialize engine 'brave_news': Engine 'brave_news': Failed to initialize engine 'brave_news':                       api.py:184
                             'BraveNewsSearchEngine' object has no attribute 'get_num_results'                                                                        
                    WARNING  Failed to initialize engines: brave_news                                                                                       api.py:191
                    ERROR    No search engines could be initialized from requested engines: brave_news                                                      api.py:199
                    ERROR    Search failed: No search engines could be initialized from requested engines: brave_news                                       api.py:246
                    ERROR    Search failed: No search engines could be initialized from requested engines: brave_news                                       cli.py:177
                              ❌ Search Errors                               
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized from requested engines: brave_news │
└───────────────────────────────────────────────────────────────────────────┘
{}

### 1.5. 1.8 Further TODOs

Several issues still need immediate attention:

1. Fix failing tests - The test suite has 5 failing tests out of 49:
   - Tests in `test_api.py` related to search functionality
   - Tests in `test_config.py` about configuration expectations
   - A test in `test_bing_scraper.py` for the convenience function

2. Address inconsistent `num_results` parameter handling in all engines

3. Fix `searchit`-based engines that are returning empty results

## 2. Project Status

The basic implementation of the `twat-search` web package is complete. This multi-provider search tool now supports multiple search engines and has a functional CLI interface.

## 3. Problem case

This is the test command that I'm targeting: 

```bash
for engine in $(twat-search web info --plain); do echo; echo; echo; echo ">>> $engine"; twat-search web q -e $engine "Adam Twardoch" -n 1 --json --verbose; done;
```

## 4. Proposed solution

Okay, let's synthesize all the provided information into a single, comprehensive development guide for the `twat-search` project.  This guide will combine the problem statement, the detailed action plan (including code samples), the testing strategy, and the documentation considerations into a cohesive document. It's structured to be a practical guide for someone working on improving this project.

## 5. Twat Search Development Guide

This guide details the current state, problems, and a plan for refactoring and improving the `twat-search` web package.

### 5.1. Project Overview

`twat-search` is an asynchronous Python package designed to query multiple search engines simultaneously, aggregate their results, and present them through a unified API and command-line interface (CLI). It aims for:

*   **Multi-Engine Support:**  Integrate with various search providers (Brave, Google, Tavily, etc.).
*   **Asynchronous Operation:** Utilize `asyncio` for concurrent requests and improved performance.
*   **Configurability:** Allow users to configure engines, API keys, and search parameters via environment variables or configuration files.
*   **Extensibility:**  Make it easy to add new search engine integrations.
*   **Robustness:**  Handle errors gracefully, including API limits and network issues.
*   **Consistency:**  Provide a consistent JSON output format for all engines.

### 5.2. Current Status (as of 2025-02-27)

The basic implementation is complete, with several engines integrated and a functional CLI. Major improvements have been made to the base `SearchEngine` class and error handling. However, there are still issues with test failures and some engines returning empty results that need to be addressed.

### 5.3. Identified Problems

The following problems have been identified through testing and code review:

1.  **Test Failures:** Several tests are failing, particularly in `test_api.py`, `test_config.py`, and `test_bing_scraper.py`. These need to be fixed to ensure the code is working as expected.

2.  **Inconsistent `num_results` Handling:**  The `num_results` parameter, intended to control the number of results returned, is not consistently respected by all engines.

3.  **Empty Results from Some Engines:** The `searchit`-based engines (and potentially others) consistently return empty result sets, indicating a problem with their integration or underlying libraries.

4.  **Inconsistent JSON Output:** Different engines return results with varying key names and structures, making it difficult to process results uniformly. Example: Typos in keys like  `"snippetHighlitedWords"`.

5.  **Code Duplication and Inconsistency in `base.SearchEngine`:**  The base class contains duplicated logic for handling HTTP requests, retries, and parameter validation.  This should be centralized.

6. **Anywebsearch:** Remove all `anywebsearch` engines.

7. **Searchit:** Review the implementation of the `searchit` engines, or remove them.

### 5.4. Action Plan and Implementation Guide

This section provides a detailed, step-by-step plan to address the identified problems.

#### 5.4.1. Fixing Critical Engine Failures

**Goal:** Ensure all engines initialize correctly, handling API key requirements gracefully.

**4.1.1.  Enforce API Key Requirements in `base.SearchEngine`**

*   **File:** `src/twat_search/web/engines/base.py`
*   **Change:**  Modify the `SearchEngine` base class to *require* subclasses to define `env_api_key_names` as an abstract property. Remove the class-level default.

    ```python
    import abc
    import asyncio
    import random  # Import the random module
    import httpx
    from pydantic import BaseModel, HttpUrl, field_validator, ValidationError
    from typing import Any, Optional
    import logging
    from twat_search.web.exceptions import SearchError, EngineError
    from twat_search.web.config import EngineConfig
    from twat_search.web.models import SearchResult
    from twat_search.web.engine_constants import (
        USER_AGENTS,
        ENGINE_FRIENDLY_NAMES,
        standardize_engine_name,
    )

    logger = logging.getLogger(__name__)


    class SearchEngine(abc.ABC):
        engine_code: str  # REQUIRED: Engine code for config and CLI

        # Should not be a class variable, should be an instance
        # and a required property.
        @property
        @abc.abstractmethod
        def env_api_key_names(self) -> list[str]:
            """List of environment variable names that can hold the API key."""
            ...  # raise NotImplementedError("Subclasses must define env_api_key_names")

        @property
        @abc.abstractmethod
        def engine_code(self) -> str:
            """
            The engine code should be a short, unique identifier for the engine,
            using only lowercase letters and underscores.
            """
            ...


        def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
            self.config = config
            # Prioritize kwargs, then config.default_params, then fallbacks.
            self.num_results = self._get_num_results()  # Use the new method.
            self.country = kwargs.get("country") or self.config.default_params.get("country")
            self.language = kwargs.get("language") or self.config.default_params.get("language")
            self.safe_search = kwargs.get("safe_search", self.config.default_params.get("safe_search", True))  # type: ignore
            self.time_frame = kwargs.get("time_frame") or self.config.default_params.get("time_frame")
            self.timeout = kwargs.get("timeout", self.config.default_params.get("timeout", 10))
            self.retries = kwargs.get("retries", self.config.default_params.get("retries", 2))
            self.retry_delay = kwargs.get("retry_delay", self.config.default_params.get("retry_delay", 1.0))
            self.use_random_user_agent = kwargs.get("use_random_user_agent", self.config.default_params.get("use_random_user_agent", True))
            # Store original kwargs for use in subclasses
            self.kwargs = kwargs


            # Check for API key if required
            if self.env_api_key_names:  # Use the property, not the class variable
                api_key = config.api_keys.get(self.engine_code)
                if not api_key:
                  msg = (
                        f"API key is required for {self.engine_code}. "
                        f"Please set it via one of these env vars: {', '.join(self.env_api_key_names)}" # Use property
                    )
                  logger.error(msg)
                  raise EngineError(self.engine_code, msg)  # Use consistent EngineError
                self.api_key = api_key # Assign it to the object if it passes.
            else:
              self.api_key = None



        def _get_num_results(self, param_name: str = "num_results", min_value: int = 1) -> int:
            # Get value from kwargs
            value = self.kwargs.get(param_name)
            if value is not None:
                try:
                    return max(min_value, int(value))
                except (TypeError, ValueError):
                    logger.warning(
                        f"Invalid value for '{param_name}' ({value!r}) in {self.engine_code}, using default."
                    )
            #If not in kwargs get from config
            default = self.config.default_params.get(
                param_name
            ) or self.config.default_params.get("num_results") # num_results as fallback
            if default is not None:
                try:
                    return max(min_value, int(default))
                except (TypeError, ValueError):
                    logger.warning(
                        f"Invalid value for '{param_name}' ({value!r}) in {self.engine_code}, using default."
                    )
            return self.num_results



        async def make_http_request(
            self, method, url, headers=None, **kwargs
        ) -> httpx.Response: # return the full httpx.Response object
            headers = headers or {}
            if self.use_random_user_agent and "user-agent" not in {k.lower() for k in headers}:
                headers["User-Agent"] = random.choice(USER_AGENTS)

            delay = self.retry_delay #initiate delay
            for attempt in range(1, self.retries + 2):  # One extra attempt
                try:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:

                        response = await client.request(
                            method, url, headers=headers, **kwargs
                        )
                        response.raise_for_status()  # Raise for status here
                        return response # return response

                except httpx.HTTPError as e:
                    if attempt > self.retries:  # Use  self.retries
                        # Final retry failed.
                        logger.error(f"Request failed after {self.retries} attempts: {e}")
                        raise EngineError(self.engine_code, f"HTTP request failed after multiple retries: {e}") from e
                    # exponential backoff with jitter
                    jitter = random.uniform(0.5, 1.5)  # Add jitter
                    actual_retry_delay = delay * jitter
                    logger.warning(f"Request failed (attempt {attempt}), retrying in {actual_retry_delay:.2f} seconds: {e}")
                    await asyncio.sleep(actual_retry_delay)
                    delay *= 2  # Exponential backoff

        @abc.abstractmethod
        async def search(self, query: str) -> list[SearchResult]:
            """Perform the search and return a list of SearchResult objects."""
            ...

    _engine_registry = {} # Move to the bottom, after the class definition


    def register_engine(engine_class: type[SearchEngine]) -> type[SearchEngine]:
        try:
          # Check that the engine class has required attributes.
          if not hasattr(engine_class, "engine_code"):
              raise AttributeError("Engine must define an 'engine_code' attribute.")

          # Now using property, and check for its presence.
          if not hasattr(engine_class, "env_api_key_names") or not callable(getattr(engine_class, 'env_api_key_names', None)):
            raise AttributeError("Engine must define a 'env_api_key_names' property.")

          standardized_name = standardize_engine_name(engine_class.engine_code)
          # Check for collisions in engine codes
          if standardized_name in _engine_registry:
                raise ValueError(f"An engine with code '{standardized_name}' is already registered.")
          _engine_registry[standardized_name] = engine_class
          return engine_class
        except Exception as e:
            logger.warning(f"Failed to register engine {engine_class}: {e}")
            return None # Ensure it is not treated as registed.




    def get_engine(engine_name: str, config: EngineConfig, **kwargs: Any) -> SearchEngine:
        engine_class = _engine_registry.get(engine_name)
        if engine_class is None:
            raise EngineError(engine_name, f"Unknown search engine: '{engine_name}'.  Available engines: {', '.join(sorted(_engine_registry.keys()))}") # Improved error message.
        if not config.enabled:
            raise EngineError(engine_name, f"Search engine '{engine_name}' is disabled.")

        return engine_class(config, **kwargs)

    def get_registered_engines() -> dict[str, type[SearchEngine]]:
        return _engine_registry.copy()
    ```
    **Key changes:**

    *   `@abc.abstractmethod` is used for `env_api_key_names` and the new `_get_num_results`. This *forces* subclasses to implement them.
    *   `engine_code` validation added.
    *   A `ValueError` is raised if `engine_code` or the correct `env_api_key_names` are not provided. This prevents silent failures.
    *   `get_engine` now raises a more descriptive `EngineError` if the engine isn't found or is disabled.
    *   `make_http_request` centralizes request logic, including retries, user-agent randomization, and exception handling.  It now returns the full `httpx.Response` object, giving the calling engine more control.
    *  The num_results is validated so that if an invalid value is passed it will take the default value.
    * `_get_num_results` includes a fallback using the general `num_results`.

**4.1.2.  Enhance `config.py`**

*   **File:** `src/twat_search/web/config.py`
*   **Change:** Modify `EngineConfig` to perform validation and require an API key if the engine specifies `env_api_key_names`.

```python
# In src/twat_search/web/config.py
from pydantic import BaseModel, Field, field_validator, ValidationError
import os
import json
import logging
from pathlib import Path

load_dotenv()
logger = logging.getLogger(__name__)

# ... (rest of your config.py) ...

class EngineConfig(BaseModel):
    api_key: str | None = Field(default=None) # Optional in general
    enabled: bool = Field(default=False)
    default_params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("api_key", mode="before")
    def check_api_key(cls, v: str | None, values: ValidationInfo) -> str:
        # print("check_api_key", v, values)
        # if engine has api key names but no key, raise an error
        engine_code = values.data.get('engine_code') # get it from data to avoid errors
        if engine_code is None:
            return v

        try:
            engine_class = get_registered_engines()[standardize_engine_name(engine_code)]
        except KeyError:
            # if engine is not registed yet, we can't check for api_key
            return v

        if hasattr(engine_class, "env_api_key_names"):
            for key_name in engine_class.env_api_key_names:
                if key := os.environ.get(key_name):
                    return key

            # if none is set
            if v is None: # and also no api_key direct value set
                    raise ValueError(
                    f"Engine '{engine_code}' requires an API key. "
                    f"Please set one of these environment variables: {', '.join(engine_class.env_api_key_names)}"
                )

        return v

#keep Config class as is.
class Config(BaseModel):
    engines: dict[str, EngineConfig] = Field(default_factory=dict)
    # ... (rest of your Config class) ...

#Rest of file is ok.
```

**Key changes:**

*   **`@field_validator("api_key", mode="before")`:**  This validator runs *before* the `api_key` field is assigned.  This is crucial because we need to check if the key is required *before* Pydantic's default value logic kicks in.  We use `values.data.get('engine_code')` to safely access the engine code *during* validation, even if it hasn't been fully assigned yet.
*   **`get_registered_engines()`:** We call the `get_registered_engines()` function to access the registry.
*   **`KeyError` Handling:** The code now includes a `try...except KeyError` block. This is important.  During the *initial* loading of the configuration, the `EngineConfig` for an engine might be created *before* the engine class itself is registered.  In this case, looking up the engine class in `_engine_registry` would raise a `KeyError`.  The `try...except` handles this gracefully, skipping the API key check if the engine isn't registered yet.  This prevents a chicken-and-egg problem during startup.
* **Clear Error Message:**  The `ValueError` now provides a very specific message, telling the user *exactly* which environment variable(s) they need to set.
* No longer need for the map with environment variables.

**4.1.3. Update Engine Implementations**

*   **Files:**  `src/twat_search/web/engines/you.py`, `src/twat_search/web/engines/pplx.py`, `src/twat_search/web/engines/serpapi.py` (and any other engine requiring an API key)
*   **Change:**  Define the `env_api_key_names` correctly. Remove any existing API key handling from the `__init__` method (it's now handled by the base class and config).

    ```python
    # Example: src/twat_search/web/engines/you.py
    @register_engine
    class YouSearchEngine(YouBaseEngine):
        engine_code = "you"
        @property
        def env_api_key_names(self) -> list[str]:
          return ["YOU_API_KEY"]
        # ... rest of the engine implementation ...

    # Example: src/twat_search/web/engines/pplx.py
    @register_engine
    class PerplexitySearchEngine(SearchEngine):
      engine_code = "pplx"
      @property
      def env_api_key_names(self) -> list[str]:
        return ["PERPLEXITY_API_KEY"] # Or PERPLEXITYAI_API_KEY if that's correct
    # ...
    #Example: src/twat_search/web/engines/serpapi.py
    @register_engine
    class SerpApiSearchEngine(SearchEngine):
        engine_code = "serpapi"

        @property
        def env_api_key_names(self) -> list[str]:
            return ["SERPAPI_API_KEY"]
    ```
    Also in each class, make sure the `engine_code` is correct, and `_get_num_results` is defined.

**4.1.4. Improve `get_engine`**

Already addressed in 4.1.1.

**4.1.5 Test Engine Initialization**

*   **File:**  `tests/unit/web/engines/test_base.py` (and potentially engine-specific test files)
*   **Change:** Add tests to cover the API key requirement and engine availability:

    ```python
    # Inside test_base.py or a new test file.
    import pytest
    from twat_search.web.engines.base import get_engine, SearchEngine, register_engine, EngineError
    from twat_search.web.config import EngineConfig

    @register_engine
    class MockEngine(SearchEngine):
        engine_code = "mock_engine"
        @property
        def env_api_key_names(self):
          return ["MOCK_API_KEY"]

        async def search(self, query: str) -> list:
            return []

    def test_get_engine_missing_api_key(monkeypatch):
        monkeypatch.delenv("MOCK_API_KEY", raising=False)  # Ensure it's not set
        config = EngineConfig(enabled=True)  # No API key provided
        with pytest.raises(EngineError) as excinfo:
            get_engine("mock_engine", config)
        assert "MOCK_API_KEY" in str(excinfo.value) # Check for expected message

    def test_get_engine_api_key_present(monkeypatch):
        monkeypatch.setenv("MOCK_API_KEY", "test_key")
        config = EngineConfig(enabled=True)
        engine = get_engine("mock_engine", config) # Should not raise error
        assert engine.api_key == "test_key"  # Access api_key (if needed)

    def test_get_engine_disabled(monkeypatch):
      monkeypatch.delenv("MOCK_API_KEY", raising=False)  # Ensure it's not set
      config = EngineConfig(enabled=False)
      with pytest.raises(EngineError):
          get_engine("mock_engine", config)

    ```

**4.2. Data Integrity and Consistency**

**4.2.1. `num_results` Implementation**

*   **`base.SearchEngine`:** Already addressed above (abstract `_get_num_results` method).
*   **Engine-Specific Implementation (Example: `bing_scraper.py`):**

    ```python

    class BingScraperSearchEngine(SearchEngine):
        engine_code = "bing_scraper" # No API key
        @property
        def env_api_key_names(self):
          return []

        def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
          super().__init__(config, **kwargs)
          self.max_results = self._get_num_results()

        #... rest of your BingScraperSearchEngine code ...

    ```
    Make sure `self.max_results` is used to limit the results in the `search` method:
    ```python
    async def search(self, query: str) -> list[SearchResult]:
      # ... your code to fetch results ...

      results = []
      for result in raw_results: # raw_results would be results from scraper.
          search_result = self._convert_result(result)
          if search_result:  # Handle potential None values.
              results.append(search_result)
          if len(results) >= self.max_results:  # Limit results here.
              break

      return results
    ```

*   **Repeat:**  Apply the same `_get_num_results` implementation and result limiting logic to *all* other engine classes.  This is repetitive but crucial.

**4.2.2.  Source Attribution**
*   **`base.SearchEngine`:**  Already addressed with the abstract `engine_code` property.
*   **Engine-Specific Implementation:** In each engine, make *absolutely sure* you're using `self.engine_code` when creating the `SearchResult`:

    ```python
    # Example within an engine's search method:
    def _convert_result(self, raw: dict[str, Any]) -> SearchResult | None:
      try:
        return SearchResult(
            title=raw.get("title", ""),
            url=HttpUrl(raw.get("link", "")), # Using link
            snippet=raw.get("snippet", ""),
            source=self.engine_code,  # ALWAYS use self.engine_code
            raw=raw  # Include the raw data
        )
      except ValidationError as e:
        # warning message
        return None

    ```

**4.3. Engine Reliability (Empty Results)**

*   **`searchit` Engines:**
    1.  **Verify Installation:**  Run `uv pip install searchit` in your activated virtual environment.
    2.  **Minimal Example:** Create a *separate* Python script (`test_searchit.py`):

        ```python
        import asyncio
        from searchit.search import GoogleScraper, ScrapeRequest, SearchitResult

        async def test_searchit():
            scraper = GoogleScraper()
            request = ScrapeRequest(query="test query")
            results = await scraper.scrape(request)
            print(results)

        if __name__ == "__main__":
            asyncio.run(test_searchit())

        ```

        Run this script independently: `python test_searchit.py`.  If this fails, the problem is with the `searchit` library itself, or your installation of it (or potentially network/proxy issues).  If it *works*, the problem is in your integration within `twat-search`.

    3.  **Debugging (if the minimal example works):** Add detailed logging to `src/twat_search/web/engines/searchit.py`:

        ```python
        # Inside the GoogleSearchitEngine, YandexSearchitEngine, etc.
        async def search(self, query: str) -> list[SearchResult]:
            if not query:
                raise EngineError(self.engine_code, "Search query cannot be empty")
            logger.info(f"Searching Google (searchit) with query: '{query}'")

            request = ScrapeRequest(
                query=query,
                domain=self.domain,
                language=self.language,
                geo=self.geo,
                max_results=self.max_results, # Use self.max_results
                sleep_interval=self.sleep_interval,

            )
            logger.debug(f"searchit request: {request!r}")  # Log the request object

            scraper = GoogleScraper( # initiate object here, to pass max_results_per_page
                max_results_per_page=min(100, self.max_results),
            )

            try:
              raw_results = await self._run_scraper(scraper, request) # run scraper
              logger.debug(f"Raw results from searchit: {raw_results!r}")  # Log raw results
              if not raw_results:
                  logger.info("No results returned from Google (searchit)")
                  return []
              logger.debug(
                  f"Received {len(raw_results)} raw results from Google (searchit)",
              )
            except Exception as exc:
                error_msg = f"Error running searchit scraper: {exc}"
                logger.error(error_msg)
                raise EngineError(self.engine_code, error_msg) from exc
        # ...rest of code ...
        ```
*   **Brave News, Perplexity:**  Start by getting the *base* Brave and Perplexity engines working.  Then debug the news-specific versions, looking for differences in API endpoints, parameters, or response formats.  Use extensive logging.

**4.4. Codebase Cleanup (`anywebsearch` Removal)**

This is straightforward:

1.  **Delete File:** Delete `src/twat_search/web/engines/anywebsearch.py`.
2.  **Remove Imports:**  Remove *all* imports related to `anywebsearch` from:
    *   `src/twat_search/web/engines/__init__.py`
    *   `src/twat_search/web/engine_constants.py`
    *   Any test files that might have been using it.
3.  **Run Linters:** Use `ruff check --fix` and `ruff format` to automatically clean up unused imports and formatting.
4.  **Run Tests:**  Run `pytest` to ensure that no other parts of the codebase were relying on `anywebsearch`.

**4.5. Improve the CLI (q command)**
* **Remove Engine Specific Params:** The `q` command in the CLI needs to be updated to only take common params. This should be done by making the parameters not prefixed.
    ```python
     @app.command(
        help="Search across multiple engines simultaneously.",
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    )
    def q(
        self,
        ctx: fire.core.Context,
        query: str = typer.Argument(..., help="The search query."),
        engines: str | None = typer.Option(
            None,
            "--engines",
            "-e",
            help="Comma-separated list of search engines to use (e.g., brave,tavily).",
        ),
        num_results: int = typer.Option(
            None,
            "--num-results",
            "-n",
            help="Number of results to return (overrides engine defaults).",
        ),
        country: str = typer.Option(
            None,
            "--country",
            "-c",
            help="Country code for the search (e.g., US, GB).",
        ),
        language: str = typer.Option(
            None,
            "--language",
            "-l",
            help="Language code for the search (e.g., en, es).",
        ),
        safe_search: bool = typer.Option(
            None,
            "--safe-search",
            "-s",
            help="Enable or disable safe search (True/False).",
        ),
        json_output: bool = typer.Option(
            False, "--json", help="Output results in JSON format."
        ),
        verbose: bool = typer.Option(
            False, "--verbose", "-v", help="Enable verbose logging."
        ),
        plain: bool = typer.Option(
            False, "--plain", "-p", help="Output in plain text, url only."
        ),
    ) -> None:
    ```
* **Remove engine specific parameters:**  from the various engine specific commands, like brave, tavily, pplx, etc.
* **Test:** Run `cleanup.py status`

**4.6 Enforce JSON Output Format**

To standardize the JSON output format across all search engines, you should create a helper function that takes the necessary data and returns a dictionary with a consistent structure. This function will be used by each engine to format its results before returning them.  Since you are already using `pydantic`, use your existing `SearchResult` model.

Here's how you would do this:

1.  **Use `SearchResult` model:**

    In `src/twat_search/web/models.py`, you have the following `SearchResult` model:

    ```python
    class SearchResult(BaseModel):
        url: HttpUrl
        title: str
        snippet: str
        source: str
        raw: dict[str, Any] | None = None  # To store any engine-specific data

        @field_validator("title", "snippet", "source")
        def validate_non_empty(cls, v: str) -> str:
            if not v or not v.strip():
                msg = f"value must not be None or empty string, got='{v}'"
                raise ValueError(msg)
            return v.strip()
    ```

2. **Remove utility function**
Remove the `_process_results` and `_display_json_results`. Remove `CustomJSONEncoder`.

3.  **Modify Engine `search` Methods:**

    Each engine's `search` method should now create and return a list of `SearchResult` objects directly, instead of plain dictionaries.

    Example (using a simplified `DuckDuckGoSearchEngine` for illustration):

    ```python
    # src/twat_search/web/engines/duckduckgo.py
    class DuckDuckGoSearchEngine(SearchEngine):
      # ...

      async def search(self, query: str) -> list[SearchResult]:
          # ... (fetch raw results from DuckDuckGo API) ...
          results: list[SearchResult] = []
          for raw_result in raw_results:
            try:
              search_result = SearchResult(
                  url=raw_result["url"],
                  title=raw_result["title"],
                  snippet=raw_result.get("snippet", ""),  # Provide a default
                  source=self.engine_code, # Set source
                  raw=raw_result,  # Store the raw result
              )
              results.append(search_result)
              if len(results) >= self.max_results:
                break # respect the num_results/max_results.
            except ValidationError as e:
                logger.warning(f"Validation error for result: {e}")
                # Consider logging the raw_result here, for debugging.
                continue  # Skip invalid results
            except Exception as e: # catch unexpected errors
                logger.warning(f"Unexpected error converting result: {e}")
                continue

          return results
    ```
    Key points here:
    * Return type is now `list[SearchResult]`.
    * A SearchResult is instantiated for *every* valid result.
    * `source=self.engine_code` is used to correctly set the source.
    * A `try...except ValidationError` block handles potential Pydantic validation errors, logging them and skipping the invalid result.
    * We have added another exception block to catch other exceptions.
    * Added a limit on the number of results using `self.max_results`.
4. **Update API function**

```python
#src/twat_search/web/api.py

async def search(
    query: str,
    engines: list[str] | None = None,
    config: Config | None = None,
    strict_mode: bool = True, # added to ensure that error is raised if engine does not exist.
    **kwargs: Any,
) -> list[SearchResult]: # Change return type
```

Change the return type to `list[SearchResult]`.

```python
    results = await asyncio.gather(*tasks, return_exceptions=True)

    flattened_results: list[SearchResult] = []
    for engine_name, result in zip(engine_names, results, strict=False):
        if isinstance(result, Exception):
            logger.error(
                f"Engine '{engine_name}' failed: {type(result).__name__} - {result}",
            )
        elif isinstance(result, list):
            # This part now expects a list of SearchResult objects. No conversion needed!
            logger.info(
                f"✅ Engine '{engine_name}' returned {len(result)} results",
            )

            for search_result in result:
                search_result.source = engine_name # override and use the engine name
                flattened_results.append(search_result)
        else:
            logger.warning(
                f"⚠️ Engine '{engine_name}' returned no results or unexpected type: {type(result)}",
            )

    if not flattened_results:
        logger.error(f"Search failed: {e}")
        raise SearchError("No results found from any search engine.")

    return flattened_results

```
The important part here is that `flattened_result` and the return is a list of `SearchResult`.

5. **Update CLI function**
Update the `q` command in `cli.py`

```python
@app.command(
    help="Search across multiple engines simultaneously.",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def q(
    self,
    ctx: fire.core.Context,
    query: str = typer.Argument(..., help="The search query."),
    engines: str | None = typer.Option(
        None,
        "--engines",
        "-e",
        help="Comma-separated list of search engines to use (e.g., brave,tavily).",
    ),
    num_results: int = typer.Option(
        None,
        "--num-results",
        "-n",
        help="Number of results to return (overrides engine defaults).",
    ),
    country: str = typer.Option(
        None,
        "--country",
        "-c",
        help="Country code for the search (e.g., US, GB).",
    ),
    language: str = typer.Option(
        None,
        "--language",
        "-l",
        help="Language code for the search (e.g., en, es).",
    ),
    safe_search: bool = typer.Option(
        None,
        "--safe-search",
        "-s",
        help="Enable or disable safe search (True/False).",
    ),
    json_output: bool = typer.Option(
        False, "--json", help="Output results in JSON format."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging."
    ),
    plain: bool = typer.Option(
        False, "--plain", "-p", help="Output in plain text, url only."
    ),
) -> None:

    self._configure_logging(verbose)
    #... parse engines, as you did before ...
    if num_results is not None:
        self.logger.debug(f"Using num_results={num_results}")
        common_params["num_results"] = num_results

    # Run search and handle potential errors.
    try:
        results = asyncio.run(
            self._run_search(
                query,
                engine_list,
                **common_params
            )
        )
        if json_output:
            # Use model_dump to serialize Pydantic models to dict
            print(json.dumps([r.model_dump() for r in results], indent=2)) # Now serializing correctly.
        else:
            _display_results(results, verbose, plain) #Simplified _display_results

    except SearchError as e:
        self.logger.error(f"Search failed: {e}")
        _display_errors([str(e)])
```

*   **Key changes:**
    *   The `q` command no longer takes engine-specific parameters.  It only takes common parameters, which are passed to the `_run_search` function.
    * The JSON output uses pydantic `model_dump` to convert `SearchResult` to dict.
    *   The non-JSON output uses a simplified `_display_results` function (see below).

```python
#Simplified display function
def _display_results(results: list[SearchResult], verbose: bool, plain: bool) -> None:
    if not results:
        console.print("[bold red]No results found![/bold red]")
        return

    if plain:
        urls = set()
        for result in results:
            # Avoid duplicate URLs
            if str(result.url) not in urls:
                urls.add(str(result.url))
        for url in sorted(urls):
            console.print(url)
        return

    table = Table()  # Remove show_lines=True to eliminate row separator lines
    table.add_column("Engine", style="magenta")
    if verbose:
      table.add_column("Title", style="green")
      table.add_column("URL", style="blue", overflow="fold", max_width=70)
    else:
      table.add_column("URL", style="blue", overflow="fold")

    for result in results:
        if verbose:
          table.add_row(result.source, result.title, str(result.url))
        else:
          table.add_row(result.source, str(result.url))
    console.print(table)
```

* **Remove helper functions:**
`_process_results`, `_display_json_results` and `CustomJSONEncoder` class are not needed anymore since `twat_search.web.models.SearchResult` model and pydantic `model_dump` are used.

**6. Testing:**

*   Create test cases for each of the above changes, especially within `tests/unit/web/engines/test_base.py` and in individual engine test files.
*   Test the CLI using `fire.Fire`'s testing utilities, as demonstrated in your existing `tests/test_twat_search.py`.

By systematically applying these steps, the code will become more robust, maintainable, and consistent. The detailed plan and code samples will guide you through the refactoring process. Remember to execute `cleanup.py status` regularly and run `pytest` to check for any errors or regressions introduced during the modifications.  Address *all* Ruff and Mypy issues.










