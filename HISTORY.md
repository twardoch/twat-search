---
this_file: HISTORY.md
---

# The Chronicles of `twat-search`: A Tale of Engines, APIs, and Async Adventures

*Or: How a Human and AI Built a Multi-Engine Search Aggregator That Actually Works (Most of the Time)*

## The Genesis (February 13th, 2025)

It was a cold Thursday evening when the first line of code was committed. The initial commit on `d7c6417` was deceptively modest—just a skeleton with dreams:

```bash
Initial commit
 .github/workflows/push.yml    | 112 +++++++++++++++
 .gitignore                    | 315 ++++++++++++++++++++++++++++++++++++++++++
 pyproject.toml                | 263 +++++++++++++++++++++++++++++++++++
 src/twat_search/__init__.py   |   5 +
 tests/test_package.py         |   6 +
```

At this point, `twat-search` was just a glimmer in Adam Twardoch's eye—a plugin for the greater `twat` framework that would eventually wrangle the wild west of web search engines into submission. The initial `pyproject.toml` already hinted at grand ambitions with its carefully categorized optional dependencies and comprehensive CI/CD setup.

## The Great Engine Awakening (Early 2025)

What followed was a flurry of activity that would make any search engine jealous. Over the next few weeks, the repository exploded into life with **106 commits** in a remarkably short timespan—a testament to the power of human-AI collaboration.

### The First Engines Rise

The early commits tell a story of methodical expansion. First came the infrastructure:

```python
# src/twat_search/web/engines/base.py - The Foundation
class SearchEngine(ABC):
    """Base class for all search engines"""
    
    @abstractmethod
    async def search(self, query: str) -> list[SearchResult]:
        """Every engine must implement this sacred method"""
        pass
```

Then, one by one, the engines came online:

**Brave Search** (`brave.py`) - The API-powered heavyweight:
```python
async def search(self, query: str) -> list[SearchResult]:
    # Because who doesn't love a search engine with an attitude?
    url = f"{self.base_url}/web/search"
    params = {"q": query, "count": self.num_results}
```

**DuckDuckGo** (`duckduckgo.py`) - The privacy-conscious alternative:
```python
# The engine that doesn't track you (but we track its results)
from duckduckgo_search import DDGS
```

**The Falla Collection** (`falla.py`) - The browser-automated cavalry:
```python
# When APIs fail, we scrape. When scraping fails, we automate browsers.
# This is the way.
```

## The Plugin Architecture Emerges

One of the most elegant aspects of the project was its integration with the `twat` framework. The `pyproject.toml` reveals this beautifully:

```toml
[project.entry-points."twat.plugins"]
search = 'twat_search'
```

This single line transforms `twat-search` from a standalone tool into a seamless plugin, demonstrating the power of well-designed extension systems.

## The Engine Zoo Expands

As the project matured, it became clear that no single search engine could rule them all. The solution? Support *all* of them:

- **API-based engines**: Brave, Tavily, Perplexity, SerpAPI, HasData
- **Scraping engines**: Bing Scraper, Google Scraper  
- **Browser-automated engines**: The entire Falla collection (Google, Yahoo, Bing, DuckDuckGo, Ask, AOL, Dogpile, Gibiru, Mojeek, Qwant, Yandex)

The engine discovery system in `engines/__init__.py` became a thing of beauty:

```python
# A self-aware import system that gracefully handles missing dependencies
try:
    from twat_search.web.engines.brave import BraveSearchEngine, brave
    available_engine_functions["brave"] = brave
except ImportError:
    # No Brave API key? No problem. The show must go on.
    pass
```

## The Configuration Conundrum

Managing configuration for dozens of search engines with varying requirements became an art form. The team solved this with a sophisticated system:

```python
# Environment variables for the masses
BRAVE_API_KEY="your_key_here"
BRAVE_ENABLED=true
BRAVE_DEFAULT_PARAMS='{"count": 10, "safesearch": "moderate"}'

# Programmatic configuration for the elite
config = Config(
    engines={
        "brave": EngineConfig(
            enabled=True,
            api_key="runtime_override",
            default_params={"count": 5}
        )
    }
)
```

## The Async Revolution

The decision to build everything async from the ground up was crucial. The main search function in `api.py` showcases this beautifully:

```python
async def search(
    query: str,
    engines: list[str] | None = None,
    num_results: int = 5,
    **kwargs: Any,
) -> list[SearchResult]:
    # Launch all engines in parallel - because waiting is for synchronous peasants
    results = await asyncio.gather(*tasks, return_exceptions=True)
```

This approach allows `twat-search` to query multiple engines simultaneously, dramatically reducing search times from sequential seconds to parallel milliseconds.

## The Great Falla Integration

Perhaps the most ambitious feature was the integration with the Falla library for browser automation. The `lib_falla` subdirectory contains an entire ecosystem:

```
lib_falla/
├── core/
│   ├── google.py      # The crown jewel
│   ├── bing.py        # Microsoft's offering
│   ├── yahoo.py       # The has-been that still works
│   └── ...           # An alphabet soup of search engines
```

This allowed `twat-search` to scrape search engines that don't offer APIs, using Playwright to automate real browsers. It's like having a digital intern who never sleeps and never complains about captchas.

## Error Handling: The Art of Graceful Failure

One of the project's strengths is its robust error handling. When one engine fails, others carry on:

```python
async def search_with_error_handling() -> list[SearchResult]:
    try:
        return await engine_instance.search(query)
    except Exception as e:
        logger.error(f"Search with engine '{engine_name}' failed: {e}")
        # Return empty results on failure instead of raising
        # Because the show must go on, even when Google has a bad day
        return []
```

## The Testing Philosophy

The project embraces a pragmatic testing approach. The `tests/` directory contains unit tests, integration tests, and even benchmark tests:

```python
@pytest.mark.benchmark(group="search")
def test_search_performance(benchmark):
    result = benchmark(run_sync_search, "python programming")
    # Because knowing your search is fast is almost as important as it working
```

## The CLI Experience

The command-line interface, powered by Python Fire, makes the tool accessible to humans:

```bash
# Search across all configured engines
twat-search web q "latest advancements in AI"

# Cherry-pick your engines like a connoisseur  
twat-search web q "Python programming" -e brave,duckduckgo

# JSON output for the machines
twat-search web q "future of tech" --json
```

## The Caching Strategy

Using the `twat-cache` framework, searches can be cached to reduce API calls and improve response times:

```python
# @ucache(maxsize=1000, ttl=3600)  # Cache 1000 searches for 1 hour
# Currently commented out, but ready for deployment
```

## The Modern Python Stack

The project showcases modern Python development practices:

- **Pydantic v2** for data validation and settings management
- **httpx** for async HTTP clients  
- **Playwright** for browser automation
- **Hatch** for build and project management
- **Ruff** for lightning-fast linting and formatting
- **uv** for dependency management

## Recent Evolution: The Review Phase

The recent commits show a project in reflection mode. The `REVIEW/` folder contains comprehensive analysis:

- `FILES-cod.md` - A complete catalog of the codebase
- `TODO-cla.md` - An improvement roadmap with surgical precision

This self-awareness phase demonstrates the maturity of the human-AI collaboration, acknowledging technical debt while planning systematic improvements.

## The Numbers Game

By the commit count, the project reached **106 commits** in its active development phase, with version tags climbing from v2.3.3 to v2.7.7. The codebase spans:

- **64 Python files** (according to the review documents)
- **12 search engines** with various implementations
- **Support for 3 Python versions** (3.10, 3.11, 3.12)
- **Comprehensive CI/CD** with GitHub Actions

## The Philosophy Behind the Code

What makes `twat-search` special isn't just its technical capabilities, but its philosophical approach:

1. **Graceful Degradation**: If one engine fails, others continue
2. **Pluggable Architecture**: Easy to add new engines without touching core code
3. **Configuration Flexibility**: Environment variables for ops teams, programmatic config for developers
4. **Modern Async**: Built for the concurrent web from day one
5. **Developer Experience**: Rich CLI, comprehensive documentation, battle-tested CI/CD

## Lessons from the Trenches

The development revealed several insights:

- **API reliability varies wildly** - Hence the multi-engine approach
- **Browser automation is complex but powerful** - The Falla integration proves this
- **Configuration management is harder than it looks** - The elaborate env var system shows the pain
- **Error handling makes or breaks user experience** - The graceful failure system is crucial
- **Testing real web services is challenging** - Mock engines and careful integration tests are essential

## The Road Ahead

The comprehensive TODO list in `REVIEW/TODO-cla.md` outlines ambitious plans:

- Fix Falla engine type issues
- Enhance test coverage to 80%+
- Implement Redis-based caching
- Add new search engines (Kagi, Ecosia)
- Performance optimizations
- Advanced search features

## The Human-AI Collaboration Story

This project exemplifies effective human-AI collaboration:

- **Human**: Provided vision, architecture decisions, and domain expertise
- **AI**: Implemented detailed code, handled refactoring, and maintained consistency
- **Together**: Created a production-ready tool with enterprise-grade CI/CD

The commit messages tell this story—from initial architectural decisions to detailed implementations to comprehensive reviews. Each phase built on the previous, creating a sophisticated search aggregation tool that would be challenging for any single developer to create in such a short timeframe.

## Conclusion: A Search Engine to Rule Them All

`twat-search` stands as a testament to what's possible when human creativity meets AI implementation speed. It's not just a search aggregator—it's a platform for search innovation, a showcase of modern Python practices, and a proof of concept for the future of human-AI collaboration.

In a world where search is increasingly fragmented across walled gardens and specialized engines, `twat-search` offers a unified interface that's both powerful for developers and accessible to users. It's the Swiss Army knife of search, ready for whatever query you throw at it.

*And somewhere in the code, amidst all the async functions and error handlers, lies the simple truth: sometimes the best way to find what you're looking for is to ask everyone at once.*

---

*Built with ♥️ by Adam Twardoch and AI collaborators*  
*"Making search searchable since 2025"*