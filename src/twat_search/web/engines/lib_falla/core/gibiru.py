# this_file: src/twat_search/web/engines/lib_falla/core/gibiru.py
# Falla-Gibiru
# Sanix-darker

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla


class Gibiru(Falla):
    """Gibiru (Google CSE-backed) search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Gibiru search engine."""
        super().__init__(name="Gibiru")
        self.use_method = "requests"
        self.container_element = ("div", {"class": "gs-webResult"})

    def get_url(self, query: str) -> str:
        return "https://gibiru.com/results.html?q=" + query.replace(" ", "+")

    def get_title(self, elm: Tag) -> str:
        a = elm.find("a", class_="gs-title")
        return a.get_text().strip() if isinstance(a, Tag) else ""

    def get_link(self, elm: Tag) -> str:
        a = elm.find("a", class_="gs-title")
        if isinstance(a, Tag):
            href = a.attrs.get("data-ctorig") or a.attrs.get("href")
            if href:
                return str(href)
        return ""

    def get_snippet(self, elm: Tag) -> str:
        d = elm.find("div", class_="gs-snippet")
        return d.get_text().strip() if isinstance(d, Tag) else ""
