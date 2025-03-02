# Falla-Qwant
# Sanix-darker

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from twat_search.web.engines.lib_falla.core.falla import Falla


class Qwant(Falla):
    def __init__(self):
        self.option = Options()
        self.option.headless = True
        self.driver = webdriver.Firefox(options=self.option)

        self.try_it = 0
        self.max_retry = 3
        self.source = "Qwant"
        self.mode = "selenium"
        self.results_box = "//div[@class='result_fragment']"
        self.each_element = {"tag": "div", "attr": {"class": "result--web"}}
        self.href = {"tag": "a:result--web--link", "type": "attribute", "key": "href", "child": {}}
        self.title = {"tag": "span:result--web--title", "type": "text", "child": {}}
        self.cite = {"tag": "div:result--web", "child": {"tag": "p", "type": "text"}}

    def search(self, search_text, pages=""):
        url = "https://www.qwant.com/?q=" + search_text.replace(" ", "+") + pages

        return self.fetch(url)


# qw = Qwant()
# print(qw.search("un avion"))
