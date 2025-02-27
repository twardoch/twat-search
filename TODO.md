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

Based on the NEXTENGINES.md file, we need to implement search engines based on the [Falla project](https://github.com/Sanix-Darker/falla), which is a search engine scraper supporting multiple search engines.

### 1.1. Understanding Falla Architecture

Falla is a Python-based search engine scraper that supports multiple search engines including Google, Bing, DuckDuckGo, and others. Each search engine has its own implementation file in the `app/core/` directory, inheriting from a base `Falla` class.

The key components of Falla are:

1. A base `Falla` class that handles common scraping functionality
2. Individual engine classes (Google, Bing, etc.) that define engine-specific parameters
3. A common interface for searching and result parsing

### 1.2. Implementation Plan for *-falla Engines

#### 1.2.1. Setup and Dependencies

1. Create a new module `src/twat_search/web/engines/falla.py` to implement Falla-based engines
2. Add necessary dependencies to `pyproject.toml`:
   - `selenium` for browser automation
   - `lxml` for HTML parsing
   - `requests` for HTTP requests
   - Optional: Consider if we need Docker/Splash for some engines

3. Define engine constants in `src/twat_search/web/engine_constants.py`:
   
```python
   # Falla-based engines
   GOOGLE_FALLA = "google-falla"
   BING_FALLA = "bing-falla"
   DUCKDUCKGO_FALLA = "duckduckgo-falla"
   AOL_FALLA = "aol-falla"
   ASK_FALLA = "ask-falla"
   DOGPILE_FALLA = "dogpile-falla"
   GIBIRU_FALLA = "gibiru-falla"
   MOJEEK_FALLA = "mojeek-falla"
   QWANT_FALLA = "qwant-falla"
   YAHOO_FALLA = "yahoo-falla"
   YANDEX_FALLA = "yandex-falla"
   
   # Update ENGINE_FRIENDLY_NAMES
   ENGINE_FRIENDLY_NAMES.update({
       GOOGLE_FALLA: "Google (Falla)",
       BING_FALLA: "Bing (Falla)",
       DUCKDUCKGO_FALLA: "DuckDuckGo (Falla)",
       AOL_FALLA: "AOL (Falla)",
       ASK_FALLA: "Ask.com (Falla)",
       DOGPILE_FALLA: "DogPile (Falla)",
       GIBIRU_FALLA: "Gibiru (Falla)",
       MOJEEK_FALLA: "Mojeek (Falla)",
       QWANT_FALLA: "Qwant (Falla)",
       YAHOO_FALLA: "Yahoo (Falla)",
       YANDEX_FALLA: "Yandex (Falla)",
   })
   
   # Update ALL_POSSIBLE_ENGINES
   ALL_POSSIBLE_ENGINES.extend([
       GOOGLE_FALLA,
       BING_FALLA,
       DUCKDUCKGO_FALLA,
       AOL_FALLA,
       ASK_FALLA,
       DOGPILE_FALLA,
       GIBIRU_FALLA,
       MOJEEK_FALLA,
       QWANT_FALLA,
       YAHOO_FALLA,
       YANDEX_FALLA,
   ])
   ```

4. Update `src/twat_search/web/engines/__init__.py` to import and register the new engines:
   
```python
   # Add to imports
   from twat_search.web.engine_constants import (
       # ... existing imports ...
       GOOGLE_FALLA,
       BING_FALLA,
       DUCKDUCKGO_FALLA,
       AOL_FALLA,
       ASK_FALLA,
       DOGPILE_FALLA,
       GIBIRU_FALLA,
       MOJEEK_FALLA,
       QWANT_FALLA,
       YAHOO_FALLA,
       YANDEX_FALLA,
   )
   
   # Add to __all__
   __all__ = [
       # ... existing entries ...
       "GOOGLE_FALLA",
       "BING_FALLA",
       "DUCKDUCKGO_FALLA",
       "AOL_FALLA",
       "ASK_FALLA",
       "DOGPILE_FALLA",
       "GIBIRU_FALLA",
       "MOJEEK_FALLA",
       "QWANT_FALLA",
       "YAHOO_FALLA",
       "YANDEX_FALLA",
   ]
   ```

#### 1.2.2. Base Implementation

1. Create a base `FallaSearchEngine` class in `src/twat_search/web/engines/falla.py`

2. Implement specific engine classes for each Falla engine

#### 1.2.3. Falla Integration Approach

Instead of making Falla a dependency, we'll incorporate the Falla code directly into the project:

1. Create a `lib_falla` directory in `src/twat_search/web/engines/` to contain the Falla code
2. Adapt the Falla code to work within our project structure:
   - Update import paths
   - Fix any compatibility issues
   - Ensure proper attribution and licensing
3. Update the `FallaSearchEngine` class to use the embedded Falla code
4. Create a fallback mechanism for when certain dependencies are not available

Benefits of this approach:
* No dependency on an unmaintained external package
* Better control over the code and its behavior
* Ability to fix bugs and make improvements as needed
* Simplified installation for users

#### 1.2.4. Implementation Details

1. The `FallaSearchEngine` class will:
   - Initialize the appropriate Falla engine based on the engine code
   - Convert Falla results to our standard `SearchResult` format
   - Handle errors gracefully
   - Provide consistent behavior across all engines

2. Each specific engine class (e.g., `GoogleFallaEngine`) will:
   - Define engine-specific parameters
   - Initialize the appropriate Falla engine
   - Register itself with the engine registry

3. The embedded Falla code will be modified to:
   - Work with our project structure
   - Use our logging system
   - Handle errors consistently with the rest of the project
   - Support our configuration system
