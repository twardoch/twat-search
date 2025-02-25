# 

The initial implementation of the `twat-search` web package is now complete. Key features implemented:

- Unified search API across multiple search engines
- Support for five search engines:
  - Brave Search
  - Google Search (via SerpAPI)
  - Tavily Search
  - Perplexity AI
  - You.com
- Asynchronous operations using asyncio and httpx
- Type safety with Pydantic models
- Comprehensive error handling
- Customizable configuration
- Example usage in `src/twat_search/web/example.py`

## Installation

```bash
pip install twat-search
```

## Usage

```python
import twat_search
plugin = twat_search.plugin
```

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development workflow management.

### Setup Development Environment

```bash
# Install hatch if you haven't already
pip install hatch

# Create and activate development environment
hatch shell

# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Run linting
hatch run lint

# Format code
hatch run format
```

## License

MIT License  
.
