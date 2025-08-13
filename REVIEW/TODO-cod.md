---
this_file: REVIEW/TODO-cod.md
title: Improvement Plan and Proposals
description: Example-illustrated, specific plan to improve the repository without changing code yet
---

# Improvement Plan (Proposals)

This plan outlines targeted, concrete improvements to the repository. It is example-illustrated and scoped to be incremental and low-risk. No code changes are made here; this simply proposes specific actions for follow-up PRs.

## Goals

- Tighten developer experience (DX) and consistency.
- Improve engine architecture clarity and documentation.
- Strengthen tests for engines/config/CLI, with reliable mocks.
- Align packaging/extras with README and CI, reduce duplication.
- Enhance logging/observability and error handling for end users.

## High-Impact Proposals

1) Logging and Diagnostics
- Rationale: Current mix relies on `logging`. The project standards request Loguru-style verbose mode. Users need easier toggles and richer diagnostics in CLI and API.
- Actions:
  - Add a thin logging wrapper with Loguru, default INFO, `--verbose`/`--quiet` flags in CLI mapped to levels.
  - Emit per-engine structured context (engine, params, duration, result_count) and collapse errors to human-friendly messages.
  - Surface a `TWAT_SEARCH_LOG_LEVEL` env override.
- Example (concept sketch):
  ```python
  # src/twat_search/web/utils_logging.py
  from loguru import logger

  def setup_logging(level: str = "INFO"):
      logger.remove()
      logger.add(lambda msg: print(msg, end=""), level=level)
      return logger
  ```
  ```python
  # In CLI: --verbose -> DEBUG; --quiet -> WARNING
  logger = setup_logging(level)
  logger.bind(engine=name).info("Querying", query=q)
  ```

2) Configuration Consistency and Docs
- Rationale: README is excellent but long; env var patterns and extras should be machine-verifiable and discoverable via CLI.
- Actions:
  - Generate a machine-readable matrix of engines → required env vars → extras (from `config.py` and `engines/*`).
  - Add `twat-search web info --json` to emit that full matrix for tooling.
  - Normalize environment variable names in code and docs (e.g., ALL_CAPS, `_ENABLED`, `_DEFAULT_PARAMS`).
  - Document precedence rules (programmatic Config > env > defaults) with short examples.
- Example (CLI JSON):
  ```bash
  twat-search web info --json | jq '.engines[] | {id, requires_api_key, extra}'
  ```

3) Extras Alignment and Packaging
- Rationale: README lists extras; ensure `pyproject.toml` matches and CI tests each extra set.
- Actions:
  - Verify extras groups: `all`, `brave`, `duckduckgo`, `serpapi`, `hasdata`, `falla`, `bing_scraper`, `pplx`, `tavily`, `you`.
  - Add a CI matrix job that installs each extra set and runs a narrow smoke test for its engines.
  - Remove duplicate dependency declarations between `requirements.txt` and `pyproject.toml` or clearly scope `requirements.txt` to dev only.
- Example (CI step):
  ```yaml
  strategy:
    matrix:
      extra: [duckduckgo, brave, serpapi, falla]
  steps:
    - run: uv pip install --system ".[${{ matrix.extra }}]"
    - run: pytest tests/unit/web/engines/test_base.py -q
  ```

4) Engine API Contract and Mocks
- Rationale: Engines implement a consistent ABC; reinforce this with shared tests and better mocks so engines can be iterated independently.
- Actions:
  - Expand `tests/unit/web/engines/test_base.py` with contract tests (timeouts, parameter mapping, result schema).
  - Provide a robust `MockEngine` that supports param echoing, errors, and delays; use in `tests/unit/web/test_api.py` for concurrency determinism.
  - Add a `--dry-run` mode in CLI that lists which engines would run and with which params.
- Example (contract test idea):
  ```python
  # Assert engines respect num_results when supported
  results = await engine.search("q")
  assert len(results) <= expected
  ```

5) CLI UX: Flags and Output
- Rationale: The CLI is powerful; add helpful affordances and consistent options.
- Actions:
  - Add flags: `--verbose/--quiet`, `--dry-run`, `--engine-params key=value[,key=value]`, `--save-json path`.
  - Plain table view and condensed JSON lines (`--jsonl`) for streaming into tools.
  - `web info` to print a compact table with enabled/disabled, key presence.
- Example:
  ```bash
  twat-search web q "topic" -e brave,duckduckgo --num_results 7 --jsonl > out.jsonl
  ```

6) Error Handling and User Guidance
- Rationale: Gracefully handle partial failures; guide users on missing keys or misconfig.
- Actions:
  - Centralize exceptions with remediation tips (missing API key -> which env var; disabled engine -> how to enable).
  - Return partial results but annotate `extra_info.error` with cause and engine.
- Example result snippet:
  ```json
  {"source_engine":"brave","title":"..","url":"..","snippet":"..","extra_info":{"duration_ms":121}}
  {"source_engine":"serpapi","extra_info":{"error":"Missing SERPAPI_API_KEY"}}
  ```

7) Caching and Rate Control
- Rationale: `twat_cache.ucache` is imported; clarify policy and tune defaults per engine.
- Actions:
  - Make cache opt-in via env/CLI (`--cache-ttl`), and document storage backend choices.
  - Implement per-engine delay/backoff hooks to respect API rate limits.

8) Documentation Structure and Examples
- Rationale: README is thorough; extract some deep-dive content into dedicated docs to keep front page lean.
- Actions:
  - Create `docs/` with concise guides: Quickstart, Engines, Config, CLI, Development.
  - Add end-to-end examples (programmatic and CLI) including engine-specific params and environment setup.
  - Cross-link `resources/` engine notes from docs.

9) Repository Hygiene and Metadata
- Rationale: Reduce duplication and ensure discoverability.
- Actions:
  - Ensure all markdown files include YAML frontmatter `this_file` as per repo standards.
  - Consider replacing `VERSION.txt` with dynamic version via `hatch-vcs` (already present) or keep `VERSION.txt` as single source of truth and wire into `pyproject.toml`.
  - Ensure `.pre-commit-config.yaml` runs ruff/format consistently with CI.

10) CI Enhancements
- Rationale: CI is strong; small upgrades help reliability and visibility.
- Actions:
  - Upload coverage XML to Codecov (if desired) and fail on significant drops.
  - Add a smoke test job that runs the CLI `web info` and `web q` with `-e duckduckgo --num_results 1` when key-free.
  - Turn `*.yml.template` into reusable workflows or document how to instantiate them.

## Sequenced Execution Plan (MVP → Enhancements)

Phase 1: Foundation and Clarity
- Add docs skeleton under `docs/` and move deep-dive sections out of README (keep a tight README).
- Implement CLI `--verbose/--quiet` and normalize logging level handling. Add `web info --json`.
- Align extras in `pyproject.toml` with README table. Update `SETUP_CI_CD.md` with matrix testing.

Phase 2: Testing and Reliability
- Strengthen engine ABC contract tests and mocks; add CLI smoke in CI without secrets.
- Add error messaging with remediation tips; annotate results with `extra_info` context.
- Optional: Introduce cache flags and document policies.

Phase 3: UX and Docs Polish
- Add `--dry-run`, `--jsonl`, and `--save-json` flags.
- Publish curated examples (per engine) and troubleshooting sections.
- Consider extracting Falla library as optional vendored module docs with clear maintenance policy.

## Concrete Example Changes (Illustrative Only)

1) CLI verbose flag mapping
```python
# In web/cli.py
if verbose and quiet:
    raise SystemExit("Use either --verbose or --quiet, not both.")
level = "DEBUG" if verbose else ("WARNING" if quiet else os.getenv("TWAT_SEARCH_LOG_LEVEL","INFO"))
setup_logging(level)
```

2) Engine parameter pass-through
```bash
twat-search web q "q" -e brave --engine-params country=US,lang=en,num_results=3
```
```python
# Parse key=value pairs and merge into engine-specific kwargs.
```

3) JSONL output
```bash
twat-search web q "site:example.com docs" --jsonl > results.jsonl
```

4) Error remediation message
```text
Engine 'serpapi' failed: Missing SERPAPI_API_KEY
Hint: export SERPAPI_API_KEY=... or disable with SERPAPI_ENABLED=false
```

## Acceptance Criteria

- CLI supports clear verbosity control; docs reflect it with examples.
- `pyproject.toml` extras fully aligned with README and CI matrix.
- `web info --json` outputs accurate engine matrix with env and extras mapping.
- Tests cover engine base contracts and API orchestrator edge cases with stable mocks.
- Improved error messages and result annotations are present and documented.

## Deferred/Consider Later

- Pluggable engine discovery via entry points to allow out-of-tree engines.
- Optional telemetry on anonymous usage stats (opt-in) to guide defaults.
- Async streaming of results as they arrive (`--stream`), with incremental rendering.

## Notes for Implementers

- Keep changes incremental and focused. Touch minimal files per PR.
- Favor pure functions and small helpers; ensure high cohesion.
- Avoid breaking public API; deprecate with warnings before removals.

