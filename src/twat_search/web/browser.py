# this_file: src/twat_search/web/browser.py
"""Offline-testable browser diagnostics for browser-backed search engines."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from twat_search.web.config import BrowserConfig

BrowserSignalKind = Literal["captcha", "consent", "rate_limit", "bot_challenge", "blocked", "login"]

_BROWSER_SIGNAL_PATTERNS: tuple[tuple[BrowserSignalKind, re.Pattern[str]], ...] = (
    ("captcha", re.compile(r"\b(?:captcha|recaptcha|hcaptcha|g-recaptcha-response)\b", re.IGNORECASE)),
    ("captcha", re.compile(r"/sorry/index|unusual traffic", re.IGNORECASE)),
    ("bot_challenge", re.compile(r"challenge-form|action=[\"'][^\"']*challenge", re.IGNORECASE)),
    ("bot_challenge", re.compile(r"\b(?:cf-turnstile|cloudflare|botguard|challenge-platform)\b", re.IGNORECASE)),
    ("rate_limit", re.compile(r"\b(?:rate limit|too many requests|temporarily blocked)\b", re.IGNORECASE)),
    ("blocked", re.compile(r"\b(?:access denied|request blocked|automated queries|are you a robot)\b", re.IGNORECASE)),
    ("consent", re.compile(r"\b(?:cookie consent|consent page|accept all|reject all|privacy choices)\b", re.IGNORECASE)),
    ("consent", re.compile(r"consent\.(?:google|youtube)\.", re.IGNORECASE)),
    ("login", re.compile(r"\b(?:sign in to continue|login required|authentication required)\b", re.IGNORECASE)),
)


@dataclass(frozen=True)
class BrowserBlockSignal:
    """Detected browser-page state that may explain a failed or degraded search."""

    kind: BrowserSignalKind
    pattern: str
    excerpt: str


@dataclass(frozen=True)
class BrowserEvidence:
    """Failure evidence captured from a browser-backed search attempt."""

    engine: str
    query: str
    url: str | None = None
    title: str | None = None
    html_path: Path | None = None
    screenshot_path: Path | None = None
    signals: list[BrowserBlockSignal] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        """Return True when diagnostics indicate a blocking challenge."""
        return any(signal.kind in {"captcha", "rate_limit", "bot_challenge", "blocked"} for signal in self.signals)

    @property
    def needs_consent(self) -> bool:
        """Return True when diagnostics indicate a consent interstitial."""
        return any(signal.kind == "consent" for signal in self.signals)

    def to_failure_details(self) -> dict[str, object]:
        """Return JSON-serializable failure details for SearchFailure."""
        return {
            "browser": {
                "engine": self.engine,
                "query": self.query,
                "url": self.url,
                "title": self.title,
                "blocked": self.blocked,
                "needs_consent": self.needs_consent,
                "html_path": str(self.html_path) if self.html_path else None,
                "screenshot_path": str(self.screenshot_path) if self.screenshot_path else None,
                "signals": [
                    {
                        "kind": signal.kind,
                        "pattern": signal.pattern,
                        "excerpt": signal.excerpt,
                    }
                    for signal in self.signals
                ],
            },
        }


class BrowserChallengeError(RuntimeError):
    """Raised when a browser-backed engine encounters a block or consent state."""

    def __init__(self, evidence: BrowserEvidence, message: str | None = None) -> None:
        """Create an error that carries browser evidence into SearchFailure."""
        self.evidence = evidence
        signal_names = ", ".join(signal.kind for signal in evidence.signals) or "unknown"
        error_message = message or f"Browser challenge detected for {evidence.engine}: {signal_names}"
        super().__init__(error_message)


def detect_browser_signals(html: str, *, url: str | None = None, title: str | None = None) -> list[BrowserBlockSignal]:
    """Detect common CAPTCHA, block, consent, and login states from browser HTML."""
    haystack = "\n".join(part for part in [url or "", title or "", html] if part)
    signals: list[BrowserBlockSignal] = []
    seen: set[tuple[BrowserSignalKind, str]] = set()
    for kind, pattern in _BROWSER_SIGNAL_PATTERNS:
        match = pattern.search(haystack)
        if not match:
            continue
        key = (kind, pattern.pattern)
        if key in seen:
            continue
        seen.add(key)
        signals.append(
            BrowserBlockSignal(
                kind=kind,
                pattern=pattern.pattern,
                excerpt=_excerpt(haystack, match.start(), match.end()),
            ),
        )
    return signals


def build_browser_evidence(
    *,
    engine: str,
    query: str,
    html: str,
    url: str | None = None,
    title: str | None = None,
) -> BrowserEvidence:
    """Build browser diagnostics from captured page state without writing files."""
    return BrowserEvidence(
        engine=engine,
        query=query,
        url=url,
        title=title,
        signals=detect_browser_signals(html, url=url, title=title),
    )


def write_browser_failure_evidence(
    *,
    engine: str,
    query: str,
    html: str,
    config: BrowserConfig,
    url: str | None = None,
    title: str | None = None,
    screenshot: bytes | None = None,
    output_dir: Path | str = ".twat-search/browser-evidence",
) -> BrowserEvidence:
    """Write configured browser failure artifacts and return diagnostics."""
    evidence = build_browser_evidence(engine=engine, query=query, html=html, url=url, title=title)
    artifact_dir = Path(output_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    stem = _artifact_stem(engine, query)

    html_path: Path | None = None
    screenshot_path: Path | None = None
    if config.save_html_on_failure:
        html_path = artifact_dir / f"{stem}.html"
        html_path.write_text(html, encoding="utf-8")
    if config.screenshots_on_failure and screenshot is not None:
        screenshot_path = artifact_dir / f"{stem}.png"
        screenshot_path.write_bytes(screenshot)

    return BrowserEvidence(
        engine=evidence.engine,
        query=evidence.query,
        url=evidence.url,
        title=evidence.title,
        html_path=html_path,
        screenshot_path=screenshot_path,
        signals=evidence.signals,
    )


def _artifact_stem(engine: str, query: str) -> str:
    """Build a short filesystem-safe artifact stem."""
    raw = f"{engine}-{query}".lower()
    stem = re.sub(r"[^a-z0-9._-]+", "-", raw).strip("-._")
    return stem[:96] or "browser-evidence"


def _excerpt(text: str, start: int, end: int, radius: int = 48) -> str:
    """Return a compact excerpt around a matched browser signal."""
    prefix = max(0, start - radius)
    suffix = min(len(text), end + radius)
    return re.sub(r"\s+", " ", text[prefix:suffix]).strip()
