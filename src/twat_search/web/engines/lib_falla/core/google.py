# this_file: src/twat_search/web/engines/lib_falla/core/google.py
"""
Google search engine implementation for the Falla search engine scraper.

This module provides the Google search engine implementation for the Falla search engine.
"""

import logging
import urllib.parse
from pathlib import Path
from typing import cast

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla

# Set up logger
logger = logging.getLogger(__name__)


class Google(Falla):
    """Google search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Google search engine."""
        super().__init__(name="Google")
        self.use_method = "playwright"
        # Use the more reliable and general container selector from falla_search.py
        self.container_element = ("div", {"class": "g"})
        # Selector to wait for to indicate results have loaded
        self.wait_for_selector = "body"
        # Increase retries and timeout for Google
        self.max_retries = 5

    def get_url(self, query: str) -> str:
        """
        Get the search URL for a query.

        Args:
            query: Search query

        Returns:
            URL string
        """
        base_url = "https://www.google.com/search"
        params = {
            "q": query,
            "num": "100",
            "hl": "en",
            "gl": "us",
        }
        query_string = urllib.parse.urlencode(params)
        return f"{base_url}?{query_string}"

    def get_title(self, elm: Tag) -> str:
        """
        Extract the title from a search result element.

        Args:
            elm: BeautifulSoup element

        Returns:
            Title string
        """
        title_elem = elm.find("h3")
        if title_elem:
            return title_elem.get_text().strip()
        return ""

    def get_link(self, elm: Tag) -> str:
        """
        Extract the link from a search result element.

        Args:
            elm: BeautifulSoup element

        Returns:
            Link URL string
        """
        link_elem = elm.find("a")
        if link_elem and isinstance(link_elem, Tag) and "href" in link_elem.attrs:
            href = cast(str, link_elem.attrs["href"])
            # Google prepends URLs with "/url?q=" and adds tracking parameters
            if href.startswith("/url?"):
                href = href.split("&")[0].replace("/url?q=", "")
                return urllib.parse.unquote(href)
            return href
        return ""

    def get_snippet(self, elm: Tag) -> str:
        """
        Extract the snippet from a search result element.

        Args:
            elm: BeautifulSoup element

        Returns:
            Snippet text string
        """
        # Try various snippet element selectors that Google might use
        snippet_elem = elm.find("div", {"class": "VwiC3b"})
        if not snippet_elem:
            snippet_elem = elm.find("span", {"class": "aCOpRe"})
        if not snippet_elem:
            snippet_elem = elm.find("div", {"class": "BNeawe s3v9rd AP7Wnd"})
        if not snippet_elem:
            # Try to find any text container that might hold a snippet
            text_containers = elm.find_all(["div", "span", "p"], class_=True)
            for container in text_containers:
                if (
                    isinstance(container, Tag)
                    and container.get_text().strip()
                    and hasattr(container, "name")
                    and container.name != "h3"
                ):
                    snippet_elem = container
                    break

        if snippet_elem and isinstance(snippet_elem, Tag):
            return snippet_elem.get_text().strip()
        return ""

    async def search_async(self, query: str, pages: str = "") -> list[dict[str, str]]:
        """
        Search for a query and return results asynchronously.
        Override to add debugging.

        Args:
            query: Search query
            pages: Optional pagination parameter

        Returns:
            List of dictionaries containing search results
        """
        try:
            url = self.get_url(query)
            if pages:
                url += f"&{pages}"

            logger.info(f"Starting Google search for: {query}")
            logger.info(f"URL: {url}")

            # Get the raw HTML content
            await self._initialize_browser()
            if not self.browser_context:
                logger.error("Browser context not initialized")
                return []

            page = await self.browser_context.new_page()

            try:
                # Set timeout for navigation to prevent hanging
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")

                logger.info("Page loaded, waiting for selector...")
                # Wait for selector
                try:
                    await page.wait_for_selector(self.wait_for_selector, timeout=10000)
                    logger.info(f"Selector '{self.wait_for_selector}' found")
                except Exception as e:
                    logger.warning(f"Timeout waiting for selector: {e}")

                # Get the page content
                html_content = await page.content()
                logger.info(f"Retrieved HTML content, length: {len(html_content)}")

                # Save to file
                debug_file = f"google_debug_{query.replace(' ', '_')}.html"
                with open(debug_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                logger.info(f"Wrote HTML content to {Path(debug_file).resolve()}")

                # Look for specific elements to debug selector issues
                result_count = await page.evaluate("""() => {
                    const results = document.querySelectorAll('div.g');
                    return results.length;
                }""")
                logger.info(f"JavaScript found {result_count} results with 'div.g' selector")

                # Try alternate selectors
                alt_selectors = [
                    "div.Gx5Zad",
                    "div.tF2Cxc",
                    "div[jscontroller='SC7lYd']",
                    "div.yuRUbf",
                    "div.eKjLze",
                    "h3",
                    "a[href]",
                ]

                for selector in alt_selectors:
                    try:
                        count = await page.evaluate(f"""() => {{
                            const elements = document.querySelectorAll('{selector}');
                            return elements.length;
                        }}""")
                        logger.info(f"Found {count} elements with selector: {selector}")
                    except Exception as e:
                        logger.error(f"Error evaluating selector {selector}: {e}")
            finally:
                await page.close()

            # Continue with the normal search process
            results = await self.fetch_async(url)
            logger.info(f"Got {len(results)} results from fetch_async")

            if not results:
                logger.warning("No results found with standard method, trying alternate parsing")

                # Parse the saved HTML file
                from bs4 import BeautifulSoup

                if Path(debug_file).exists():
                    with open(debug_file, encoding="utf-8") as f:
                        html_content = f.read()

                    soup = BeautifulSoup(html_content, "html.parser")

                    # Try various selectors
                    alt_container_selectors = [
                        ("div", {"class": "g"}),
                        ("div", {"class": "Gx5Zad"}),
                        ("div", {"class": "tF2Cxc"}),
                        ("div", {"jscontroller": "SC7lYd"}),
                        ("div", {"class": "yuRUbf"}),
                        ("div", {"class": "eKjLze"}),
                    ]

                    for selector_type, selector_attrs in alt_container_selectors:
                        logger.info(f"Trying alternate selector: {selector_type}.{selector_attrs}")
                        elements = soup.find_all(selector_type, attrs=selector_attrs)
                        logger.info(f"Found {len(elements)} elements")

                        if elements:
                            self.container_element = (selector_type, selector_attrs)
                            logger.info(f"Using alternate container: {self.container_element}")
                            # Try to extract results with this selector
                            manual_results = []
                            for elem in elements[:10]:
                                title = self.get_title(elem) or ""
                                link = self.get_link(elem) or ""
                                snippet = self.get_snippet(elem) or ""

                                if title or link:  # Only add if we have at least a title or link
                                    logger.info(f"Found result: {title} - {link}")
                                    manual_results.append(
                                        {
                                            "title": title,
                                            "link": link,
                                            "snippet": snippet,
                                        },
                                    )

                            if manual_results:
                                logger.info(f"Returning {len(manual_results)} manually parsed results")
                                return manual_results

            return results
        finally:
            # Clean up resources
            await self._close_browser()

    def search(self, query: str, pages: str = "") -> list[dict[str, str]]:
        """
        Search for a query and return results.

        Args:
            query: Search query
            pages: Optional pagination parameter

        Returns:
            List of dictionaries containing search results
        """
        url = self.get_url(query)
        if pages:
            url += f"&{pages}"

        # Debug: Get raw HTML content and log key information
        html_parser = self.parse_entry_point(url)
        if html_parser:
            # Log the HTML structure for debugging
            html_content = str(html_parser)
            logger.debug(f"Google search HTML content length: {len(html_content)}")
            logger.debug(f"HTML Preview: {html_content[:500]}...")

            # Debug: Try different selectors and log what we find
            logger.debug("Testing various selectors:")

            # Try the standard container selector
            elements = html_parser.find_all(self.container_element[0], attrs=self.container_element[1])
            logger.debug(f"Found {len(elements)} results with selector: div.g")

            # Try alternative selectors
            alt_selectors = [
                ("div", {"class": "Gx5Zad"}),
                ("div", {"class": "tF2Cxc"}),
                ("div", {"jscontroller": "SC7lYd"}),
                ("div", {"class": "yuRUbf"}),
                ("div", {"class": "g"}),
                ("div", {"class": "eKjLze"}),
            ]

            for selector_type, selector_attrs in alt_selectors:
                alt_elements = html_parser.find_all(selector_type, attrs=selector_attrs)
                attr_str = ", ".join([f"{k}={v}" for k, v in selector_attrs.items()])
                logger.debug(f"Found {len(alt_elements)} results with selector: {selector_type}[{attr_str}]")

                # If we found elements, check for titles and links
                if alt_elements:
                    for i, elem in enumerate(alt_elements[:3]):
                        h3 = elem.find("h3")
                        a = elem.find("a", href=True)
                        logger.debug(f"Element {i}: h3={h3 is not None}, a={a is not None}")

            # Create a debug file with the full HTML
            try:
                debug_file = f"google_debug_{query.replace(' ', '_')}_sync.html"
                with open(debug_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                logger.info(f"Saved Google HTML content to: {debug_file}")
            except Exception as e:
                logger.error(f"Failed to save debug HTML: {e}")

        # Continue with normal search process
        return self.fetch(url)


# g = Google()
# print(g.search("un avion"))
