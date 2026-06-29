# this_file: src/twat_search/web/engines/lib_falla/core/aol.py
# Falla-Aol
# Sanix-darker

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla


class Aol(Falla):
    """AOL (Yahoo-backed) search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the AOL search engine."""
        super().__init__(name="Aol")
        self.use_method = "requests"
        self.container_element = ("div", {"class": "algo"})

    def get_url(self, query: str) -> str:
        return "https://search.aol.com/aol/search?q=" + query.replace(" ", "+")

    def get_title(self, elm: Tag) -> str:
        h = elm.find(["h3", "h2"])
        return h.get_text().strip() if isinstance(h, Tag) else ""

    def get_link(self, elm: Tag) -> str:
        a = elm.find("a", href=True)
        return str(a.attrs["href"]) if isinstance(a, Tag) else ""

    def get_snippet(self, elm: Tag) -> str:
        p = elm.find("p")
        return p.get_text().strip() if isinstance(p, Tag) else ""
