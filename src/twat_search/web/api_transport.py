# this_file: src/twat_search/web/api_transport.py
"""HTTPX transport execution for API-backed search providers."""

from __future__ import annotations

import asyncio
import logging
import random
from typing import Any

import httpx

from twat_search.web.exceptions import EngineError

logger = logging.getLogger(__name__)

# List of user agents to rotate for scrapers and unofficial API endpoints.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
]


async def execute_api_request(
    *,
    engine_code: str,
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_data: Any = None,
    timeout: float = 10.0,
    retries: int = 2,
    retry_delay: float = 1.0,
    min_delay: float = 0.0,
    use_random_user_agent: bool = True,
    proxy_url: str | None = None,
) -> httpx.Response:
    """Execute an HTTPX request using shared timeout, retry, delay, and proxy policy."""
    request_headers = dict(headers or {})
    if use_random_user_agent and "user-agent" not in {key.lower() for key in request_headers}:
        request_headers["User-Agent"] = random.choice(USER_AGENTS)

    delay = retry_delay
    last_error: httpx.RequestError | httpx.HTTPStatusError | None = None

    for attempt in range(1, retries + 2):
        try:
            if min_delay > 0:
                await asyncio.sleep(min_delay + random.uniform(0, min_delay * 0.1))

            client_kwargs: dict[str, Any] = {"timeout": timeout}
            if proxy_url:
                client_kwargs["proxy"] = proxy_url

            async with httpx.AsyncClient(**client_kwargs) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    params=params,
                    json=json_data,
                )
                response.raise_for_status()
                return response
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            last_error = exc
            if attempt > retries:
                break

            actual_delay = delay * random.uniform(0.5, 1.5)
            logger.warning(
                "Request failed (attempt %s/%s), retrying in %.2fs: %s",
                attempt,
                retries + 1,
                actual_delay,
                exc,
            )

            await asyncio.sleep(actual_delay)
            delay *= 2

    if last_error is None:
        last_error = httpx.RequestError("Unknown error occurred during HTTP request")

    msg = f"HTTP request failed after {retries + 1} attempts: {last_error}"
    raise EngineError(engine_code, msg) from last_error
