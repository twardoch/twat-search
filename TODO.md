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

1. Create a base `FallaSearchEngine` class in `src/twat_search/web/engines/falla.py`:

```python
#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["selenium", "lxml", "requests"]
# ///
# this_file: src/twat_search/web/engines/falla.py
"""
Falla-based search engine implementations.

This module implements search engines based on the Falla project
(https://github.com/Sanix-Darker/falla), which is a search engine scraper
supporting multiple search engines.

The FallaSearchEngine class serves as a base class for all Falla-based
engines, providing common functionality for initialization, searching,
and result parsing.
"""

from __future__ import annotations

import importlib.util
import logging
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Union, cast

import requests
from lxml import etree
from pydantic import BaseModel, HttpUrl, ValidationError
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from twat_search.web.config import EngineConfig
from twat_search.web.engine_constants import (
    AOL_FALLA,
    ASK_FALLA,
    BING_FALLA,
    DEFAULT_NUM_RESULTS,
    DOGPILE_FALLA,
    DUCKDUCKGO_FALLA,
    ENGINE_FRIENDLY_NAMES,
    GIBIRU_FALLA,
    GOOGLE_FALLA,
    MOJEEK_FALLA,
    QWANT_FALLA,
    YAHOO_FALLA,
    YANDEX_FALLA,
)
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult

# Initialize logger
logger = logging.getLogger(__name__)

class FallaResult(BaseModel):
    """
    Pydantic model for a single Falla search result.
    
    This model is used to validate the response from Falla scrapers.
    It ensures that each result has the required fields and proper types
    before being converted to the standard SearchResult format.
    
    Attributes:
        title: The title of the search result
        url: The URL of the search result, validated as a proper HTTP URL
        snippet: Description/snippet of the search result
    """
    
    title: str
    url: HttpUrl
    snippet: str = ""

class FallaSearchEngine(SearchEngine, ABC):
    """
    Base class for all Falla-based search engines.
    
    This class provides common functionality for initializing Falla components,
    performing searches, and parsing results. It is designed to be subclassed
    by specific engine implementations.
    
    Attributes:
        engine_code: The name of the search engine (e.g., "google-falla")
        env_api_key_names: Empty list since no API key is needed for Falla engines
    """
    
    # No API key needed for Falla engines
    env_api_key_names: ClassVar[list[str]] = []
    
    def __init__(
        self,
        config: EngineConfig,
        num_results: int = DEFAULT_NUM_RESULTS,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | str | None = True,
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize Falla Search engine.
        
        Args:
            config: Engine configuration
            num_results: Number of results to return
            country: Country code for results
            language: Language code for results
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            **kwargs: Additional Falla-specific parameters
        """
        super().__init__(config, **kwargs)
        self.num_results = self._get_num_results()
        self.country = country or self.config.default_params.get("country")
        self.language = language or self.config.default_params.get("language", "en")
        self.safe_search = safe_search if safe_search is not None else self.config.default_params.get("safe_search", True)
        self.time_frame = time_frame or self.config.default_params.get("time_frame")
        
        # Falla-specific parameters
        self.mode = kwargs.get("mode") or self.config.default_params.get("mode", "requests")
        self.max_retry = kwargs.get("max_retry") or self.config.default_params.get("max_retry", 3)
        
        # Initialize Falla engine
        self.falla_engine = self._initialize_falla_engine()
    
    @abstractmethod
    def _initialize_falla_engine(self) -> Any:
        """
        Initialize the specific Falla engine.
        
        This method should be implemented by subclasses to create and configure
        the appropriate Falla engine instance.
        
        Returns:
            An instance of the specific Falla engine
        """
        pass
    
    def _convert_result(self, result: Dict[str, Any]) -> SearchResult | None:
        """
        Convert a raw result from Falla into a SearchResult.
        
        This method validates the raw result using the FallaResult model
        and converts it to the standard SearchResult format if valid.
        
        Args:
            result: Raw result dictionary from Falla
        
        Returns:
            SearchResult object or None if validation fails
        """
        if not result:
            logger.warning("Empty result received from Falla")
            return None
        
        try:
            # Ensure title and snippet are at least empty strings
            title = result.get("title", "") or ""
            snippet = result.get("cite", "") or ""
            url = result.get("href", "")
            
            # Validate result fields
            validated = FallaResult(
                title=title,
                url=HttpUrl(url),
                snippet=snippet,
            )
            
            # Create and return the SearchResult
            return SearchResult(
                title=validated.title,
                url=validated.url,
                snippet=validated.snippet,
                source=self.engine_code,
                raw=result,
            )
        except ValidationError as exc:
            logger.warning(f"Validation error for result: {exc}")
            return None
        except Exception as exc:
            logger.warning(f"Unexpected error converting result: {exc}")
            return None
    
    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Falla engine.
        
        This method uses the initialized Falla engine to perform the search
        and converts the results to the standard SearchResult format.
        
        Args:
            query: The search query string
        
        Returns:
            A list of SearchResult objects
        
        Raises:
            EngineError: If the search fails due to invalid input, network issues,
                         parsing errors, or other exceptions
        """
        if not query:
            raise EngineError(self.engine_code, "Search query cannot be empty")
        
        logger.info(f"Searching {self.engine_code} with query: '{query}'")
        
        try:
            # Perform search using the Falla engine
            raw_results = self.falla_engine.search(query)
            
            if not raw_results:
                logger.info(f"No results returned from {self.engine_code}")
                return []
            
            logger.debug(f"Received {len(raw_results)} raw results from {self.engine_code}")
            
            # Convert and filter results
            results: list[SearchResult] = []
            for result in raw_results:
                search_result = self._convert_result(result)
                if search_result:
                    results.append(search_result)
                    if len(results) >= self.num_results:
                        break
            
            logger.info(f"Returning {len(results)} validated results from {self.engine_code}")
            return results
            
        except Exception as exc:
            error_msg = f"Error during {self.engine_code} search: {exc}"
            logger.error(error_msg)
            raise EngineError(self.engine_code, error_msg) from exc
```

2. Implement specific engine classes for each Falla engine:

```python
@register_engine
class GoogleFallaEngine(FallaSearchEngine):
    """
    Implementation of Google search using Falla.
    
    This engine uses the Falla Google scraper to search Google without requiring an API key.
    """
    
    engine_code = GOOGLE_FALLA
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[GOOGLE_FALLA]
    
    def _initialize_falla_engine(self) -> Any:
        """
        Initialize the Google Falla engine.
        
        Returns:
            An instance of the Falla Google engine
        """
        try:
            from app.core.Google import Google
            return Google()
        except ImportError:
            raise EngineError(
                self.engine_code,
                "Failed to import Falla Google engine. Make sure Falla is installed correctly."
            )

@register_engine
class BingFallaEngine(FallaSearchEngine):
    """
    Implementation of Bing search using Falla.
    
    This engine uses the Falla Bing scraper to search Bing without requiring an API key.
    """
    
    engine_code = BING_FALLA
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[BING_FALLA]
    
    def _initialize_falla_engine(self) -> Any:
        """
        Initialize the Bing Falla engine.
        
        Returns:
            An instance of the Falla Bing engine
        """
        try:
            from app.core.Bing import Bing
            return Bing()
        except ImportError:
            raise EngineError(
                self.engine_code,
                "Failed to import Falla Bing engine. Make sure Falla is installed correctly."
            )

@register_engine
class DuckDuckGoFallaEngine(FallaSearchEngine):
    """
    Implementation of DuckDuckGo search using Falla.
    
    This engine uses the Falla DuckDuckGo scraper to search DuckDuckGo without requiring an API key.
    """
    
    engine_code = DUCKDUCKGO_FALLA
    friendly_engine_name = ENGINE_FRIENDLY_NAMES[DUCKDUCKGO_FALLA]
    
    def _initialize_falla_engine(self) -> Any:
        """
        Initialize the DuckDuckGo Falla engine.
        
        Returns:
            An instance of the Falla DuckDuckGo engine
        """
        try:
            from app.core.DuckDuckGo import DuckDuckGo
            return DuckDuckGo()
        except ImportError:
            raise EngineError(
                self.engine_code,
                "Failed to import Falla DuckDuckGo engine. Make sure Falla is installed correctly."
            )

# Implement the remaining engine classes following the same pattern
```

#### 1.2.3. Falla integration

Make Falla a direct dependency of twat-search:

```python
# In pyproject.toml
dependencies = [
    # ... existing dependencies ...
    "falla @ git+https://github.com/Sanix-Darker/falla.git",
]
```

**Pros:**

* Simple for users (installed automatically with twat-search)
* Ensures consistent version

