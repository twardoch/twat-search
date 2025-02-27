# this_file: src/twat_search/web/engines/lib_falla/core/google.py
"""
Google search engine implementation for the Falla search engine scraper.

This module provides the Google search engine implementation for the Falla search engine.
"""

import urllib.parse

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla


class Google(Falla):
    """Google search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Google search engine."""
        super().__init__(name="Google")
        self.use_method = "requests"
        self.container_element = ("div", {"class": "g"})

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

    def get_title(self, elm: Tag, is_test: bool = False) -> str:
        """
        Extract the title from a search result element.

        Args:
            elm: BeautifulSoup element
            is_test: Whether this is a test run

        Returns:
            Title string
        """
        title_elem = elm.find("h3")
        if title_elem:
            return title_elem.get_text().strip()
        return ""

    def get_link(self, elm: Tag, is_test: bool = False) -> str:
        """
        Extract the link from a search result element.

        Args:
            elm: BeautifulSoup element
            is_test: Whether this is a test run

        Returns:
            Link URL string
        """
        link_elem = elm.find("a")
        if link_elem and link_elem.has_attr("href"):
            href = link_elem["href"]
            # Google prepends URLs with "/url?q=" and adds tracking parameters
            if href.startswith("/url?"):
                href = href.split("&")[0].replace("/url?q=", "")
                return urllib.parse.unquote(href)
            return href
        return ""

    def get_snippet(self, elm: Tag, is_test: bool = False) -> str:
        """
        Extract the snippet from a search result element.

        Args:
            elm: BeautifulSoup element
            is_test: Whether this is a test run

        Returns:
            Snippet text string
        """
        snippet_elem = elm.find("div", {"class": "VwiC3b"})
        if snippet_elem:
            return snippet_elem.get_text().strip()
        return ""

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

        return self.fetch(url)


# g = Google()
# print(g.search("un avion"))
