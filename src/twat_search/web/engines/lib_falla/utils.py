# this_file: src/twat_search/web/engines/lib_falla/utils.py
"""
Utility functions for the Falla search engine scraper.

This module provides helper functions for working with Falla search engines.
"""

from pathlib import Path

# Import all the search engine implementations
from twat_search.web.engines.lib_falla.core.aol import Aol
from twat_search.web.engines.lib_falla.core.ask import Ask
from twat_search.web.engines.lib_falla.core.bing import Bing
from twat_search.web.engines.lib_falla.core.dogpile import DogPile
from twat_search.web.engines.lib_falla.core.duckduckgo import DuckDuckGo
from twat_search.web.engines.lib_falla.core.gibiru import Gibiru
from twat_search.web.engines.lib_falla.core.google import Google
from twat_search.web.engines.lib_falla.core.mojeek import Mojeek
from twat_search.web.engines.lib_falla.core.qwant import Qwant
from twat_search.web.engines.lib_falla.core.searchencrypt import SearchEncrypt
from twat_search.web.engines.lib_falla.core.startpage import StartPage
from twat_search.web.engines.lib_falla.core.yahoo import Yahoo
from twat_search.web.engines.lib_falla.core.yandex import Yandex


class Bcolors:
    """Terminal colors for pretty printing."""

    AUTRE = "\033[96m"  # rose
    HEADER = "\033[95m"  # rose
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"  # jaune
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def list_engines() -> list[str]:
    """
    List all available search engines.

    Returns:
        List[str]: List of available search engine names.
    """
    engines = []
    core_dir = Path(__file__).parent / "core"

    for file in core_dir.glob("*.py"):
        if file.name not in ["__init__.py", "__pycache__", "falla.py"]:
            engine_name = file.stem
            engines.append(engine_name)

    return engines


def get_results(engine: str, query: str, num_results: int = 10) -> list[dict[str, str]]:
    """
    Get search results from the specified engine.

    Args:
        engine: Name of the search engine to use
        query: Search query
        num_results: Number of results to return (default: 10)

    Returns:
        List[Dict[str, str]]: List of search results, each containing title, link, and snippet
    """
    engines = {
        "Aol": Aol,
        "Ask": Ask,
        "Bing": Bing,
        "DogPile": DogPile,
        "DuckDuckGo": DuckDuckGo,
        "Gibiru": Gibiru,
        "Google": Google,
        "Mojeek": Mojeek,
        "Qwant": Qwant,
        "SearchEncrypt": SearchEncrypt,
        "StartPage": StartPage,
        "Yahoo": Yahoo,
        "Yandex": Yandex,
    }

    if engine not in engines:
        msg = f"Engine {engine} not found"
        raise ValueError(msg)

    engine_instance = engines[engine]()
    results = engine_instance.search(query)

    # Limit the number of results
    if num_results and len(results) > num_results:
        results = results[:num_results]

    return results
