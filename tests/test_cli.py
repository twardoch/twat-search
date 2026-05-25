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

import pytest

ORIGINAL_ENV = os.environ.copy()
LIVE_CLI_GATE = "RUN_TWAT_SEARCH_LIVE_TESTS"


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


def _run_with_env(*args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    """Run the CLI with an explicit environment."""
    env = env.copy()
    env.pop("_TEST_ENGINE", None)
    return subprocess.run(
        [sys.executable, "-m", "twat_search", *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def _run_twat(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the installed twat dispatcher with the search plugin."""
    env = os.environ.copy()
    env.pop("_TEST_ENGINE", None)
    return subprocess.run(
        [sys.executable, "-m", "twat", "search", *args],
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


def test_twat_search_dispatcher_matches_twat_search_entry() -> None:
    """`twat search ...` should expose the same web behavior as `twat-search ...`."""
    direct = _run("web", "info", "--json")
    dispatched = _run_twat("web", "info", "--json")

    assert direct.returncode == 0, f"Expected exit 0, got {direct.returncode}\nstderr: {direct.stderr}"
    assert dispatched.returncode == 0, f"Expected exit 0, got {dispatched.returncode}\nstderr: {dispatched.stderr}"
    assert direct.stderr == ""
    assert dispatched.stderr == ""
    assert json.loads(dispatched.stdout) == json.loads(direct.stdout)


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


def test_web_providers_json_outputs_catalog_records() -> None:
    """twat-search web providers --json should emit provider catalog records."""
    result = _run("web", "providers", "--json")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    data = json.loads(result.stdout)
    brave = next(provider for provider in data["providers"] if provider["code"] == "brave")
    assert brave["transport"] == "api"
    assert brave["requires_api_key"] is True


def test_web_routes_json_outputs_selected_engines() -> None:
    """twat-search web routes --json should emit route policies and selections."""
    result = _run("web", "routes", "--json")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    data = json.loads(result.stdout)
    route_names = {route["name"] for route in data["routes"]}
    assert {"best", "fast", "cheap", "resilient", "deep", "browser", "api-only"}.issubset(route_names)


def test_web_doctor_json_outputs_readiness_payload() -> None:
    """twat-search web doctor --json should emit local readiness diagnostics."""
    result = _run("web", "doctor", "--json")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    data = json.loads(result.stdout)
    assert data["counts"]["implemented_providers"] > 0
    assert "proxy" in data
    assert "routes" in data
    assert isinstance(data["issues"], list)


def test_web_fetch_json_rejects_invalid_url_without_network() -> None:
    """twat-search web fetch --json should validate URL shape before network I/O."""
    result = _run("web", "fetch", "not-a-url", "--json")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert data["exception_type"] == "ValueError"
    assert "http://" in data["error"]


def test_web_q_jsonl_outputs_machine_readable_failure_records() -> None:
    """twat-search web q --jsonl should emit newline-delimited JSON records."""
    result = _run("web", "q", "catalog smoke", "-e", "does-not-exist", "--jsonl")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    records = [json.loads(line) for line in lines]

    assert [record["type"] for record in records] == ["request", "engine", "failure"]
    assert records[0]["request"]["query"] == "catalog smoke"
    assert records[1]["engine"] == "does_not_exist"
    assert records[1]["status"] == "failed"
    assert records[2]["failure"]["kind"] == "initialization"


def test_provider_sweep_shell_command_uses_plain_engine_listing() -> None:
    """The documented provider sweep shell loop has a stable engine source."""
    result = _run("web", "info", "--plain")
    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"

    engines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert "brave" in engines

    smoke_commands = [
        f'twat-search web q -e "{engine}" "Adam Twardoch" -n 1 --json --verbose' for engine in engines[:3]
    ]

    assert smoke_commands
    assert all(command.startswith('twat-search web q -e "') for command in smoke_commands)
    assert all(command.endswith('"Adam Twardoch" -n 1 --json --verbose') for command in smoke_commands)


@pytest.mark.online
@pytest.mark.requires_api_key
def test_live_brave_smoke_command_is_explicitly_gated() -> None:
    """Run the live Brave smoke command only when the live-test gate is explicit."""
    if ORIGINAL_ENV.get(LIVE_CLI_GATE) != "1":
        pytest.skip(f"Set {LIVE_CLI_GATE}=1 and BRAVE_API_KEY to run live CLI smoke tests.")
    if not ORIGINAL_ENV.get("BRAVE_API_KEY"):
        pytest.skip("Set BRAVE_API_KEY to run the live Brave CLI smoke test.")

    result = _run_with_env(
        "web",
        "q",
        "-e",
        "brave",
        "Adam Twardoch",
        "-n",
        "1",
        "--json",
        "--verbose",
        env=ORIGINAL_ENV,
    )

    assert result.returncode == 0, f"Expected exit 0, got {result.returncode}\nstderr: {result.stderr}"
    data = json.loads(result.stdout)
    assert "brave" in data
    assert len(data["brave"]["results"]) <= 1


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
