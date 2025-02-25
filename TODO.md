# twat-search Web Package - Future Tasks

The basic implementation of the `twat-search` web package is complete. 

Tip: Periodically run `./cleanup.py status` to see results of lints and tests. 

## 1. TODO

### 1.1. Review and extend engines

#### 1.1.1. Tavily (should be accessible as engine `tavily`)

@https://docs.tavily.com/sdk/python/get-started
@https://github.com/tavily-ai/tavily-python
@https://docs.tavily.com/sdk/python/reference
@https://docs.tavily.com/sdk/javascript/get-started


#### 1.1.2. Brave

- Web search (should be accessible as engine `brave`)

@https://api-dashboard.search.brave.com/app/documentation/web-search/get-started
@https://api-dashboard.search.brave.com/app/documentation/web-search/query
@https://api-dashboard.search.brave.com/app/documentation/web-search/request-headers
@https://api-dashboard.search.brave.com/app/documentation/web-search/response-headers
@https://api-dashboard.search.brave.com/app/documentation/web-search/responses
@https://api-dashboard.search.brave.com/app/documentation/web-search/codes

- News search (should be accessible as engine `brave-news`)

@https://api-dashboard.search.brave.com/app/documentation/news-search/get-started
@https://api-dashboard.search.brave.com/app/documentation/news-search/query
@https://api-dashboard.search.brave.com/app/documentation/news-search/request-headers
@https://api-dashboard.search.brave.com/app/documentation/news-search/response-headers
@https://api-dashboard.search.brave.com/app/documentation/news-search/responses
@https://api-dashboard.search.brave.com/app/documentation/news-search/codes

#### 1.1.3. You.com

- Web search (should be accessible as engine `you`)

@https://documentation.you.com/api-reference/search

- News search (`you-news`)

@https://documentation.you.com/api-reference/news

#### 1.1.4. SerpApi 

- Google Search (`serpapi`)

@https://serpapi.com/search-api





### 1.2. Testing Plan

The following tests should be implemented to ensure the robustness and reliability of the package:

#### 1.2.1. Unit Tests

##### Core API
- Test `search` function
  - Test with single engine
  - Test with multiple engines
  - Test with custom configuration
  - Test with engine-specific parameters
  - Test error handling (no engines, all engines fail)
  - Test empty result handling

##### Models
- Test `SearchResult` model
  - Test validation of URLs (valid and invalid)
  - Test serialization/deserialization

##### Configuration
- Test `Config` class
  - Test loading from environment variables
  - Test loading from .env file
  - Test default configuration
- Test `EngineConfig` class
  - Test enabled/disabled functionality
  - Test default parameters

##### Utilities
- Test `RateLimiter` class
  - Test it properly limits requests to specified rate
  - Test with different rate limits
  - Test behavior under high load

##### Exceptions
- Test `SearchError` and `EngineError` classes
  - Test proper error message formatting
  - Test exception hierarchy

#### 1.2.2. Engine-specific Tests

For each search engine implementation (Brave, Google, Tavily, Perplexity, You.com):

- Test initialization
  - Test with valid configuration
  - Test with missing API key
  - Test with custom parameters
- Test search method
  - Test with mock responses (happy path)
  - Test error handling
    - Connection errors
    - API errors (rate limits, invalid requests)
    - Authentication errors
    - Timeout errors
  - Test response parsing
    - Valid responses
    - Malformed responses
    - Empty responses

#### 1.2.3. Integration Tests

- Test the entire search flow
  - Test search across multiple engines
  - Test fallback behavior when some engines fail
  - Test rate limiting in real-world scenarios

#### 1.2.4. Type Checking Tests

- Add tests to verify type hints are correct
- Fix existing mypy type errors identified in CLEANUP.txt
  - Fix HttpUrl validation issues
  - Fix BaseSettings issues in config.py
  - Fix missing return type annotations

#### 1.2.5. Performance Tests

- Benchmark search performance
  - Measure latency across different engines
  - Test with concurrent searches
  - Test with rate limiting

#### 1.2.6. Mock Implementation

Create mock implementations for testing that don't require actual API calls:

```python
# Example mock implementation
@register_engine
class MockSearchEngine(SearchEngine):
    name = "mock"
    
    async def search(self, query: str) -> list[SearchResult]:
        # Return predictable test results
        return [
            SearchResult(
                title="Mock Result 1",
                url="https://example.com/1",
                snippet="This is a mock result for testing",
                source=self.name
            )
        ]
```

#### 1.2.7. Test Utilities

- Create helper functions for testing
  - Mock response generators
  - Configuration helpers
  - Test data generators

#### 1.2.8. Continuous Integration

- Add GitHub workflow for running tests
- Add coverage reporting
- Add type checking to CI pipeline

Tests!!! FIXME Describe here in detail the planned tests before implementing them 

