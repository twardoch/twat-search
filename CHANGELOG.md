---
this_file: CHANGELOG.md
---

# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.2] - 2025-03-04

### Fixed
- Fixed linting errors in the codebase:
  - Replaced `os.path.abspath()` with `Path.resolve()` in `google.py`
  - Replaced `os.path.exists()` with `Path.exists()` in `google.py`
  - Replaced insecure usage of the temporary file directory `/tmp` with `tempfile.gettempdir()` in `test_google_falla_debug.py`
  - Replaced `os.path.join()` with `Path` and the `/` operator in `test_google_falla_debug.py`
  - Removed unused imports (`os` and `NavigableString`) from `google.py`

### Improved
- Improved code quality and maintainability through better path handling using `pathlib.Path`
- Enhanced security by using the standard library's `tempfile` module for temporary file operations

## [0.1.1] - 2025-02-26

### Added
- Refactored CLI to use `fire` for better command-line interface
- Updated methods to use unified parameters
- Added `brave` search engine integration
- Added `tavily` search engine integration
- Added `perplexity` search engine integration
- Added `you` search engine integration
- Added `searchit` search engine integration
- Added `falla` search engine integration
- Added `bing_falla` search engine integration
- Added `google_falla` search engine integration
- Added `duckduckgo_falla` search engine integration
- Added `aol_falla` search engine integration
- Added `ask_falla` search engine integration
- Added `dogpile_falla` search engine integration
- Added `gibiru_falla` search engine integration
- Added `mojeek_falla` search engine integration
- Added `qwant_falla` search engine integration
- Added `yahoo_falla` search engine integration
- Added `yandex_falla` search engine integration
- Added `bing_searchit` search engine integration
- Added `google_searchit` search engine integration
- Added `qwant_searchit` search engine integration
- Added `yandex_searchit` search engine integration
- Added `utils.py` for common utility functions
- Added `config.py` for configuration management
- Added `api.py` for API functions
- Added `cli.py` for CLI functions
- Added `base.py` for base classes
- Added `engine_constants.py` for engine constants
- Added `models.py` for data models
- Added `exceptions.py` for custom exceptions
- Added `__init__.py` files for package structure
- Added `pyproject.toml` for package configuration
- Added `README.md` for documentation
- Added `LICENSE` for licensing information
- Added `CHANGELOG.md` for change tracking
- Added `TODO.md` for task tracking
- Added `PROGRESS.md` for progress tracking
- Added `cleanup.py` for code cleanup

## [0.1.0] - 2025-02-25

### Added
- Initial project structure
- Core functionality
- Basic search engine integrations
- Command-line interface
- Python API
- Documentation
- Tests

### Changed

- Updated the `config.py` file to correctly import BaseSettings from the pydantic-settings package.
- Updated the `pyproject.toml` file to add pydantic-settings as a dependency.
- Updated the example usage in `example.py`.
- Completed the implementation of the web search functionality as specified in TODO.md.
- Planned comprehensive tests for the package.

### 2025-02-25 - Initial Development

- Created initial project structure and files.
- Created a preliminary TODO.md, PROGRESS.md, and research.txt.

---
