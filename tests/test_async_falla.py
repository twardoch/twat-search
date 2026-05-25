#!/usr/bin/env python3
# this_file: tests/test_async_falla.py
import asyncio

import pytest

pytest.importorskip("playwright.async_api", reason="Falla browser tests require optional Playwright")
from twat_search.web.engines.lib_falla.core.duckduckgo import DuckDuckGo


async def test_async():
    d = DuckDuckGo()
    try:
        return await d.search_async("FontLab")
    except Exception:
        return None


if __name__ == "__main__":
    asyncio.run(test_async())
