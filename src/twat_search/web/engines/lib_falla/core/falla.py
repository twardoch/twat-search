# this_file: src/twat_search/web/engines/lib_falla/core/falla.py
"""
Base Falla class for search engine scraping.

This module provides the base class for all Falla search engine scrapers.
"""

import time

import bs4
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from twat_search.web.engines.lib_falla.settings import SPLASH_SCRAP_URL


class Falla:
    """
    Base class for all Falla search engine implementations.

    This class provides common functionality for web scraping search engines,
    including methods for making requests, parsing HTML, and extracting results.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a new Falla search engine instance.

        Args:
            name: The name of the search engine
        """
        self.name = name
        self.results: list[dict[str, str]] = []

    def get_element_from_type(
        self,
        bs_obj: BeautifulSoup,
        type_elem: str,
        attr_elem: dict[str, str],
    ) -> bs4.element.Tag | None:
        """
        Get a BeautifulSoup element by type and attributes.

        Args:
            bs_obj: BeautifulSoup object
            type_elem: HTML element type (e.g., 'div', 'a')
            attr_elem: Dictionary of attributes to match

        Returns:
            BeautifulSoup element or None if not found
        """
        try:
            return bs_obj.find(type_elem, attr_elem)
        except Exception:
            return None

    def get_tag(
        self,
        element: bs4.element.Tag,
        _type: str = "div",
        _attr: dict[str, str] | None = None,
    ) -> bs4.element.Tag | None:
        """
        Get a tag from within an element.

        Args:
            element: Parent BeautifulSoup element
            _type: Type of tag to find
            _attr: Attributes to match

        Returns:
            BeautifulSoup element or None if not found
        """
        if _attr is None:
            _attr = {}
        try:
            return element.find(_type, _attr)
        except Exception:
            return None

    def parse_entry_point(self, entry_point: str, use_splash: bool = False) -> BeautifulSoup | None:
        """
        Parse the entry point URL and return a BeautifulSoup object.

        Args:
            entry_point: URL to parse
            use_splash: Whether to use Splash for rendering JavaScript

        Returns:
            BeautifulSoup object or None if parsing fails
        """
        try:
            if use_splash:
                return BeautifulSoup(self.scrapy_splash_request(entry_point), "html.parser")
            return BeautifulSoup(self.get_html_content(entry_point), "html.parser")
        except Exception:
            return None

    def get_each_elements(self, elements: bs4.element.ResultSet, is_test: bool = False) -> list[dict[str, str]]:
        """
        Extract search results from a list of elements.

        Args:
            elements: List of BeautifulSoup elements
            is_test: Whether this is a test run

        Returns:
            List of dictionaries containing search results
        """
        elements_list = []

        if is_test:
            pass

        for elm in elements[:10]:
            elements_list.append(
                {
                    "title": self.get_title(elm, is_test=is_test),
                    "link": self.get_link(elm, is_test=is_test),
                    "snippet": self.get_snippet(elm, is_test=is_test),
                },
            )

        return elements_list

    def scrapy_splash_request(self, entry_point: str) -> str:
        """
        Use Splash to render JavaScript before scraping.

        Args:
            entry_point: URL to scrape

        Returns:
            HTML content as string
        """
        try:
            splash_url = f"{SPLASH_SCRAP_URL}/render.html?url={entry_point}&timeout=10&wait=0.5"
            return requests.get(splash_url, timeout=30).text
        except Exception:
            return ""

    def get_html_content(self, url: str) -> str:
        """
        Get HTML content from a URL.

        Args:
            url: URL to fetch

        Returns:
            HTML content as string
        """
        try:
            if "selenium" in self.use_method:
                options = Options()
                options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)
                driver.get(url)
                # Wait for JavaScript to load
                time.sleep(2)
                content = driver.page_source
                driver.quit()
                return content
            # Standard HTTP request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            }
            return requests.get(url, headers=headers, timeout=15).text
        except Exception:
            return ""

    def fetch(self, entry_point: str, use_splash: bool = False) -> list[dict[str, str]]:
        """
        Fetch and parse search results from an entry point URL.

        Args:
            entry_point: URL to fetch
            use_splash: Whether to use Splash for JavaScript rendering

        Returns:
            List of dictionaries containing search results
        """
        try:
            html_parser = self.parse_entry_point(entry_point, use_splash)
            if html_parser:
                elements = html_parser.find_all(self.container_element[0], self.container_element[1])
                return self.get_each_elements(elements)
            return []
        except Exception:
            return []

    def get_url(self, query: str) -> str:
        """
        Get the search URL for a query.

        Args:
            query: Search query

        Returns:
            URL string
        """
        msg = "Subclasses must implement get_url"
        raise NotImplementedError(msg)

    def get_title(self, elm: bs4.element.Tag, is_test: bool = False) -> str:
        """
        Extract the title from a search result element.

        Args:
            elm: BeautifulSoup element
            is_test: Whether this is a test run

        Returns:
            Title string
        """
        msg = "Subclasses must implement get_title"
        raise NotImplementedError(msg)

    def get_link(self, elm: bs4.element.Tag, is_test: bool = False) -> str:
        """
        Extract the link from a search result element.

        Args:
            elm: BeautifulSoup element
            is_test: Whether this is a test run

        Returns:
            Link URL string
        """
        msg = "Subclasses must implement get_link"
        raise NotImplementedError(msg)

    def get_snippet(self, elm: bs4.element.Tag, is_test: bool = False) -> str:
        """
        Extract the snippet from a search result element.

        Args:
            elm: BeautifulSoup element
            is_test: Whether this is a test run

        Returns:
            Snippet text string
        """
        msg = "Subclasses must implement get_snippet"
        raise NotImplementedError(msg)

    def search(self, query: str, pages: str = "") -> list[dict[str, str]]:
        """
        Search for a query and return results.

        Args:
            query: Search query
            pages: Optional pagination parameter

        Returns:
            List of dictionaries containing search results
        """
        msg = "Subclasses must implement search"
        raise NotImplementedError(msg)
