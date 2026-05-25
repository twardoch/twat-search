# this_file: src/twat_search/web/browser_transport.py
"""Browser-backed transport diagnostics and failure evidence helpers."""

from __future__ import annotations

from twat_search.web.browser import (
    BrowserBlockSignal,
    BrowserChallengeError,
    BrowserEvidence,
    BrowserSignalKind,
    build_browser_evidence,
    detect_browser_signals,
    write_browser_failure_evidence,
)

__all__ = [
    "BrowserBlockSignal",
    "BrowserChallengeError",
    "BrowserEvidence",
    "BrowserSignalKind",
    "build_browser_evidence",
    "detect_browser_signals",
    "write_browser_failure_evidence",
]
