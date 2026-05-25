"""Smoke tests for the twat_search package contract."""

from __future__ import annotations

import subprocess
import sys
from importlib import metadata

import twat_search


def test_version() -> None:
    """Verify package exposes version."""
    assert twat_search.__version__


def test_public_contract_exports() -> None:
    """The package exposes the public API used by the twat host."""
    assert callable(twat_search.main)
    assert "__version__" in twat_search.__all__
    assert "main" in twat_search.__all__


def test_installed_entry_points() -> None:
    """Installed metadata exposes direct and host-dispatched CLIs."""
    console_scripts = metadata.entry_points(group="console_scripts")
    scripts = {entry_point.name: entry_point.value for entry_point in console_scripts}
    assert scripts["twat-search"] == "twat_search.__main__:main"

    plugin_entries = metadata.entry_points(group="twat.plugins")
    plugins = {entry_point.name: entry_point.value for entry_point in plugin_entries}
    assert plugins["search"] == "twat_search"


def test_python_module_help_smoke() -> None:
    """`python -m twat_search --help` reaches the Fire CLI."""
    result = subprocess.run(
        [sys.executable, "-m", "twat_search", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    help_text = result.stdout + result.stderr
    assert "twat-search" in help_text
    assert "version" in help_text
