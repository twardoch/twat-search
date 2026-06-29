# this_file: src/twat_search/web/engines/lib_falla/core/mojeek.py
# Falla-Mojeek
# Sanix-darker

import logging

from bs4.element import ResultSet, Tag

from twat_search.web.engines.lib_falla.core.falla import Falla

logger = logging.getLogger(__name__)


class Mojeek(Falla):
    """Mojeek search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Mojeek search engine."""
        super().__init__(name="Mojeek")
        self.use_method = "requests"
        # Result list; individual results are <li> children parsed below.
        self.container_element = ("ul", {"class": "results-standard"})

    def get_url(self, query: str) -> str:
        return "https://www.mojeek.com/search?q=" + query.replace(" ", "+")

    def get_title(self, elm: Tag) -> str:
        a = elm.find("a", class_="title")
        return a.get_text().strip() if isinstance(a, Tag) else ""

    def get_link(self, elm: Tag) -> str:
        a = elm.find("a", class_="title")
        if isinstance(a, Tag) and "href" in a.attrs:
            return str(a.attrs["href"])
        return ""

    def get_snippet(self, elm: Tag) -> str:
        p = elm.find("p", class_="s")
        return p.get_text().strip() if isinstance(p, Tag) else ""

    def get_each_elements(self, elements: ResultSet) -> list[dict[str, str]]:
        """Expand the results list into its individual <li> result rows."""
        results: list[dict[str, str]] = []
        for container in elements:
            if not isinstance(container, Tag):
                continue
            for li in container.find_all("li"):
                if not isinstance(li, Tag):
                    continue
                try:
                    link = self.get_link(li)
                    if not link:
                        continue
                    results.append(
                        {
                            "title": self.get_title(li),
                            "link": link,
                            "snippet": self.get_snippet(li),
                        },
                    )
                except Exception as e:
                    logger.debug(f"Error processing Mojeek element: {e}")
        return results
