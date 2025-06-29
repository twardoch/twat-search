# Twat Search

**Part of the [twat](https://pypi.org/project/twat/) collection of tools.**

`twat-search` is a powerful and flexible multi-engine web search aggregator. It provides a unified command-line and programmatic interface to query a wide array of search engines simultaneously, returning results in a consistent and easy-to-process format.

## Who is it for?

`twat-search` is designed for:

*   **Developers** who need to integrate web search capabilities into their applications.
*   **Researchers** and **analysts** who require comprehensive search results from multiple sources for data gathering and analysis.
*   **Data scientists** looking to collect web data for training models or generating insights.
*   **Anyone** who wants to save time and effort by querying multiple search engines at once and getting aggregated results.

## Why is it useful?

*   **Comprehensive Results**: Get a broader perspective by searching across many engines, including specialized ones, reducing the chance of missing information.
*   **Time-Saving**: Query multiple search engines with a single command or API call.
*   **Consistent Output**: All results are normalized into a standard JSON format, making them easy to parse and use.
*   **Programmatic Access**: Easily integrate search functionality into your Python scripts and applications.
*   **Rich CLI**: Enjoy a user-friendly command-line interface with features like engine selection, JSON output, and easy configuration.
*   **Configurability**: Fine-tune search parameters, select engines, and manage API keys via environment variables or direct code configuration.
*   **Asynchronous Operations**: Leverages `asyncio` for efficient, non-blocking searches when used programmatically.

## Key Features

*   **Multi-Engine Support**: Access a diverse range of search engines (e.g., Brave, DuckDuckGo, Google via SerpAPI, Bing Scraper, and many more).
*   **Unified Interface**: Consistent CLI commands and Python API for all supported engines.
*   **Asynchronous API**: High-performance `asyncio`-based API for concurrent searching.
*   **Standardized Results**: Search results provided in a uniform Pydantic model, easily exportable to JSON.
*   **Flexible Configuration**: Configure API keys, engine preferences, and default parameters through environment variables (`.env` supported) or Python code.
*   **Rich Command-Line Tool**: Powered by `python-fire` and `rich` for a pleasant and informative CLI experience.
*   **Extensible**: Designed to easily incorporate new search engines.
*   **Robust Error Handling**: Gracefully handles issues with individual engines without disrupting the overall search process.
## Installation

You can install `twat-search` using pip:

```bash
pip install twat-search
```

This will install the core package with a basic set of features.

### Installing with Optional Engine Dependencies

Many search engines require additional libraries (e.g., for specific APIs or web scraping capabilities). You can install these optional dependencies as "extras".

To install support for specific engines, list them in brackets:

```bash
# Install with support for DuckDuckGo and Brave
pip install twat-search[duckduckgo,brave]

# Install with support for Falla-based engines (e.g., Google Falla)
pip install twat-search[falla]
```

To install support for all available optional engines:

```bash
pip install twat-search[all]
```

You can find the list of available extras and the engines they enable in the `pyproject.toml` file or the "Supported Search Engines" section of this document.

## Usage

`twat-search` can be used both as a command-line tool and as a Python library.

### Command-Line Interface (CLI)

The CLI provides a quick way to perform searches directly from your terminal. The main command is `twat-search web`.

**Basic Search:**
Query all configured and enabled engines:
```bash
twat-search web q "latest advancements in AI"
```

**Specify Engines:**
Search using only selected engines (e.g., `brave` and `duckduckgo`):
```bash
twat-search web q "Python programming best practices" -e brave,duckduckgo
```
*Note: Engine names are typically lowercase. Use `twat-search web info --plain` to see available engine identifiers.*

**Get JSON Output:**
Retrieve results in a machine-readable JSON format:
```bash
twat-search web q "future of renewable energy" --json
```

**List Available Engines:**
See a list of all search engines detected by the tool:
```bash
twat-search web info --plain
```
This will show their identifiers, whether they are enabled, and if API keys are found (if required).

**Control Number of Results:**
Specify the number of results per engine (if the engine supports it):
```bash
twat-search web q "best Python IDEs" --num_results 5
```
*Note: `num_results` is a global parameter. Some engines might also support engine-specific parameters like `count` via the CLI. For example, `twat-search web q -e brave "query" --count 3`.*


### Programmatic Usage (Python API)

Integrate `twat-search` into your Python applications using its asynchronous API.

**Basic Asynchronous Search:**

```python
import asyncio
from twat_search.web.api import search
from twat_search.web.models import SearchResult

async def main():
    query = "What is quantum computing?"
    print(f"Searching for: {query}...")

    # Search across all enabled and configured engines
    # You can also specify engines: await search(query, engines=["brave", "duckduckgo"])
    results: list[SearchResult] = await search(query)

    if not results:
        print("No results found.")
        return

    print(f"Found {len(results)} results:\n")
    for result in results:
        print(f"Engine: {result.source_engine}")
        print(f"Title: {result.title}")
        print(f"URL: {result.url}")
        print(f"Snippet: {result.snippet}")
        if result.extra_info:
            print(f"Extra: {result.extra_info}")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(main())
```

This example demonstrates a basic search. The `search` function can be further customized with specific engines, configurations, and parameters.

## Configuration Overview

`twat-search` offers flexible configuration options primarily through **environment variables** and **programmatic settings**.

*   **Environment Variables**:
    *   This is the most common way to configure `twat-search`, especially for API keys and engine enablement.
    *   You can set variables in your shell, or for convenience, define them in a `.env` file in your project's root directory. `twat-search` will automatically load it.
    *   Key settings include:
        *   API keys for services like Brave, SerpAPI, Tavily (e.g., `BRAVE_API_KEY="your_key_here"`).
        *   Enabling or disabling specific engines (e.g., `DUCKDUCKGO_ENABLED=true`, `GOOGLE_FALLA_ENABLED=false`).
        *   Setting default search parameters for engines (e.g., `BRAVE_DEFAULT_PARAMS='{"count": 7, "country": "US"}'`).
        *   Global settings like `NUM_RESULTS=10` to attempt to fetch a specific number of results from all engines.

*   **Programmatic Configuration**:
    *   When using `twat-search` as a Python library, you can pass a `Config` object to the `search` function.
    *   This allows for dynamic, in-code configuration of engines, API keys, and parameters, overriding any environment settings.

A more detailed explanation of all configuration options, including specific environment variable names and programmatic `Config` object usage, can be found in the **Technical Deep Dive** section later in this document.

## Technical Deep Dive

This section provides a more detailed look into the inner workings of `twat-search`, aimed at developers who wish to understand or contribute to the project.

### Core Architecture

`twat-search` is built with a modular architecture, primarily centered around its Python components. Key modules and their roles include:

*   **`twat_search.web.api`**:
    *   This module exposes the main programmatic interface, primarily the `async def search(...)` function.
    *   It orchestrates the search process: loading configurations, selecting and initializing engines, dispatching search queries concurrently, aggregating results, and handling errors.

*   **`twat_search.web.cli`**:
    *   Implements the command-line interface using the `python-fire` library for command parsing and `rich` for formatted output.
    *   It translates CLI arguments into calls to the `twat_search.web.api` or configuration display functions.
    *   The entry point for the CLI is `twat-search web ...`. (Note: `twat-search` itself is a top-level namespace, and `web` is the subcommand for web search functionalities).

*   **`twat_search.web.config`**:
    *   Manages all configuration aspects of the library.
    *   Defines Pydantic models (`Config`, `EngineConfig`) for structuring configuration data.
    *   Loads settings from environment variables (with support for `.env` files via `pydantic-settings`) and allows for programmatic overrides.
    *   Handles validation and default values for engine parameters and API keys.

*   **`twat_search.web.engines`**:
    *   This package is the heart of the multi-engine capability.
    *   **`engines/__init__.py`**: Dynamically discovers and registers available engine implementations. It also checks for necessary dependencies and API keys for each engine.
    *   **`engines/base.py`**: Defines the `SearchEngine` abstract base class. All individual engine implementations must inherit from this class and implement its required methods (e.g., `async_search`).
    *   **Individual Engine Modules** (e.g., `brave.py`, `duckduckgo.py`, `falla.py`): Each file implements the logic for a specific search engine, handling its API communication or web scraping process, parameter mapping, and result parsing.
        *   Engines requiring browser automation (like `google_falla`) might reside in sub-packages like `lib_falla` and utilize tools such as Playwright.

*   **`twat_search.web.models`**:
    *   Defines Pydantic models for data structures, most importantly `SearchResult`.
    *   `SearchResult` provides a standardized format for search results (title, URL, snippet, source engine, etc.), ensuring consistency across all engines. These models are also used for JSON serialization.

*   **`twat_search.web.exceptions`**:
    *   Contains custom exception classes (e.g., `SearchError`, `EngineError`, `ConfigError`) to provide more specific error information and allow for granular error handling by users of the library.

*   **Asynchronous Operations**:
    *   The core search functionality (`api.search` and individual engine searches) is built using `asyncio` and `httpx.AsyncClient` (for most HTTP-based engines). This allows for efficient concurrent execution of multiple search engine queries, significantly speeding up the overall search process.

*   **Engine Discovery and Loading**:
    *   Engines are typically classes inheriting from `SearchEngine`. They are discovered at runtime by inspecting the `twat_search.web.engines` package.
    *   The `Config` object determines which discovered engines are actually enabled and used for a given search operation, based on environment variables or programmatic settings.

### Supported Search Engines

`twat-search` provides a consistent interface to a variety of search engines. The availability of each engine depends on whether required API keys are provided and necessary optional dependencies are installed.

| Engine Name          | Identifier (`-e` flag) | API Key Req. | API Key Env Var        | Package Extra (`pip install twat-search[extra]`) | Description                                      |
|----------------------|------------------------|----------------|------------------------|----------------------------------------------------|--------------------------------------------------|
| Brave Search         | `brave`                | Yes            | `BRAVE_API_KEY`        | `brave` (or `all`)                                 | General web search via Brave Search API.         |
| Brave News           | `brave_news`           | Yes            | `BRAVE_API_KEY`        | `brave` (or `all`)                                 | News-specific search via Brave API.              |
| You.com              | `you`                  | Yes            | `YOU_API_KEY`          | `-` (core dependency)                              | Web search via You.com API.                      |
| You.com News         | `you_news`             | Yes            | `YOU_API_KEY`          | `-` (core dependency)                              | News search via You.com API.                     |
| Tavily               | `tavily`               | Yes            | `TAVILY_API_KEY`       | `tavily` (or `all`)                                | AI-powered research-focused search API.          |
| Perplexity AI        | `pplx`                 | Yes            | `PERPLEXITY_API_KEY`   | `pplx` (or `all`)                                  | AI-powered search with detailed answers.         |
| SerpAPI (Google)     | `serpapi`              | Yes            | `SERPAPI_API_KEY`      | `serpapi` (or `all`)                               | Google search results via SerpAPI.               |
| HasData Google       | `hasdata-google`       | Yes            | `HASDATA_API_KEY`      | `hasdata` (or `all`)                               | Google search results via HasData API.           |
| HasData Google Light | `hasdata-google-light` | Yes            | `HASDATA_API_KEY`      | `hasdata` (or `all`)                               | Light version of HasData Google API.             |
| Critique             | `critique`             | Yes            | `CRITIQUE_API_KEY`     | `-` (core dependency)                              | Visual and textual search capabilities.          |
| DuckDuckGo           | `duckduckgo`           | No             | -                      | `duckduckgo` (or `all`)                            | Privacy-focused search results.                  |
| Bing Scraper         | `bing_scraper`         | No             | -                      | `bing_scraper` (or `all`)                          | Web scraping of Bing search results.             |
| Google Falla         | `google_falla`         | No             | -                      | `falla` (or `all`)                                 | Google search via Playwright-based scraping.     |
| Google Scraper       | `google_scraper`       | No             | -                      | `google_scraper` (or `all`)                        | Google search via direct scraping (less reliable).|

*Notes:*
*   "-" in "Package Extra" means the dependencies are part of the core `twat-search` installation or not explicitly defined as an extra (this might need verification against `pyproject.toml`).
*   Engine identifiers are used with the `-e` flag in the CLI (e.g., `twat-search web q "query" -e brave,duckduckgo`) and in programmatic configuration.
*   Some engines might be disabled by default and require explicit enabling via environment variables (e.g., `ENGINE_NAME_ENABLED=true`) or programmatic configuration, in addition to API keys and optional dependencies.

### Configuration Management (Detailed)

Configuration is primarily handled by the `twat_search.web.config.Config` class, which uses `pydantic-settings` to load values from environment variables and `.env` files.

#### Environment Variables

Environment variables are the primary method for configuring `twat-search` outside of direct code. They are case-sensitive. If an `.env` file exists in the current working directory when `twat-search` is initialized, it will be loaded automatically.

**Key Environment Variables:**

*   **Global Settings:**
    *   `LOG_LEVEL`: Set the logging level (e.g., `DEBUG`, `INFO`, `WARNING`). Defaults to `INFO`.
    *   `NUM_RESULTS`: A global suggestion for the number of results to fetch from each engine. Engines will try to honor this if they support such a parameter. Example: `NUM_RESULTS=5`.

*   **Engine-Specific Settings:**
    Most engine settings follow a pattern: `[ENGINE_IDENTIFIER_UPPERCASE]_API_KEY`, `[ENGINE_IDENTIFIER_UPPERCASE]_ENABLED`, `[ENGINE_IDENTIFIER_UPPERCASE]_DEFAULT_PARAMS`.

    *   **API Keys**:
        *   `BRAVE_API_KEY="your_brave_key"`
        *   `YOU_API_KEY="your_you_key"`
        *   `TAVILY_API_KEY="your_tavily_key"`
        *   `PERPLEXITY_API_KEY="your_perplexity_key"`
        *   `SERPAPI_API_KEY="your_serpapi_key"` (for Google via SerpAPI)
        *   `HASDATA_API_KEY="your_hasdata_key"` (for HasData Google engines)
        *   `CRITIQUE_API_KEY="your_critique_key"`
        *   *(Add other API key variables as defined in `config.py` or engine modules)*

    *   **Enabling/Disabling Engines**:
        By default, engines that require API keys are typically disabled if the key is not found. Engines that don't require keys are often enabled by default. You can explicitly enable or disable any engine:
        *   `BRAVE_ENABLED=true` (or `false`)
        *   `DUCKDUCKGO_ENABLED=true`
        *   `GOOGLE_FALLA_ENABLED=false`
        *   *(Refer to `twat_search.web.config.EngineConfig` and specific engine implementations for default enabled states and identifiers)*

    *   **Default Parameters**:
        Set default search parameters for specific engines using a JSON string. These parameters are passed to the engine during searches if not overridden by parameters in the `search` call.
        *   `BRAVE_DEFAULT_PARAMS='{"count": 10, "safesearch": "strict", "country": "US"}'`
        *   `TAVILY_DEFAULT_PARAMS='{"max_results": 7, "search_depth": "advanced"}'`
        *   `DUCKDUCKGO_DEFAULT_PARAMS='{"max_results": 5, "region": "us-en"}'`
        *   `SERPAPI_DEFAULT_PARAMS='{"num": 10, "gl": "us", "hl": "en"}'`
        *   *(Consult each engine's documentation or its module in `twat_search.web.engines` for available parameters.)*

**Example `.env` file:**
```env
# .env
BRAVE_API_KEY="YOUR_ACTUAL_BRAVE_KEY"
BRAVE_ENABLED=true
BRAVE_DEFAULT_PARAMS='{"count": 5, "safesearch": "moderate"}'

DUCKDUCKGO_ENABLED=true
DUCKDUCKGO_DEFAULT_PARAMS='{"max_results": 3}'

# Disable an engine that might be enabled by default
# SOME_OTHER_ENGINE_ENABLED=false

NUM_RESULTS=7
LOG_LEVEL=INFO
```

#### Programmatic Configuration

For more dynamic control within Python applications, you can instantiate and pass a `Config` object to the `search` function. This will override any settings from environment variables for that specific search call.

```python
from twat_search.web.api import search
from twat_search.web.config import Config, EngineConfig
import asyncio

async def perform_custom_search():
    custom_config = Config(
        # Global settings can also be set here if applicable, e.g. num_results
        # num_results=3, # This would apply to all engines in this config
        engines={
            "brave": EngineConfig(
                enabled=True,
                api_key="your_brave_key_for_this_search", # Overrides env
                default_params={"count": 3, "country": "DE"}
            ),
            "duckduckgo": EngineConfig(
                enabled=True,
                default_params={"max_results": 2, "region": "de-de"}
            ),
            "serpapi": EngineConfig( # Example: enabling an engine that might be off by env
                enabled=True,
                api_key="your_serpapi_key_here",
                default_params={"num": 2, "gl": "de", "hl": "de"}
            ),
            # Ensure other engines are explicitly disabled if not desired
            "google_falla": EngineConfig(enabled=False),
            "bing_scraper": EngineConfig(enabled=False),
            # ... and so on for other engines to ensure precise control
        }
    )

    results = await search("example query", config=custom_config)
    for result in results:
        print(f"[{result.source_engine}] {result.title}: {result.url}")

if __name__ == "__main__":
    asyncio.run(perform_custom_search())
```

When using programmatic configuration:
*   Any engine *not* explicitly defined in the `engines` dictionary of your `Config` object will typically fall back to its environment variable settings or defaults.
*   To ensure only specified engines run, you might need to explicitly disable others in your `Config` object if they could be enabled by environment variables. Alternatively, use the `engines=["engine1", "engine2"]` parameter in the `search()` call, which takes precedence for engine selection.

### Output Format

All search results, whether from the CLI (using the `--json` flag) or the Python API, are standardized into a consistent structure defined by the `twat_search.web.models.SearchResult` Pydantic model.

**Key Fields in `SearchResult`:**

*   `query` (str): The original search query.
*   `source_engine` (str): The identifier of the engine that produced this result (e.g., "brave", "duckduckgo").
*   `title` (str): The title of the search result.
*   `url` (str): The URL of the search result.
*   `snippet` (Optional[str]): A short description or snippet from the result page. May be `None`.
*   `score` (Optional[float]): A relevance score, if provided by the engine. May be `None`.
*   `position` (Optional[int]): The rank/position of the result in the engine's original list. May be `None`.
*   `raw` (Optional[dict]): The raw, unprocessed result data from the engine, for debugging or advanced use. May be `None`.
*   `extra_info` (Optional[dict]): Any additional structured information provided by the engine. May be `None`.
*   `timestamp` (datetime): The timestamp when the search result was processed.

**Sample JSON Output Snippet (from CLI with `--json`):**

When using the CLI with the `--json` flag, the output is a JSON array of `SearchResult` objects.

```json
[
  {
    "query": "Python programming",
    "source_engine": "duckduckgo",
    "title": "Python For Beginners - Learn Python Programming",
    "url": "https://www.pythonforbeginners.com/",
    "snippet": "Python For Beginners.com is a website where you can learn Python programming. We have tutorials for total beginners and advanced programmers.",
    "score": null,
    "position": 1,
    "raw": {
      "hostname": "www.pythonforbeginners.com",
      "icon": "https://www.pythonforbeginners.com/favicon.ico",
      "html": "<b>Python</b> For Beginners.com is a website where you can learn <b>Python</b> programming. We have tutorials for total beginners and advanced programmers."
    },
    "extra_info": null,
    "timestamp": "2023-10-27T10:30:00.123456"
  },
  {
    "query": "Python programming",
    "source_engine": "brave",
    "title": "Python (programming language) - Wikipedia",
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "snippet": "Python is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant indentation.",
    "score": 0.95,
    "position": 1,
    "raw": {
      "meta_url": {
        "scheme": "https",
        "netloc": "en.wikipedia.org",
        "path": "/wiki/Python_(programming_language)",
        "favicon": "https://en.wikipedia.org/static/favicon/wikipedia.ico"
      }
    },
    "extra_info": {
      "type": "web"
    },
    "timestamp": "2023-10-27T10:30:01.567890"
  }
  // ... more results
]
```

Programmatically, you receive a `list[SearchResult]` where each item is an instance of the Pydantic model, allowing direct attribute access (e.g., `result.title`, `result.url`).

### Error Handling Framework

`twat-search` includes a robust error handling system to manage issues that may arise during configuration, engine initialization, or the search process. Custom exceptions provide clarity and allow for targeted error management.

**Custom Exception Hierarchy:**

Located in `twat_search.web.exceptions`:

*   `SearchError(Exception)`: Base exception for all errors originating from the `twat-search` library.
    *   `ConfigError(SearchError)`: Raised for configuration-related problems (e.g., invalid parameter values, missing required settings if not handled by Pydantic's validation directly).
    *   `EngineError(SearchError)`: Base for errors specific to a search engine's operation.
        *   `APIKeyMissingError(EngineError)`: Raised if a required API key for an engine is not found.
        *   `EngineDisabledError(EngineError)`: Raised when an attempt is made to use an explicitly disabled engine.
        *   `EngineRequestError(EngineError)`: For issues during an engine's request to its external API or source (e.g., network errors, HTTP status code errors).
        *   `EngineResponseError(EngineError)`: For problems parsing or interpreting an engine's response.
    *   `NoEnginesAvailableError(SearchError)`: Raised if no search engines are specified or if all specified/configured engines are unavailable or disabled.

**Key Error Handling Features:**

*   **Graceful Engine Failures**: If one engine encounters an error (e.g., API down, invalid credentials), it logs the error and is excluded from the current search. Other configured engines will still attempt to perform the search. The overall `search` call will not fail unless `NoEnginesAvailableError` occurs.
*   **Clear Logging**: Errors are logged with context, including the engine name and a description of the issue, aiding in debugging.
*   **Specific Exceptions**: Using distinct exception types allows programmatic users to catch and handle different error conditions appropriately.
*   **Configuration Validation**: Pydantic models in `twat_search.web.config` automatically validate many configuration parameters on load, raising errors for type mismatches or invalid values according to defined constraints.

**Example (Programmatic Error Handling):**

```python
import asyncio
from twat_search.web.api import search
from twat_search.web.exceptions import (
    SearchError,
    EngineError,
    APIKeyMissingError,
    NoEnginesAvailableError
)

async def main():
    try:
        # Intentionally use an engine that might be misconfigured or requires an API key
        results = await search("test query", engines=["misconfigured_engine", "brave"])
        for result in results:
            print(f"[{result.source_engine}] {result.title}")
    except APIKeyMissingError as e:
        print(f"API Key Error: {e}. Please check your configuration for engine '{e.engine_name}'.")
    except NoEnginesAvailableError as e:
        print(f"Search Failed: {e}. No engines could be used for the search.")
    except EngineError as e:
        # Catch other engine-specific errors
        print(f"An error occurred with engine '{e.engine_name}': {e}")
    except SearchError as e:
        # Catch any other search-related errors
        print(f"A general search error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

This structured approach to error handling makes `twat-search` more resilient and easier to integrate into larger applications where robust error management is critical.

## Development and Contribution

We welcome contributions to `twat-search`! Whether it's adding a new search engine, fixing a bug, or improving documentation, your help is appreciated.

### Project Structure

The project follows a standard Python src-layout:

*   `src/twat_search/`: Main source code for the library.
    *   `web/`: Core web search functionality.
        *   `engines/`: Implementations for each search engine.
*   `tests/`: Contains unit and integration tests.
*   `pyproject.toml`: Defines project metadata, dependencies, build system (Hatch), and tool configurations (Ruff, Mypy, Pytest).
*   `README.md`: This file.
*   `CHANGELOG.md`: Tracks changes across versions.
*   `TODO.md`: Lists planned features and improvements.
*   `.github/workflows/`: GitHub Actions for CI (testing, linting, releases).

### Setting up Development Environment

We use [Hatch](https://hatch.pypa.io/) for project management and [uv](https://github.com/astral-sh/uv) as a fast package installer/resolver, often via Hatch.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/twardoch/twat-search.git
    cd twat-search
    ```

2.  **Create and activate the development environment:**
    Hatch will manage this for you. To create the default environment (which includes dev, test, and all engine dependencies):
    ```bash
    hatch env create
    ```
    This command sets up an environment (often a virtual environment) and installs all necessary dependencies as defined in `pyproject.toml`.

    To activate the environment's shell if you need to run commands directly:
    ```bash
    hatch shell
    ```
    Alternatively, you can run commands through Hatch: `hatch run <command>`.

### Running Tests

Tests are written using `pytest` and are located in the `tests/` directory.

*   **Run all tests:**
    ```bash
    hatch run test
    ```
    Or, if you have activated the shell:
    ```bash
    pytest
    ```

*   **Run tests with coverage:**
    ```bash
    hatch run test-cov
    ```
    This will generate a coverage report in the terminal and potentially an XML report for CI. Configuration for coverage is in `pyproject.toml` (`[tool.coverage]`).

### Code Quality & Linting

We use several tools to maintain code quality, all configured in `pyproject.toml`:

*   **Ruff**: For extremely fast linting and formatting. It replaces tools like Flake8, isort, and Black.
*   **Mypy**: For static type checking.
*   **Pre-commit Hooks**: Configured in `.pre-commit-config.yaml` to run checks automatically before commits. It's highly recommended to install and use these.

**Common Commands (run via Hatch):**

*   **Check for linting issues and format code:**
    ```bash
    hatch run lint  # Runs ruff check and ruff format
    ```
    Or more fine-grained:
    ```bash
    hatch run fix   # Runs ruff check --fix --unsafe-fixes and ruff format
    ```

*   **Run type checking:**
    ```bash
    hatch run type-check
    ```
    Or within the Hatch shell:
    ```bash
    mypy src/twat_search tests
    ```

**Pre-commit Hooks:**
Install pre-commit hooks to automate these checks:
```bash
pip install pre-commit  # If not already installed
pre-commit install
```
Now, `ruff` and other checks will run on staged files before each commit.

### Coding Conventions

*   **Style**: We follow PEP 8, with formatting enforced by Ruff (configured in `pyproject.toml`). Maximum line length is 120 characters.
*   **Imports**:
    *   Absolute imports are preferred (`from twat_search.web.utils import ...`).
    *   Imports are sorted by Ruff (according to isort rules).
    *   `flake8-tidy-imports` is used (via Ruff) to ban relative imports.
*   **Type Hinting**:
    *   Comprehensive type hints are mandatory for all functions and methods.
    *   Mypy is used for static type checking with a strict configuration (see `[tool.mypy]` in `pyproject.toml`).
*   **Logging**: Use the standard `logging` module for any informational or debug messages.
*   **Docstrings**: Use Google-style docstrings for modules, classes, functions, and methods.
*   **Asynchronous Code**: Use `async/await` syntax for all I/O-bound operations, particularly for network requests within search engines. Use `httpx.AsyncClient` for HTTP requests.

### Contributing Guidelines

1.  **Find an Issue or Feature**:
    *   Check the `TODO.md` file for a list of planned tasks.
    *   Look at existing issues on GitHub, especially those labeled `help wanted` or `good first issue`.
    *   If you have a new idea, consider opening an issue first to discuss it.

2.  **Fork and Branch**:
    *   Fork the repository on GitHub.
    *   Create a new branch for your feature or bugfix from the `main` branch (e.g., `git checkout -b feature/add-new-engine` or `fix/resolve-bug-123`).

3.  **Develop**:
    *   Write your code, adhering to the coding conventions.
    *   **Add tests!** New features must include corresponding tests. Bug fixes should ideally include a test that reproduces the bug and verifies the fix.
    *   Ensure your code is well-documented with docstrings and comments where necessary.

4.  **Test and Lint**:
    *   Run all tests: `hatch run test`.
    *   Run linters and type checkers: `hatch run lint`, `hatch run type-check`. Fix any reported issues.
    *   Using pre-commit hooks will help catch issues early.

5.  **Update Changelog**:
    *   Add a concise entry to `CHANGELOG.md` under the "Unreleased" section, describing your changes. Include your GitHub username.

6.  **Commit and Push**:
    *   Commit your changes with a clear and descriptive commit message.
    *   Push your branch to your fork on GitHub.

7.  **Submit a Pull Request (PR)**:
    *   Open a PR from your branch to the `main` branch of the `twardoch/twat-search` repository.
    *   Provide a clear description of the changes in the PR. Link to any relevant issues.
    *   Ensure that CI checks (GitHub Actions) pass on your PR.

### Build and Release Process (Maintainers)

This section is primarily for project maintainers.

*   **Versioning**: The project uses `hatch-vcs` for versioning, which derives the version from Git tags.
*   **Building**: Hatch is used to build the package (wheels and sdists).
    ```bash
    hatch build
    ```
*   **Releasing**:
    1.  Ensure `main` branch is up-to-date and all tests/checks pass.
    2.  Update `CHANGELOG.md`: Move entries from "Unreleased" to a new version section.
    3.  Commit changelog changes: `git commit -m "Docs: Update changelog for vX.Y.Z"`
    4.  Create a Git tag for the new version: `git tag vX.Y.Z`
    5.  Push the commit and tag: `git push && git push --tags`
    6.  The `release.yml` GitHub Actions workflow should automatically trigger, build the package, and publish it to PyPI.
    7.  Verify the new version on PyPI. Create a GitHub Release from the tag with release notes based on the changelog.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
