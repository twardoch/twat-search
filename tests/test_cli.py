# this_file: tests/test_cli.py
"""CLI smoke tests for twat-search Fire entry points.

Each test runs a subprocess to verify that:
- --help exits 0 and prints usage to stdout
- version leaf exits 0 and prints a semver string
- each dashed-entry --help exits 0
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("_TEST_ENGINE", None)
    return subprocess.run(
        [sys.executable, "-m", "twat_search", *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def _run_module(module: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run a module directly via python -c import+call pattern using entry functions."""
    return subprocess.run(
        [sys.executable, "-c", f"from twat_search.__main__ import {module}; {module}()", *args],
        capture_output=True,
        text=True,
        check=False,
    )


# ---------------------------------------------------------------------------
# Top-level dispatcher tests
# ---------------------------------------------------------------------------


def test_help_exits_zero() -> None:
    """twat-search --help should exit 0."""
    result = _run("--help")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"


def test_help_lists_subcommands() -> None:
    """--help output should mention known subcommands."""
    result = _run("--help")
    combined = result.stdout + result.stderr
    assert "version" in combined.lower() or "web" in combined.lower(), (
        f"Expected subcommand listing in help output.\nOutput: {combined}"
    )


def test_version_exits_zero() -> None:
    """twat-search version should exit 0."""
    result = _run("version")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"


def test_version_prints_semver() -> None:
    """twat-search version should print a semver-like string."""
    result = _run("version")
    combined = result.stdout + result.stderr
    assert re.search(r"\d+\.\d+", combined), f"Expected semver in output, got: {combined!r}"


# ---------------------------------------------------------------------------
# Leaf: list-engines
# ---------------------------------------------------------------------------


def test_list_engines_help_exits_zero() -> None:
    """twat-search list-engines --help should exit 0."""
    result = _run("list-engines", "--help")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"


# ---------------------------------------------------------------------------
# Group: web
# ---------------------------------------------------------------------------


def test_web_help_exits_zero() -> None:
    """twat-search web --help should exit 0."""
    result = _run("web", "--help")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"


def test_web_help_lists_subcommands() -> None:
    """twat-search web --help should mention q or info."""
    result = _run("web", "--help")
    combined = result.stdout + result.stderr
    assert any(sub in combined for sub in ("q", "info", "brave", "duckduckgo")), (
        f"Expected web subcommands in help output.\nOutput: {combined}"
    )


def test_web_info_json_outputs_engine_metadata() -> None:
    """twat-search web info --json should emit machine-readable provider metadata."""
    result = _run("web", "info", "--json")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    data = json.loads(result.stdout)
    assert data["brave"]["transport"] == "api"
    assert data["brave"]["status"] == "implemented"
    assert data["brave"]["proxy_policy"] == "none"


def test_web_q_free_preset_uses_catalog_filter() -> None:
    """The free preset should not expand to API-key-only providers."""
    result = _run("web", "q", "catalog smoke", "-e", "free", "--json")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    combined = result.stdout + result.stderr
    assert "API key is required" not in combined


def test_web_q_explain_json_outputs_search_metadata() -> None:
    """twat-search web q --explain --json should include explain metadata."""
    result = _run("web", "q", "catalog smoke", "-e", "free", "--explain", "--json")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    data = json.loads(result.stdout)
    assert "explain" in data
    assert "results" in data
    assert "selected_engines" in data["explain"]
    assert "proxy" in data["explain"]
    assert "llm_steps" in data["explain"]


# ---------------------------------------------------------------------------
# Dashed-entry cmd_* functions (via python -c invocation)
# ---------------------------------------------------------------------------


def _run_cmd(fn_name: str, *extra: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        "-c",
        f"import sys; sys.argv = ['{fn_name}', '--help']; from twat_search.__main__ import {fn_name}; {fn_name}()",
    ]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def test_cmd_version_help_exits_zero() -> None:
    """cmd_version --help should exit 0."""
    result = _run_cmd("cmd_version")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"


def test_cmd_list_engines_help_exits_zero() -> None:
    """cmd_list_engines --help should exit 0."""
    result = _run_cmd("cmd_list_engines")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"


def test_cmd_web_help_exits_zero() -> None:
    """cmd_web --help should exit 0 (legacy twat-search-web entry point)."""
    result = _run_cmd("cmd_web")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"
