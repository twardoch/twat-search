# Falla-Qwant
# Sanix-darker

import logging
import urllib.parse

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla

logger = logging.getLogger(__name__)


class Qwant(Falla):
    """Qwant search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Qwant search engine."""
        super().__init__(name="Qwant")
        self.use_method = "playwright"
        self.container_element = ("article", {"class": "webResult"})
        self.wait_for_selector = ".webResults"
        # Increase timeout for Qwant which can be slow to load
        self.max_retries = 5

        # Qwant may show a consent dialog or have different layouts
        # We'll need to handle that with flexible selectors

    def get_url(self, query: str) -> str:
        """
        Get the search URL for a query.

        Args:
            query: Search query

        Returns:
            URL string
        """
        params = {
            "q": query,
        }
        query_string = urllib.parse.urlencode(params)
        return f"https://www.qwant.com/?{query_string}"

    def get_title(self, elm: Tag) -> str:
        """
        Extract the title from a search result element.

        Args:
            elm: BeautifulSoup element

        Returns:
            Title string
        """
        title_elem = elm.select_one(".title")
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
        link_elem = elm.select_one(".title")
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
        snippet_elem = elm.select_one(".description")
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


# qw = Qwant()
# print(qw.search("un avion"))
