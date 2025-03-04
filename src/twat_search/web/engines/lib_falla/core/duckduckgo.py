# Falla-DuckDuckGo
# Sanix-darker

import logging
import urllib.parse

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla

logger = logging.getLogger(__name__)


class DuckDuckGo(Falla):
    """DuckDuckGo search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the DuckDuckGo search engine."""
        super().__init__(name="DuckDuckGo")
        self.use_method = "playwright"
        # Use the HTML version of DuckDuckGo which is more reliable for scraping
        self.container_element = ("div", {"class": "result"})
        self.wait_for_selector = "body"
        # Increase timeout for DuckDuckGo which can be slow to load
        self.max_retries = 5

    def get_url(self, query: str) -> str:
        """
        Get the search URL for a query.

        Args:
            query: Search query

        Returns:
            URL string
        """
        # Use the HTML version of DuckDuckGo which is more reliable for scraping
        base_url = "https://html.duckduckgo.com/html/"
        params = {
            "q": query,
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
        # HTML version of DuckDuckGo uses this class for titles
        title_elem = elm.select_one(".result__title")
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
        # HTML version of DuckDuckGo uses this class for links
        link_elem = elm.select_one(".result__a")
        if link_elem and "href" in link_elem.attrs:
            href = str(link_elem.attrs["href"])
            # The HTML version of DuckDuckGo uses relative URLs
            if href.startswith("/"):
                return f"https://duckduckgo.com{href}"
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
        # HTML version of DuckDuckGo uses this class for snippets
        snippet_elem = elm.select_one(".result__snippet")
        if snippet_elem:
            return snippet_elem.get_text().strip()
        return ""

    def get_each_elements(self, elements: list) -> list[dict[str, str]]:
        """
        Custom implementation to filter out elements that don't have valid links.

        Args:
            elements: List of BeautifulSoup elements

        Returns:
            List of dictionaries containing search results
        """
        elements_list: list[dict[str, str]] = []

        for elm in elements:
            try:
                # Only process if it has a valid link
                link = self.get_link(elm)
                if link:
                    title = self.get_title(elm) or ""
                    snippet = self.get_snippet(elm) or ""

                    elements_list.append(
                        {
                            "title": title,
                            "link": link,
                            "snippet": snippet,
                        },
                    )
            except Exception as e:
                logger.debug(f"Error processing element: {e}")
                continue

        return elements_list


# d = DuckDuckGo()
# print(d.search("un avion"))
