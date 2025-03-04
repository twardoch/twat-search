# Falla-Yahoo
# Sanix-darker

import logging
import urllib.parse

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla

logger = logging.getLogger(__name__)


class Yahoo(Falla):
    """Yahoo search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Yahoo search engine."""
        super().__init__(name="Yahoo")
        self.use_method = "playwright"
        # Yahoo search results have different selectors
        self.container_element = ("div", {"class": "dd algo algo-sr"})
        self.wait_for_selector = "#results"
        # Increase timeout for Yahoo which can be slow to load
        self.max_retries = 5

        # Yahoo often shows a consent page first
        # We'll need to handle that using a separate method

    def get_url(self, query: str) -> str:
        """
        Get the search URL for a query.

        Args:
            query: Search query

        Returns:
            URL string
        """
        params = {
            "p": query,
        }
        query_string = urllib.parse.urlencode(params)
        return f"https://search.yahoo.com/search?{query_string}"

    def get_title(self, elm: Tag) -> str:
        """
        Extract the title from a search result element.

        Args:
            elm: BeautifulSoup element

        Returns:
            Title string
        """
        title_elem = elm.select_one("h3.title")
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
        link_elem = elm.select_one("a.d-ib")
        if link_elem and "href" in link_elem.attrs:
            return str(link_elem.attrs["href"])
        return ""

    def get_snippet(self, elm: Tag) -> str:
        """
        Extract the snippet from a search result element.

        Args:
            elm: BeautifulSoup element

        Returns:
            Snippet text string
        """
        snippet_elem = elm.select_one("div.compText.aAbs")
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


# y = Yahoo()
# print(y.search("un avion"))
