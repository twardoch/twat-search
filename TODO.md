# twat-search Web Package - Future Tasks

The basic implementation of the `twat-search` web package is complete. 

Tip: Periodically run `./cleanup.py status` to see results of lints and tests. 

## TODO

### Testing Plan

The following tests should be implemented to ensure the robustness and reliability of the package:

#### 1. Unit Tests

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

#### 2. Engine-specific Tests

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

#### 3. Integration Tests

- Test the entire search flow
  - Test search across multiple engines
  - Test fallback behavior when some engines fail
  - Test rate limiting in real-world scenarios

#### 4. Type Checking Tests

- Add tests to verify type hints are correct
- Fix existing mypy type errors identified in CLEANUP.txt
  - Fix HttpUrl validation issues
  - Fix BaseSettings issues in config.py
  - Fix missing return type annotations

#### 5. Performance Tests

- Benchmark search performance
  - Measure latency across different engines
  - Test with concurrent searches
  - Test with rate limiting

#### 6. Mock Implementation

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

#### 7. Test Utilities

- Create helper functions for testing
  - Mock response generators
  - Configuration helpers
  - Test data generators

#### 8. Continuous Integration

- Add GitHub workflow for running tests
- Add coverage reporting
- Add type checking to CI pipeline

Tests!!! FIXME Describe here in detail the planned tests before implementing them 

