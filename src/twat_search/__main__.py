#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire>=0.5.0", "rich>=13.6.0"]
# ///
# this_file: src/twat_search/__main__.py
"""
Main entry point for the Twat Search CLI.
"""

from __future__ import annotations

import logging
from typing import Any, TypeVar

import fire  # type: ignore
from rich.ansi import AnsiDecoder
from rich.console import Console, Group
from rich.logging import RichHandler
from rich.theme import Theme
from rich.traceback import install

from twat_search import web  # Keep for potential use, handle import error at usage
from twat_search.__version__ import version as project_version # Alias to avoid conflict

# Set up logging with rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)
console = Console()

# Define types for the CLI components
SearchCLIType = TypeVar("SearchCLIType")


class TwatSearchCLI:
    """Twat Search Command Line Interface."""

    def __init__(self) -> None:
        """Initialize the Twat Search CLI."""
        try:
            # Access the cli attribute from the imported web module
            if web and hasattr(web, "cli") and hasattr(web.cli, "SearchCLI"):
                self.web: Any = web.cli.SearchCLI()
            else:
                raise AttributeError("SearchCLI not found in twat_search.web.cli")
        except (ImportError, AttributeError) as e:
            # Create a placeholder if the web CLI is not available
            logger.error(f"Web CLI not available: {e!s}")
            logger.error(
                "Make sure twat_search.web.cli is properly installed and accessible.",
            )
            self.web = self._cli_error

    @staticmethod
    def _cli_error(*args: Any, **kwargs: Any) -> int:
        """Placeholder function when web CLI is not available.

        Args are ignored but necessary to match any possible call signature.
        """
        # Use the module-level console instance
        console.print(
            "[bold red]Web CLI not available. Make sure twat_search.web.cli is properly installed.[/bold red]",
        )
        return 1

    @staticmethod
    def version() -> str:
        """Display the version of the Twat Search tool."""
        if project_version:
            return f"Twat Search version {project_version}"
        return "Twat Search (version not available)"


def main() -> None:
    install(show_locals=True)
    ansi_decoder = AnsiDecoder()
    # Use the module-level console instance, re-configure if necessary or use a new one
    # For simplicity, re-assigning to the global console for this specific theme.
    # Alternatively, pass console instance around or make Theme global.
    global console
    console = Console(theme=Theme({"prompt": "cyan", "question": "bold cyan"}))


    def display(lines, out):
        # Ensure this console is the themed one if that's intended for fire output
        console.print(Group(*map(ansi_decoder.decode_line, lines)))

    fire.core.Display = display

    fire.Fire(TwatSearchCLI, name="twat-search")


if __name__ == "__main__":
    main()
