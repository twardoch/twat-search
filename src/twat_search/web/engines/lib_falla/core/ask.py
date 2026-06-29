# this_file: src/twat_search/web/engines/lib_falla/core/ask.py
# Falla-Ask
# Sanix-darker

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla


class Ask(Falla):
    """Ask.com search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Ask.com search engine."""
        super().__init__(name="Ask")
        self.use_method = "requests"
        self.container_element = ("div", {"class": "PartialSearchResults-item"})

    def get_url(self, query: str) -> str:
        return "https://www.ask.com/web?q=" + query.replace(" ", "+")

    def get_title(self, elm: Tag) -> str:
        a = elm.find("a", class_="PartialSearchResults-item-title-link")
        if not isinstance(a, Tag):
            a = elm.find(["h2", "h3"])
        return a.get_text().strip() if isinstance(a, Tag) else ""

    def get_link(self, elm: Tag) -> str:
        a = elm.find("a", class_="PartialSearchResults-item-title-link")
        if not isinstance(a, Tag):
            a = elm.find("a", href=True)
        return str(a.attrs["href"]) if isinstance(a, Tag) and a.has_attr("href") else ""

    def get_snippet(self, elm: Tag) -> str:
        p = elm.find("p", class_="PartialSearchResults-item-abstract")
        if not isinstance(p, Tag):
            p = elm.find("p")
        return p.get_text().strip() if isinstance(p, Tag) else ""
