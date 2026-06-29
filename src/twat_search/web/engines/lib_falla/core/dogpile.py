# this_file: src/twat_search/web/engines/lib_falla/core/dogpile.py
# Falla-DogPile
# Sanix-darker

from bs4.element import Tag

from twat_search.web.engines.lib_falla.core.falla import Falla


class DogPile(Falla):
    """Dogpile search engine implementation for Falla."""

    def __init__(self) -> None:
        """Initialize the Dogpile search engine."""
        super().__init__(name="DogPile")
        self.use_method = "requests"
        self.container_element = ("div", {"class": "web-bing__result"})

    def get_url(self, query: str) -> str:
        return "https://www.dogpile.com/serp?q=" + query.replace(" ", "+")

    def get_title(self, elm: Tag) -> str:
        a = elm.find("a", class_="web-bing__title")
        if not isinstance(a, Tag):
            a = elm.find(["h2", "h3"])
        return a.get_text().strip() if isinstance(a, Tag) else ""

    def get_link(self, elm: Tag) -> str:
        a = elm.find("a", class_="web-bing__title")
        if not isinstance(a, Tag):
            a = elm.find("a", href=True)
        return str(a.attrs["href"]) if isinstance(a, Tag) and a.has_attr("href") else ""

    def get_snippet(self, elm: Tag) -> str:
        s = elm.find("span", class_="web-bing__description")
        if not isinstance(s, Tag):
            s = elm.find("p")
        return s.get_text().strip() if isinstance(s, Tag) else ""
