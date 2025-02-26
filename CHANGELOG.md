# Changelog

All notable changes to this project will be documented in this file.

## Changes by date

### 2025-02-26

#### Changed

- Refactored the CLI to import engine functions more safely, handling missing dependencies.
- Updated the CLI to use a dictionary to map the registered engines to their convenience functions, making it easier to call functions.
- Standardized engine names to use underscores internally.
- Modified the `_parse_engines` method in the CLI to handle special strings ("free", "best", "all") for selecting groups of engines.
- Updated the `q` method in the CLI to use unified parameters and to control verbose output.
- Updated the `info` method in the CLI to use unified parameters, to list engines, and to provide detailed information about specific engines.
- Updated `_display_results` in the CLI to handle multiple results per engine and optional plain-text output (no table, just URLs).
- Updated the `_display_json_results` function in the CLI to create JSON output.
- Updated the `config` class to parse environment variables for engines using a regular expression, addressing issues with engine configuration.
- Updated various engine implementations (Brave, Tavily, You, Perplexity, SerpApi) to use unified parameters and improve URL handling.

#### Added

- Implemented `bing_scraper` convenience function.
- Added comprehensive tests to verify the correct behavior of the `bing_scraper` convenience function.
- Implemented the `WebScoutEngine` class, providing basic search functionality.
- Added new search engine integrations:
    - `google_scraper.py`: Implemented a `GoogleScraperEngine` and a `google_scraper` convenience function.
    - `searchit.py`: Implemented several search engines using the `searchit` library: `GoogleSearchitEngine`, `YandexSearchitEngine`, `QwantSearchitEngine`, `BingSearchitEngine`.
    - `anywebsearch.py`: Implemented multiple search engines using the `anywebsearch` library: `GoogleAnyWebSearchEngine`, `BingAnyWebSearchEngine`, `BraveAnyWebSearchEngine`, `QwantAnyWebSearchEngine`, `YandexAnyWebSearchEngine`.
    - `hasdata.py`: Implemented `HasDataGoogleEngine` and `HasDataGoogleLightEngine`.
- Added tests for `bing_scraper`.

### 2025-02-25

#### Added

- Created initial project structure and implemented several search engine integrations (Brave, Google, Tavily, Perplexity, You.com).
- Developed core functionality, including a command-line interface (CLI) and asynchronous search capabilities.
- Implemented configuration management and exception handling.
- Implemented rate limiting utility.
- Added Pydantic models for data validation.
- Added unit tests for the models, configuration, utility functions, exceptions, and the base search engine class.

#### Changed

- Updated the `config.py` file to correctly import BaseSettings from the pydantic-settings package.
- Updated the `pyproject.toml` file to add pydantic-settings as a dependency.
- Updated the example usage in `example.py`.
- Completed the implementation of the web search functionality as specified in TODO.md.
- Planned comprehensive tests for the package.

### 2025-02-25 - Initial Development

- Created initial project structure and files.
- Created a preliminary TODO.md, PROGRESS.md, and research.txt.

---
