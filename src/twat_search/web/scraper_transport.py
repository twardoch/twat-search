# this_file: src/twat_search/web/scraper_transport.py
"""Synchronous scraper transport helpers for bundled HTML adapters."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from twat_search.web.config import ProxyConfig

logger = logging.getLogger(__name__)

DEFAULT_SCRAPER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)


def fetch_scraper_html(
    url: str,
    *,
    proxy_config: ProxyConfig,
    user_agent: str = DEFAULT_SCRAPER_USER_AGENT,
    default_timeout: float = 15,
) -> str:
    """Fetch HTML with the shared proxy timeout, retry, and requests proxy policy."""
    headers = {"User-Agent": user_agent}
    proxy_url = proxy_config.httpx_proxy_url()
    timeout = proxy_config.timeout if proxy_config.enabled else default_timeout
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    max_attempts = max(1, proxy_config.retries + 1) if proxy_config.enabled else 1

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
            response.raise_for_status()
            return response.text
        except Exception as exc:
            if attempt >= max_attempts:
                logger.error("Error getting HTML content: %s", exc)
                return ""
            time.sleep(proxy_config.retry_delay)
    return ""
