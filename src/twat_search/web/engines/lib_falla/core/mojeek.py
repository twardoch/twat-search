# Falla-Mojeek
# Sanix-darker

from twat_search.web.engines.lib_falla.core.falla import Falla


class Mojeek(Falla):
    def __init__(self):
        self.try_it = 0
        self.max_retry = 3
        self.source = "Mojeek"
        self.mode = "requests"
        self.results_box = "//ul[@class='results-standard']"
        self.each_element = {"tag": "li"}
        self.href = {"tag": "a:ob", "type": "attribute", "key": "href", "child": {}}
        self.title = {"tag": "a:ob", "type": "text"}
        self.cite = {"tag": "p:s", "type": "text"}

    def search(self, search_text, pages=""):
        url = "https://www.mojeek.com/search?q=" + search_text.replace(" ", "+") + pages

        return self.fetch(url)


# mk = Mojeek()
# print(mk.search("un avion"))
