"""twat-search: Tools for web search and information retrieval."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("twat-search")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

# Configure twat_cache if available
try:
    import twat_cache

    from twat_search.paths import get_cache_dir

    # Configure twat_cache to use the paths from twat_os
    twat_cache.utils.get_cache_path = lambda *args, **kwargs: get_cache_dir()
except ImportError:
    pass  # twat_cache is not installed, no configuration needed

__all__: list[str] = ["__version__"]

# Import submodules if available
try:
    from twat_search import web

    __all__.append("web")
except ImportError:
    pass


def main() -> None:
    """CLI entry point for twat-search."""
    print(f"twat-search v{__version__}")


__all__.append("main")
