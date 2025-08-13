# TODO-cla.md
# Comprehensive Improvement Plan for twat-search Repository

This document outlines specific, actionable improvement proposals for the twat-search repository, organized by priority and impact. Each section includes detailed implementation guidance and rationale.

## 🚨 CRITICAL PRIORITY (Fix Broken Functionality)

### 1. Fix Falla-Based Engine Dependencies and Type Issues

**Problem**: Multiple Falla engines are broken due to Playwright dependency issues and type errors.

**Specific Actions**:
```bash
# Install missing Playwright dependencies
uv add --group dev playwright
python -m playwright install chromium

# Fix type errors in google.py:
# Line ~35: self.wait_for_selector could be None
# Line ~67: attrs parameter type incompatibility  
# Line ~89: elem parameter type issues in get_title, get_link, get_snippet
# Line ~156: PageElement missing 'find' attribute
```

**Implementation Plan**:
1. **Update type annotations** in `src/twat_search/web/engines/lib_falla/core/google.py`:
   ```python
   # Fix Optional types
   from typing import Optional
   # Fix Optional types
   wait_for_selector: Optional[str] = None
   
   # Fix BeautifulSoup element types
   from typing import Optional
   # Fix Optional types
   wait_for_selector: Optional[str] = None
   
   # Fix BeautifulSoup element types
   def get_title(self, elem: Optional[Tag]) -> str:
       if elem is None:
           return ""
       title_elem = elem.find("h3")
       return title_elem.get_text() if title_elem else ""
   ```

2. **Add proper error handling** for Playwright browser context:
   ```python
   async def ensure_browser_context(self):
       if not self.browser_context:
           await self.init_browser()
       return self.browser_context
   ```

3. **Update CSS selectors** for current Google page structure (likely changed since implementation).

**Impact**: This fixes the core search functionality that's currently broken.

### 2. Standardize Search Result Processing

**Problem**: Inconsistent result formatting across engines, some using custom JSON encoders.

**Specific Actions**:
```python
# Remove CustomJSONEncoder class from cli.py
# Update all engine search methods to return List[SearchResult]
# Standardize result processing in api.py

# Example fix for brave.py:
from typing import List
async def search(self, query: str) -> List[SearchResult]:
    # ... existing code ...
    results = []
    for item in response_data.get("web", {}).get("results", []):
        result = SearchResult(
            query=query,
            source_engine=self.name,
            title=item.get("title", ""),
            url=item.get("url", ""),
            snippet=item.get("description", ""),
            timestamp=datetime.utcnow(),
            raw=item
        )
        results.append(result)
    return results
```

**Impact**: Ensures consistent API responses and easier maintenance.

## 🔥 HIGH PRIORITY (Code Quality & Reliability)

### 3. Implement Comprehensive Error Handling Strategy

**Problem**: Inconsistent error handling across engines leads to unexpected failures.

**Specific Actions**:
1. **Create custom exception hierarchy**:
   ```python
   # In exceptions.py
   class SearchEngineTimeout(SearchError):
       """Raised when search engine times out"""
       pass
   
   class SearchEngineRateLimit(SearchError):
       """Raised when rate limited by search engine"""
       pass
   
   class SearchEngineBlocked(SearchError):
       """Raised when search engine blocks requests"""
       pass
   ```

2. **Add retry mechanism with exponential backoff**:
   ```python
   # In base.py
   from typing import List
   async def search_with_retry(self, query: str, max_retries: int = 3) -> List[SearchResult]:
       for attempt in range(max_retries):
           try:
               return await self.search(query)
           except SearchEngineRateLimit:
               wait_time = 2 ** attempt
               await asyncio.sleep(wait_time)
           except SearchEngineTimeout:
               if attempt == max_retries - 1:
                   raise
               continue
       return []
   ```

3. **Implement graceful degradation**:
   ```python
   # In api.py
   from typing import List
   async def search_with_fallback(engines: List[str], query: str) -> List[SearchResult]:
       results = []
       for engine_name in engines:
           try:
               engine_results = await search_single_engine(engine_name, query)
               results.extend(engine_results)
               if len(results) >= 10:  # Minimum acceptable results
                   break
           except Exception as e:
               logger.warning(f"Engine {engine_name} failed: {e}")
               continue
       return results
   ```

### 4. Enhance Test Coverage and Quality

**Problem**: Only 12 test files for 64 Python files (18.75% file coverage).

**Specific Actions**:
1. **Create engine-specific test suites**:
   ```python
   # tests/unit/web/engines/test_brave.py
   @pytest.mark.asyncio
   async def test_brave_search_success():
       engine = BraveSearchEngine(api_key="test_key")
       with aioresponses() as m:
           m.get('https://api.search.brave.com/res/v1/web/search', 
                 payload=mock_brave_response)
           results = await engine.search("test query")
           assert len(results) > 0
           assert all(isinstance(r, SearchResult) for r in results)
   ```

2. **Add integration tests**:
   ```python
   # tests/integration/test_search_pipeline.py
   @pytest.mark.integration
   async def test_multi_engine_search():
       config = Config(engines={"mock": EngineConfig(enabled=True)})
       results = await search("test query", config=config)
       assert len(results) > 0
   ```

3. **Create performance benchmarks**:
   ```python
   # tests/benchmarks/test_performance.py
   @pytest.mark.benchmark(group="search")
   def test_search_performance(benchmark):
       result = benchmark(run_sync_search, "python programming")
       assert len(result) > 0
   ```

**Target Metrics**:
- Achieve 80%+ line coverage
- Add 50+ additional test cases
- Create benchmark suite for performance regression detection

### 5. Modernize Configuration Management

**Problem**: Environment variable handling is complex and error-prone.

**Specific Actions**:
1. **Simplify configuration with Pydantic v2 features**:
   ```python
   # In config.py
   from pydantic import Field, computed_field
   from pydantic_settings import BaseSettings, SettingsConfigDict
   
   class EngineConfig(BaseModel):
       enabled: bool = Field(default=True)
   from typing import Optional
   
   class EngineConfig(BaseModel):
       enabled: bool = Field(default=True)
       api_key: Optional[str] = Field(default=None, validation_alias='API_KEY')
   from typing import Dict, Any
   
   class EngineConfig(BaseModel):
       enabled: bool = Field(default=True)
       default_params: Dict[str, Any] = Field(default_factory=dict)
       api_key: str | None = Field(default=None, validation_alias='API_KEY')
       
       @computed_field
       @property
       def is_available(self) -> bool:
           return self.enabled and (self.api_key is not None or not self.requires_api_key)
   ```

2. **Add configuration validation**:
   ```python
   class Config(BaseSettings):
       model_config = SettingsConfigDict(
           env_file='.env',
           env_file_encoding='utf-8',
           case_sensitive=False,
           validate_assignment=True
       )
       
       @model_validator(mode='after')
       def validate_engines(self):
           if not any(engine.is_available for engine in self.engines.values()):
               raise ValueError("No search engines are available")
           return self
   ```

## 🔧 MEDIUM PRIORITY (Developer Experience)

### 6. Improve Development Workflow

**Specific Actions**:
1. **Add pre-commit hooks configuration**:
   ```yaml
   # .pre-commit-config.yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.3.0
       hooks:
         - id: ruff
           args: [--fix]
         - id: ruff-format
     - repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.8.0
       hooks:
         - id: mypy
           additional_dependencies: [types-requests]
   ```

2. **Create development Makefile**:
   ```makefile
   .PHONY: install test lint format clean
   
   install:
   	uv sync --all-extras
   	pre-commit install
   
   test:
   	uv run pytest -xvs --cov=src/twat_search
   
   lint:
   	uv run ruff check --fix
   	uv run mypy src/twat_search
   
   format:
   	uv run ruff format
   
   clean:
   	find . -type d -name __pycache__ -delete
   	find . -name "*.pyc" -delete
   ```

3. **Add Docker development environment**:
   ```dockerfile
   # Dockerfile.dev
   FROM python:3.12-slim
   RUN pip install uv
   WORKDIR /app
   COPY pyproject.toml uv.lock ./
   RUN uv sync --all-extras
   COPY . .
   CMD ["uv", "run", "pytest"]
   ```

### 7. Enhance Documentation

**Problem**: While README is comprehensive, API documentation and examples need improvement.

**Specific Actions**:
1. **Add docstring examples to all public methods**:
   ```python
   async def search(self, query: str) -> list[SearchResult]:
       """Search for the given query.
       
       Args:
           query: The search query string
           
       Returns:
           List of search results
           
       Example:
           >>> engine = BraveSearchEngine(api_key="your_key")
           >>> results = await engine.search("python programming")
           >>> print(f"Found {len(results)} results")
           Found 10 results
       """
   ```

2. **Create API documentation with Sphinx**:
   ```python
   # docs/conf.py
   extensions = [
       'sphinx.ext.autodoc',
       'sphinx.ext.viewcode',
       'sphinx.ext.napoleon',
       'sphinx_autodoc_typehints'
   ]
   ```

3. **Add usage examples for each engine**:
   ```python
   # examples/engine_usage.py
   async def demonstrate_brave_search():
       engine = BraveSearchEngine(api_key=os.getenv("BRAVE_API_KEY"))
       results = await engine.search("artificial intelligence")
       for result in results[:5]:
           print(f"{result.title}: {result.url}")
   ```

### 8. Implement Result Caching Strategy

**Problem**: No caching leads to repeated API calls and potential rate limiting.

**Specific Actions**:
1. **Add Redis-based caching**:
   ```python
   # In api.py
   from twat_cache import ucache
   
   @ucache(maxsize=1000, ttl=3600, namespace="search_results")
   async def cached_search(query: str, engines: list[str]) -> list[SearchResult]:
       return await search(query, engines=engines)
   ```

2. **Implement result deduplication**:
   ```python
   def deduplicate_results(results: list[SearchResult]) -> list[SearchResult]:
       seen_urls = set()
       unique_results = []
       for result in results:
           if result.url not in seen_urls:
               seen_urls.add(result.url)
               unique_results.append(result)
       return unique_results
   ```

3. **Add cache management CLI commands**:
   ```python
   # In cli.py
   def cache_clear(self):
       """Clear the search result cache."""
       # Implementation for cache clearing
       
   def cache_stats(self):
       """Show cache statistics."""
       # Implementation for cache stats
   ```

## 📈 LOW PRIORITY (Feature Enhancements)

### 9. Add New Search Engines

**Specific Actions**:
1. **Implement Kagi search engine**:
   ```python
   # engines/kagi.py
   class KagiSearchEngine(SearchEngine):
       def __init__(self, api_key: str):
           super().__init__(name="kagi")
           self.api_key = api_key
           self.base_url = "https://kagi.com/api/v0/search"
   ```

2. **Add Ecosia search engine**:
   ```python
   # engines/ecosia.py
   class EcosiaSearchEngine(SearchEngine):
       # Implementation using web scraping
   ```

### 10. Implement Advanced Search Features

**Specific Actions**:
1. **Add search result ranking**:
   ```python
   def rank_results(results: list[SearchResult], query: str) -> list[SearchResult]:
       # Implement TF-IDF or similar ranking algorithm
       pass
   ```

2. **Add search filters**:
   ```python
   class SearchFilters(BaseModel):
       date_range: tuple[datetime, datetime] | None = None
       language: str | None = None
   from typing import Optional
   class SearchFilters(BaseModel):
       date_range: tuple[datetime, datetime] | None = None
       region: Optional[str] = None
       language: str | None = None
   from typing import Optional
   class SearchFilters(BaseModel):
       date_range: tuple[datetime, datetime] | None = None
       language: Optional[str] = None
       region: Optional[str] = None
       content_type: Optional[str] = None
   ```

3. **Implement image and news search**:
   ```python
   from typing import List
   async def search_images(query: str, engines: List[str]) -> List[ImageResult]:
       # Implementation for image search
       pass
   ```

### 11. Performance Optimizations

**Specific Actions**:
1. **Add request connection pooling**:
   ```python
   # Use a shared aiohttp session across engines
   session = aiohttp.ClientSession(
       connector=aiohttp.TCPConnector(limit=100),
       timeout=aiohttp.ClientTimeout(total=30)
   )
   ```

2. **Implement smart timeout handling**:
   ```python
   async def search_with_adaptive_timeout(engine, query):
       base_timeout = 10
       for attempt in range(3):
           timeout = base_timeout * (2 ** attempt)
           try:
               return await asyncio.wait_for(engine.search(query), timeout=timeout)
           except asyncio.TimeoutError:
               continue
   ```

## 🔍 MONITORING & OBSERVABILITY

### 12. Add Comprehensive Logging and Metrics

**Specific Actions**:
1. **Implement structured logging**:
   ```python
   import structlog
   
   logger = structlog.get_logger()
   
   async def search(query: str):
       logger.info("search_started", query=query, engines=engines)
       # ... search logic ...
       logger.info("search_completed", 
                  query=query, 
                  result_count=len(results),
                  duration=time.time() - start_time)
   ```

2. **Add performance metrics**:
   ```python
   from prometheus_client import Counter, Histogram
   
   search_requests = Counter('search_requests_total', 'Total search requests', ['engine'])
   search_duration = Histogram('search_duration_seconds', 'Search duration', ['engine'])
   ```

## IMPLEMENTATION TIMELINE

### Phase 1 (Week 1-2): Critical Fixes
- Fix Falla engine dependencies and type issues
- Standardize search result processing
- Implement basic error handling

### Phase 2 (Week 3-4): Quality Improvements  
- Enhance test coverage to 80%+
- Modernize configuration management
- Add pre-commit hooks and development workflow

### Phase 3 (Week 5-6): Developer Experience
- Complete documentation overhaul
- Implement caching strategy
- Add performance monitoring

### Phase 4 (Week 7-8): Feature Enhancements
- Add new search engines
- Implement advanced search features
- Performance optimizations

## SUCCESS METRICS

**Code Quality**:
- Test coverage: 80%+ (currently ~19%)
- Type coverage: 95%+ (currently ~70%)
- Linting errors: 0 (currently ~50)

**Performance**:
- Average search time: <2 seconds
- Success rate: >95%
- Cache hit rate: >60%

**Developer Experience**:
- Documentation coverage: 100% of public APIs
- Example coverage: 100% of engines
- Development setup time: <5 minutes

This improvement plan addresses the most critical issues first while building toward a more robust, maintainable, and feature-rich search library. Each phase builds on the previous one, ensuring continuous improvement without breaking existing functionality.