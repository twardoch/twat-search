# this_file: src/twat_search/__main__.py
"""Fire CLI entry point for twat-search."""

from __future__ import annotations

import fire


def _version() -> str:
    """Print the installed package version."""
    from twat_search.__version__ import __version__  # noqa: PLC0415

    return __version__


def _list_engines() -> None:
    """List all known search engines and their availability."""
    from twat_search.web.cli import SearchCLI  # noqa: PLC0415

    SearchCLI().info()


def _make_commands() -> dict[str, object]:
    """Build COMMANDS dict lazily so web imports don't run at module load time."""
    from twat_search.web.cli import SearchCLI  # noqa: PLC0415

    return {
        "version": _version,
        "list-engines": _list_engines,
        "web": SearchCLI(),
    }


# Explicit allow-list per SPEC §6.
# Populated lazily in main() to keep optional-dep imports deferred.
COMMANDS: dict[str, object] = {
    "version": _version,
    "list-engines": _list_engines,
    # 'web' group added at runtime in main() to avoid eager import of SearchCLI
}


def main() -> None:
    """Top-level dispatcher: twat-search <subcommand> …"""
    fire.Fire(_make_commands(), name="twat-search")


# ---------------------------------------------------------------------------
# Dashed-entry helpers — one per leaf and group (SPEC §4.2 / §4.3)
# ---------------------------------------------------------------------------


def cmd_version() -> None:
    """Entry point for twat-search-version."""
    fire.Fire(_version, name="twat-search-version")


def cmd_list_engines() -> None:
    """Entry point for twat-search-list-engines."""
    fire.Fire(_list_engines, name="twat-search-list-engines")


def cmd_web() -> None:
    """Entry point for twat-search-web (also used as the legacy twat-search-web script)."""
    from twat_search.web.cli import main as web_main  # noqa: PLC0415

    web_main()


if __name__ == "__main__":
    main()
