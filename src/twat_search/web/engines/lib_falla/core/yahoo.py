# Falla-Yahoo
# Sanix-darker

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from twat_search.web.engines.lib_falla.core.falla import Falla


class Yahoo(Falla):
    def __init__(self):
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox(options=self.option)

        self.try_it = 0
        self.max_retry = 3
        self.source = "Yahoo"
        self.mode = "selenium"
        self.results_box = "//div[@id='web']"
        self.each_element = {"tag": "li"}
        self.href = {"tag": "a", "type": "attribute", "key": "href", "child": {}}
        self.title = {"tag": "a", "type": "text"}
        self.cite = {"tag": "div:compText", "child": {"tag": "p", "type": "text"}}

    def search(self, search_text, pages=""):
        url = "https://search.yahoo.com/search?p=" + search_text.replace(" ", "+") + pages

        return self.fetch(url)


# y = Yahoo()
# print(y.search("un avion"))
