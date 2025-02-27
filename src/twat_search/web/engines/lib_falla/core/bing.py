# Falla-Bing
# Sanix-darker


from twat_search.web.engines.lib_falla.core.falla import Falla


class Bing(Falla):
    def __init__(self):
        self.source = "Bing"
        self.mode = "splash_scrap"
        self.try_it = 0
        self.max_retry = 3
        self.results_box = "//ol[@id='b_results']"
        self.each_element = {"tag": "li", "attr": {"class": "b_algo"}}
        self.href = {"tag": "a", "type": "attribute", "key": "href", "child": {}}
        self.title = {"tag": "h2", "type": "text", "child": {}}
        self.cite = {"tag": "div:b_caption", "child": {"tag": "p", "type": "text"}}

    def search(self, search_text, pages=""):
        url = "https://www.bing.com/search?q=" + search_text.replace(" ", "+") + pages

        return self.fetch(url)


# b = Bing()
# print(b.search("un avion"))
