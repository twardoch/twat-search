#!/usr/bin/env python3
# this_file: tests/test_falla.py
import asyncio
import contextlib

import pytest

pytest.importorskip("playwright.async_api", reason="Falla browser tests require optional Playwright")
from twat_search.web.engines.lib_falla.core.duckduckgo import DuckDuckGo


async def test():
    d = DuckDuckGo()
    try:
        await d._initialize_browser()
        return await d._fetch_page("https://duckduckgo.com/?q=FontLab")
    finally:
        await d._close_browser()


if __name__ == "__main__":
    with contextlib.suppress(Exception):
        result = asyncio.run(test())
