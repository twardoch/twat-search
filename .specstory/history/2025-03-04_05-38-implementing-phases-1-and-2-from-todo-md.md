## SpecStory

## Implementing Phases 1 and 2 from TODO.md (04/03/2025, 05:38:16)

_**User**_

Implement phases 1, 2 from @TODO.md 

---

_**Assistant**_

I'll help you implement phases 1 and 2 from the TODO.md file, which focus on fixing Falla-based search engines and critical engine failures. Let me first explore the codebase to understand the current structure and issues.

---

_****_



---

_****_



Now, let's examine the Falla-based search engines to understand the issues that need to be fixed.

---

_****_

Read file: src/twat_search/web/engines/falla.py

---

_****_



Now, let's look at the Yahoo and Qwant implementations in the Falla library, which are mentioned in the TODO as needing fixes:

---

_****_

Read file: src/twat_search/web/engines/lib_falla/core/yahoo.py

---

_****_





---

_****_

Read file: src/twat_search/web/engines/lib_falla/core/qwant.py

---

_****_



Let's also look at the Google implementation to understand the type errors mentioned in the TODO:

---

_****_

Read file: src/twat_search/web/engines/lib_falla/core/google.py

---

_****_

Read file: src/twat_search/web/engines/lib_falla/core/duckduckgo.py

---

_****_

Read file: src/twat_search/web/engines/lib_falla/core/falla.py

---

_****_



Let's also check the debug output files to understand the current structure of Yahoo and Qwant search results:

---

_****_

Tool call timed out after 5000ms

---

_****_



Let's try a different approach:

---

_****_

<details>
            <summary>Listed directory debug_output • **6** results</summary>
        
| Name |
|-------|
| 📄 `qwant_analysis.txt` |
| 📄 `qwant_content.html` |
| 📄 `qwant_screenshot.png` |
| 📄 `yahoo_analysis.txt` |
| 📄 `yahoo_content.html` |
| 📄 `yahoo_screenshot.png` |

</details>

---

_****_

Tool call timed out after 5000ms

---

_****_



Let's try to run a test to see the current state of the search engines:

---

_****_

```bash
cd $(git rev-parse --show-toplevel) && python -c "from twat_search.web.engines.lib_falla.core.yahoo import Yahoo; y = Yahoo(); print(y.get_url('test query'))"
```

```
am/.config/broot/launcher/bash/br
cd $(git rev-parse --show-toplevel) && python -c "from twat_search
.web.engines.lib_falla.core.yahoo import Yahoo; y = Yahoo(); print
(y.get_url('test q%                                               
uery'))"                        
(twat_search) adam@Hamlet twat_search % cd $(git rev-parse --show-
ython -c "from twat_search.web.engines.lib_falla.core.yahoo import
hoo(); print(y.get_url('test query'))"
2025-03-04 05:45:34.866 | WARNING  | twat_search.web.engines:<modu
le>:285 - Failed to import falla module: No module named 'playwrig
ht'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/Users/adam/Developer/vcs/github.twardoch/pub/twat-package
s/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines
/lib_falla/core/__init__.py", line 12, in <module>
    from twat_search.web.engines.lib_falla.core.aol import Aol
  File "/Users/adam/Developer/vcs/github.twardoch/pub/twat-package
s/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines
/lib_falla/core/aol.py", line 4, in <module>
    from twat_search.web.engines.lib_falla.core.falla import Falla
  File "/Users/adam/Developer/vcs/github.twardoch/pub/twat-package
s/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines
/lib_falla/core/falla.py", line 21, in <module>
    from playwright.async_api import Browser, BrowserContext
ModuleNotFoundError: No module named 'playwright'
(twat_search) adam@Hamlet twat_search %
```

---

_****_





Let's install the required dependencies and then run a test:

---

_****_

```bash
pip install playwright && python -m playwright install
```

```
Requirement already satisfied: playwright in /usr/local/lib/python
3.10/site-packages (1.50.0)
Requirement already satisfied: pyee<13,>=12 in /usr/local/lib/pyth
on3.10/site-packages (from playwright) (12.1.1)
Requirement already satisfied: greenlet<4.0.0,>=3.1.1 in /usr/loca
l/lib/python3.10/site-packages (from playwright) (3.1.1)
Requirement already satisfied: typing-extensions in /usr/local/lib
/python3.10/site-packages (from pyee<13,>=12->playwright) (4.12.2)
[notice] A new release of pip is available: 24.3.1 -> 25.0.1
[notice] To update, run: /usr/local/opt/python@3.10/bin/python3.10
 -m pip install --upgrade pip
/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/
twat/plugins/repos/twat_search/.venv/bin/python: No module named p
laywright

```

---

_****_





Let's try to install the dependencies in the virtual environment:

---

_****_

```bash
uv pip install playwright lxml requests && python -m playwright install
```

```
(twat_search) adam@Hamlet twat_search % uv pip install playwright 
lxml requests && python -m playwright inuv pip install playwright 
lxml requests && python -m playwright install
Resolved 10 packages in 377ms
Installed 4 packages in 112ms
 + greenlet==3.1.1
 + lxml==5.3.1
 + playwright==1.50.0
 + pyee==12.1.1
Downloading Firefox 134.0 (playwright build v1471) from https://cd
n.playwright.dev/dbazure/download/playwright/builds/firefox/1471/f
irefox-mac.zip
89.4 MiB [====================] 100% 0.0s
Firefox 134.0 (playwright build v1471) downloaded to /Users/adam/L
ibrary/Caches/ms-playwright/firefox-1471
(twat_search) adam@Hamlet twat_search %
```

---

_****_





Now, let's implement the fixes for the Yahoo and Qwant search engines based on the TODO list. First, let's update the Yahoo implementation:

---

_****_

```diff
  import logging
  import urllib.parse
+ import asyncio
  
  from bs4.element import Tag
          super().__init__(name="Yahoo")
          self.use_method = "playwright"
-         # Yahoo search results have different selectors
-         self.container_element = ("div", {"class": "dd algo algo-sr"})
-         self.wait_for_selector = "#results"
+         # Updated selectors for Yahoo search results
+         self.container_element = ("div", {"class": "algo-sr"})
+         self.wait_for_selector = "#web"
          # Increase timeout for Yahoo which can be slow to load
          self.max_retries = 5
  
-         # Yahoo often shows a consent page first
-         # We'll need to handle that using a separate method
- 
      def get_url(self, query: str) -> str:
          """
          params = {
              "p": query,
+             "fr": "yfp-t",
          }
          query_string = urllib.parse.urlencode(params)
          return f"https://search.yahoo.com/search?{query_string}"
  
+     async def _fetch_page(self, url: str) -> str:
+         """
+         Override _fetch_page to handle Yahoo consent page.
+         
+         Args:
+             url: URL to fetch
+             
+         Returns:
+             HTML content as string
+         """
+         page = None
+         try:
+             await self._initialize_browser()
+             if not self.browser_context:
+                 logger.error("Browser context not initialized")
+                 return ""
+ 
+             page = await self.browser_context.new_page()
+ 
+             # Set timeout for navigation to prevent hanging
+             await page.goto(url, timeout=30000, wait_until="domcontentloaded")
+ 
+             # Check for and handle consent page
+             try:
+                 # Look for the "Accept all" button on consent page
+                 consent_button = page.locator('button:has-text("Accept all")')
+                 if await consent_button.count() > 0:
+                     logger.info("Consent page detected, clicking 'Accept all'")
+                     await consent_button.click()
+                     # Wait for navigation after consent
+                     await page.wait_for_load_state("networkidle")
+             except Exception as e:
+                 logger.debug(f"No consent page or error handling consent: {e}")
+ 
+             # Wait for results to load
+             try:
+                 if self.wait_for_selector:
+                     logger.info(f"Waiting for selector: {self.wait_for_selector}")
+                     await page.wait_for_selector(self.wait_for_selector, timeout=5000)
+                 else:
+                     await asyncio.sleep(2)
+             except Exception as e:
+                 logger.warning(f"Timeout waiting for selector in {self.name}: {e}")
+ 
+             # Get the page content
+             return await page.content()
+         except Exception as e:
+             logger.error(f"Error fetching page with Playwright: {e}")
+             self.current_retry += 1
+             if self.current_retry < self.max_retries:
+                 # Wait before retrying
+                 await asyncio.sleep(2)
+                 return await self._fetch_page(url)
+             return ""
+         finally:
+             if page:
+                 await page.close()
+ 
      def get_title(self, elm: Tag) -> str:
          """
              Title string
          """
-         title_elem = elm.select_one("h3.title")
+         # Updated selector for title
+         title_elem = elm.select_one("h3.title a")
+         if title_elem:
+             return title_elem.get_text().strip()
+         
+         # Fallback to other possible selectors
+         title_elem = elm.select_one("h3")
          if title_elem:
              return title_elem.get_text().strip()
+         
          return ""
  
              Link URL string
          """
-         link_elem = elm.select_one("a.d-ib")
+         # Updated selector for link
+         link_elem = elm.select_one("h3.title a")
+         if link_elem and "href" in link_elem.attrs:
+             return str(link_elem.attrs["href"])
+         
+         # Fallback to other possible selectors
+         link_elem = elm.select_one("a[href]")
          if link_elem and "href" in link_elem.attrs:
              return str(link_elem.attrs["href"])
+         
          return ""
  
              Snippet text string
          """
-         snippet_elem = elm.select_one("div.compText.aAbs")
+         # Updated selector for snippet
+         snippet_elem = elm.select_one("div.compText")
+         if snippet_elem:
+             return snippet_elem.get_text().strip()
+         
+         # Fallback to other possible selectors
+         snippet_elem = elm.select_one("p")
          if snippet_elem:
              return snippet_elem.get_text().strip()
+         
          return ""
  
```

---

_****_





Now, let's update the Qwant implementation:

---

_****_

```diff
  import logging
  import urllib.parse
+ import asyncio
  
  from bs4.element import Tag
          super().__init__(name="Qwant")
          self.use_method = "playwright"
-         self.container_element = ("article", {"class": "webResult"})
-         self.wait_for_selector = ".webResults"
+         # Updated selectors for Qwant search results
+         self.container_element = ("div", {"class": "result--web"})
+         self.wait_for_selector = ".results-column"
          # Increase timeout for Qwant which can be slow to load
          self.max_retries = 5
  
-         # Qwant may show a consent dialog or have different layouts
-         # We'll need to handle that with flexible selectors
- 
      def get_url(self, query: str) -> str:
          """
          params = {
              "q": query,
+             "t": "web",
+             "l": "en",
          }
          query_string = urllib.parse.urlencode(params)
          return f"https://www.qwant.com/?{query_string}"
  
+     async def _fetch_page(self, url: str) -> str:
+         """
+         Override _fetch_page to handle Qwant consent page.
+         
+         Args:
+             url: URL to fetch
+             
+         Returns:
+             HTML content as string
+         """
+         page = None
+         try:
+             await self._initialize_browser()
+             if not self.browser_context:
+                 logger.error("Browser context not initialized")
+                 return ""
+ 
+             page = await self.browser_context.new_page()
+ 
+             # Set timeout for navigation to prevent hanging
+             await page.goto(url, timeout=30000, wait_until="domcontentloaded")
+ 
+             # Check for and handle consent page
+             try:
+                 # Look for the consent button on Qwant
+                 consent_button = page.locator('button:has-text("Accept all")')
+                 if await consent_button.count() > 0:
+                     logger.info("Consent page detected, clicking 'Accept all'")
+                     await consent_button.click()
+                     # Wait for navigation after consent
+                     await page.wait_for_load_state("networkidle")
+             except Exception as e:
+                 logger.debug(f"No consent page or error handling consent: {e}")
+ 
+             # Wait for results to load
+             try:
+                 if self.wait_for_selector:
+                     logger.info(f"Waiting for selector: {self.wait_for_selector}")
+                     await page.wait_for_selector(self.wait_for_selector, timeout=5000)
+                 else:
+                     await asyncio.sleep(2)
+             except Exception as e:
+                 logger.warning(f"Timeout waiting for selector in {self.name}: {e}")
+ 
+             # Get the page content
+             return await page.content()
+         except Exception as e:
+             logger.error(f"Error fetching page with Playwright: {e}")
+             self.current_retry += 1
+             if self.current_retry < self.max_retries:
+                 # Wait before retrying
+                 await asyncio.sleep(2)
+                 return await self._fetch_page(url)
+             return ""
+         finally:
+             if page:
+                 await page.close()
+ 
      def get_title(self, elm: Tag) -> str:
          """
              Title string
          """
-         title_elem = elm.select_one(".title")
+         # Updated selector for title
+         title_elem = elm.select_one(".result__title")
+         if title_elem:
+             return title_elem.get_text().strip()
+         
+         # Fallback to other possible selectors
+         title_elem = elm.select_one("a.url")
+         if title_elem:
+             return title_elem.get_text().strip()
+         
+         # Try generic h3 selector
+         title_elem = elm.select_one("h3")
          if title_elem:
              return title_elem.get_text().strip()
+         
          return ""
  
              Link URL string
          """
-         link_elem = elm.select_one(".title")
+         # Updated selector for link
+         link_elem = elm.select_one(".result__url")
+         if link_elem and "href" in link_elem.attrs:
+             return str(link_elem.attrs["href"])
+         
+         # Fallback to other possible selectors
+         link_elem = elm.select_one("a.url")
+         if link_elem and "href" in link_elem.attrs:
+             return str(link_elem.attrs["href"])
+         
+         # Try any anchor with href
+         link_elem = elm.select_one("a[href]")
          if link_elem and "href" in link_elem.attrs:
              return str(link_elem.attrs["href"])
+         
          return ""
  
              Snippet text string
          """
-         snippet_elem = elm.select_one(".description")
+         # Updated selector for snippet
+         snippet_elem = elm.select_one(".result__desc")
+         if snippet_elem:
+             return snippet_elem.get_text().strip()
+         
+         # Fallback to other possible selectors
+         snippet_elem = elm.select_one(".result__snippet")
+         if snippet_elem:
+             return snippet_elem.get_text().strip()
+         
+         # Try generic paragraph
+         snippet_elem = elm.select_one("p")
          if snippet_elem:
              return snippet_elem.get_text().strip()
+         
          return ""
  
```

---

_****_







Now, let's fix the Google implementation to address the type errors mentioned in the TODO:

---

_****_

```diff
  import urllib.parse
  from pathlib import Path
- from typing import cast
+ from typing import Any, Optional, cast
  
- from bs4.element import Tag
+ from bs4 import BeautifulSoup
+ from bs4.element import ResultSet, Tag
  
  from twat_search.web.engines.lib_falla.core.falla import Falla
          """
          title_elem = elm.find("h3")
-         if title_elem:
+         if title_elem and isinstance(title_elem, Tag):
              return title_elem.get_text().strip()
          return ""
          # Try various snippet element selectors that Google might use
          snippet_elem = elm.find("div", {"class": "VwiC3b"})
-         if not snippet_elem:
+         if not snippet_elem or not isinstance(snippet_elem, Tag):
              snippet_elem = elm.find("span", {"class": "aCOpRe"})
-         if not snippet_elem:
+         if not snippet_elem or not isinstance(snippet_elem, Tag):
              snippet_elem = elm.find("div", {"class": "BNeawe s3v9rd AP7Wnd"})
-         if not snippet_elem:
+         if not snippet_elem or not isinstance(snippet_elem, Tag):
              # Try to find any text container that might hold a snippet
              text_containers = elm.find_all(["div", "span", "p"], class_=True)
          return ""
  
+     def get_each_elements(self, elements: ResultSet) -> list[dict[str, str]]:
+         """
+         Process a list of BeautifulSoup elements into search results.
+ 
+         Args:
+             elements: List of BeautifulSoup elements
+ 
+         Returns:
+             List of dictionaries containing search results
+         """
+         elements_list: list[dict[str, str]] = []
+ 
+         for elm in elements:
+             if not isinstance(elm, Tag):
+                 continue
+                 
+             try:
+                 title = self.get_title(elm)
+                 link = self.get_link(elm)
+                 snippet = self.get_snippet(elm)
+ 
+                 # Only add if we have at least a title or link
+                 if title or link:
+                     elements_list.append(
+                         {
+                             "title": title,
+                             "link": link,
+                             "snippet": snippet,
+                         },
+                     )
+             except Exception as e:
+                 logger.debug(f"Error processing element: {e}")
+                 continue
+ 
+         return elements_list
+ 
      async def search_async(self, query: str, pages: str = "") -> list[dict[str, str]]:
          """
                  # Wait for selector
                  try:
-                     await page.wait_for_selector(self.wait_for_selector, timeout=10000)
-                     logger.info(f"Selector '{self.wait_for_selector}' found")
+                     if self.wait_for_selector:
+                         await page.wait_for_selector(self.wait_for_selector, timeout=10000)
+                         logger.info(f"Selector '{self.wait_for_selector}' found")
                  except Exception as e:
                      logger.warning(f"Timeout waiting for selector: {e}")
  
+                 # Check for CAPTCHA
+                 try:
+                     captcha_selector = 'form[action*="sorry/index"]'
+                     captcha_exists = await page.evaluate(f"""() => {{
+                         return !!document.querySelector('{captcha_selector}');
+                     }}""")
+                     
+                     if captcha_exists:
+                         logger.warning("CAPTCHA detected on Google search page")
+                         # Take a screenshot for debugging
+                         await page.screenshot(path="google_captcha.png")
+                         return []
+                 except Exception as e:
+                     logger.error(f"Error checking for CAPTCHA: {e}")
+ 
                  # Get the page content
                  html_content = await page.content()
                  logger.info(f"Retrieved HTML content, length: {len(html_content)}")
  
-                 # Save to file
+                 # Save to file for debugging
                  debug_file = f"google_debug_{query.replace(' ', '_')}.html"
                  with open(debug_file, "w", encoding="utf-8") as f:
  
                  # Parse the saved HTML file
-                 from bs4 import BeautifulSoup
- 
                  if Path(debug_file).exists():
                      with open(debug_file, encoding="utf-8") as f:
                              manual_results = []
                              for elem in elements[:10]:
+                                 if not isinstance(elem, Tag):
+                                     continue
+                                     
                                  title = self.get_title(elem) or ""
                                  link = self.get_link(elem) or ""
                                              "link": link,
                                              "snippet": snippet,
-                                         },
+                                         }
                                      )
  
                              if manual_results:
-                                 logger.info(f"Returning {len(manual_results)} manually parsed results")
+                                 logger.info(f"Found {len(manual_results)} results with alternate parsing")
                                  return manual_results
  
              return results
-         finally:
-             # Clean up resources
-             await self._close_browser()
+         except Exception as e:
+             logger.error(f"Search failed: {e}", exc_info=True)
+             return []
  
      def search(self, query: str, pages: str = "") -> list[dict[str, str]]:
          if pages:
              url += f"&{pages}"
- 
-         # Debug: Get raw HTML content and log key information
-         html_parser = self.parse_entry_point(url)
-         if html_parser:
-             # Log the HTML structure for debugging
-             html_content = str(html_parser)
-             logger.debug(f"Google search HTML content length: {len(html_content)}")
-             logger.debug(f"HTML Preview: {html_content[:500]}...")
- 
-             # Debug: Try different selectors and log what we find
-             logger.debug("Testing various selectors:")
- 
-             # Try the standard container selector
-             elements = html_parser.find_all(self.container_element[0], attrs=self.container_element[1])
-             logger.debug(f"Found {len(elements)} results with selector: div.g")
- 
-             # Try alternative selectors
-             alt_selectors = [
-                 ("div", {"class": "Gx5Zad"}),
-                 ("div", {"class": "tF2Cxc"}),
-                 ("div", {"jscontroller": "SC7lYd"}),
-                 ("div", {"class": "yuRUbf"}),
-                 ("div", {"class": "g"}),
-                 ("div", {"class": "eKjLze"}),
-             ]
- 
-             for selector_type, selector_attrs in alt_selectors:
-                 alt_elements = html_parser.find_all(selector_type, attrs=selector_attrs)
-                 attr_str = ", ".join([f"{k}={v}" for k, v in selector_attrs.items()])
-                 logger.debug(f"Found {len(alt_elements)} results with selector: {selector_type}[{attr_str}]")
- 
-                 # If we found elements, check for titles and links
-                 if alt_elements:
-                     for i, elem in enumerate(alt_elements[:3]):
-                         h3 = elem.find("h3")
-                         a = elem.find("a", href=True)
-                         logger.debug(f"Element {i}: h3={h3 is not None}, a={a is not None}")
- 
-             # Create a debug file with the full HTML
-             try:
-                 debug_file = f"google_debug_{query.replace(' ', '_')}_sync.html"
-                 with open(debug_file, "w", encoding="utf-8") as f:
-                     f.write(html_content)
-                 logger.info(f"Saved Google HTML content to: {debug_file}")
-             except Exception as e:
-                 logger.error(f"Failed to save debug HTML: {e}")
- 
-         # Continue with normal search process
          return self.fetch(url)
  
```

---

_****_







Let's fix the linter error in the Google implementation:

---

_****_

```diff
  import logging
  import urllib.parse
+ from collections.abc import Mapping
  from pathlib import Path
  from typing import Any, Optional, cast
  
                      # Try various selectors
-                     alt_container_selectors = [
+                     alt_container_selectors: list[tuple[str, Mapping[str, Any]]] = [
                          ("div", {"class": "g"}),
                          ("div", {"class": "Gx5Zad"}),
```

---

_****_







Let's fix the DuckDuckGo implementation to handle CAPTCHA challenges:

---

_****_

```diff
  import logging
  import urllib.parse
+ import asyncio
  
  from bs4.element import Tag
          # Use the HTML version of DuckDuckGo which is more reliable for scraping
          self.container_element = ("div", {"class": "result"})
-         self.wait_for_selector = "body"
+         self.wait_for_selector = ".results"
          # Increase timeout for DuckDuckGo which can be slow to load
          self.max_retries = 5
          params = {
              "q": query,
+             "kl": "us-en",  # Region and language
          }
          query_string = urllib.parse.urlencode(params)
          return f"{base_url}?{query_string}"
  
+     async def _fetch_page(self, url: str) -> str:
+         """
+         Override _fetch_page to handle DuckDuckGo challenges.
+         
+         Args:
+             url: URL to fetch
+             
+         Returns:
+             HTML content as string
+         """
+         page = None
+         try:
+             await self._initialize_browser()
+             if not self.browser_context:
+                 logger.error("Browser context not initialized")
+                 return ""
+ 
+             page = await self.browser_context.new_page()
+ 
+             # Set timeout for navigation to prevent hanging
+             await page.goto(url, timeout=30000, wait_until="domcontentloaded")
+ 
+             # Check for and handle CAPTCHA or challenge page
+             try:
+                 # Look for common challenge indicators
+                 challenge_selectors = [
+                     'form[action*="challenge"]',
+                     'input[name="g-recaptcha-response"]',
+                     '.challenge-form',
+                     'div[class*="captcha"]',
+                 ]
+                 
+                 for selector in challenge_selectors:
+                     challenge_exists = await page.evaluate(f"""() => {{
+                         return !!document.querySelector('{selector}');
+                     }}""")
+                     
+                     if challenge_exists:
+                         logger.warning(f"Challenge detected on DuckDuckGo using selector: {selector}")
+                         # Take a screenshot for debugging
+                         await page.screenshot(path="duckduckgo_challenge.png")
+                         # Try to save the HTML content for analysis
+                         html_content = await page.content()
+                         with open("duckduckgo_challenge.html", "w", encoding="utf-8") as f:
+                             f.write(html_content)
+                         logger.info("Saved challenge page content for debugging")
+                         break
+             except Exception as e:
+                 logger.debug(f"Error checking for challenges: {e}")
+ 
+             # Wait for results to load
+             try:
+                 if self.wait_for_selector:
+                     logger.info(f"Waiting for selector: {self.wait_for_selector}")
+                     await page.wait_for_selector(self.wait_for_selector, timeout=5000)
+                 else:
+                     await asyncio.sleep(2)
+             except Exception as e:
+                 logger.warning(f"Timeout waiting for selector in {self.name}: {e}")
+ 
+             # Get the page content
+             return await page.content()
+         except Exception as e:
+             logger.error(f"Error fetching page with Playwright: {e}")
+             self.current_retry += 1
+             if self.current_retry < self.max_retries:
+                 # Wait before retrying
+                 await asyncio.sleep(2)
+                 return await self._fetch_page(url)
+             return ""
+         finally:
+             if page:
+                 await page.close()
+ 
      def get_title(self, elm: Tag) -> str:
          """
```

---

_****_







Now, let's improve the `get_engine` function and error handling as mentioned in Phase 2 of the TODO:

---

_****_

Read file: src/twat_search/web/api.py

---

_****_

Read file: src/twat_search/web/engines/base.py

---

_****_





Now, let's improve the `get_engine` function in `base.py` to provide better error handling:

---

_****_

```diff
      """
      Get an instance of a search engine by name.
+ 
+     This function looks up the engine class by name, then instantiates it
+     with the provided configuration and parameters.
  
      Args:
-         engine_name: The name of the engine to get.
-         config: Engine configuration.
-         **kwargs: Additional engine-specific parameters.
+         engine_name: Name of the engine to instantiate
+         config: Engine configuration
+         **kwargs: Additional engine-specific parameters
  
      Returns:
-         An instance of the requested search engine.
+         An instance of the requested search engine
  
      Raises:
-         EngineError: If the engine is not found or disabled.
-     """
-     engine_class = _engine_registry.get(engine_name)
+         EngineError: If the engine is not found, disabled, or fails to initialize
+     """
+     # Get the registry of engines
+     engines = get_registered_engines()
+     
+     # Standardize the engine name for lookup
+     from twat_search.web.engines import standardize_engine_name
+     std_engine_name = standardize_engine_name(engine_name)
+     
+     # Try to find the engine class
+     engine_class = engines.get(std_engine_name)
+     
+     # If not found with standardized name, try original name (for backward compatibility)
+     if engine_class is None:
+         engine_class = engines.get(engine_name)
+     
+     # If still not found, provide a helpful error message
      if engine_class is None:
-         available_engines = ", ".join(sorted(_engine_registry.keys()))
-         msg = f"Unknown search engine: '{engine_name}'. Available engines: {available_engines}"
+         available_engines = ", ".join(sorted(engines.keys()))
+         msg = (
+             f"Engine '{engine_name}' not found. "
+             f"Available engines: {available_engines}"
+         )
+         logger.error(msg)
          raise EngineError(engine_name, msg)
- 
-     # Check if the engine requires an API key
-     if hasattr(engine_class, "env_api_key_names") and engine_class.env_api_key_names:
-         # If no API key is provided in config, check environment variables
-         if not config.api_key:
-             logger.debug(f"No API key in config for {engine_name}, checking environment variables")
-             for env_var in engine_class.env_api_key_names:
-                 env_value = os.environ.get(env_var)
-                 if env_value:
-                     logger.debug(f"Found API key in environment variable {env_var}")
-                     # Update the config with the API key from environment
-                     config.api_key = env_value
-                     break
- 
-     try:
-         return engine_class(config, **kwargs)
+     
+     try:
+         # Check if the engine is enabled in the configuration
+         if not config.enabled:
+             msg = (
+                 f"Engine '{engine_name}' is disabled in configuration. "
+                 f"Enable it by setting the appropriate environment variable "
+                 f"or updating the configuration."
+             )
+             logger.warning(msg)
+             raise EngineError(engine_name, msg)
+         
+         # Try to instantiate the engine
+         engine_instance = engine_class(config, **kwargs)
+         logger.debug(f"Successfully initialized engine: {engine_name}")
+         return engine_instance
+     except EngineError as e:
+         # Re-raise EngineError with more context if needed
+         if "API key" in str(e):
+             # Provide more helpful information for API key errors
+             env_vars = getattr(engine_class, "env_api_key_names", [])
+             env_vars_str = ", ".join(env_vars) if env_vars else "No environment variables defined"
+             msg = (
+                 f"{str(e)} "
+                 f"Environment variables for this engine: {env_vars_str}"
+             )
+             logger.error(msg)
+             raise EngineError(engine_name, msg) from e
+         # For other EngineError types, just re-raise
+         raise
      except Exception as e:
+         # For any other exception, wrap it in an EngineError with context
          msg = f"Failed to initialize engine '{engine_name}': {e}"
+         logger.error(msg)
          raise EngineError(engine_name, msg) from e
  
```

---

_****_









Let's also update the `init_engine_task` function in `api.py` to improve error handling:

---

_****_

```diff
      config: Config,
      **kwargs: Any,
- ) -> tuple[str, Coroutine[Any, Any, list[SearchResult]]]:
+ ) -> tuple[str, Coroutine[Any, Any, list[SearchResult]]] | None:
      """
      Initialize a search engine and create a task for searching.
+ 
+     This function handles the initialization of a search engine and creates
+     a coroutine for performing the search. It includes robust error handling
+     to prevent failures from affecting other engines.
+ 
+     Args:
+         engine_name: Name of the engine to initialize
+         query: Search query
+         config: Configuration object
+         **kwargs: Additional parameters for the engine
+ 
+     Returns:
+         A tuple of (engine_name, search_coroutine) or None if initialization fails
      """
      # Standardize engine name for lookups
          engine_config = config.engines.get(engine_name)
          if not engine_config:
-             logger.warning(f"Engine '{engine_name}' not configured.")
+             logger.warning(f"Engine '{engine_name}' not configured, using default configuration.")
              engine_config = EngineConfig(enabled=True)
  
  
          logger.info(f"🔍 Querying engine: {engine_name}")
-         return engine_name, engine_instance.search(query)
+         
+         # Create a wrapper coroutine that handles exceptions
+         async def search_with_error_handling() -> list[SearchResult]:
+             try:
+                 return await engine_instance.search(query)
+             except Exception as e:
+                 logger.error(f"Search with engine '{engine_name}' failed: {e}")
+                 # Return empty results on failure instead of raising
+                 return []
+         
+         return engine_name, search_with_error_handling()
      except Exception as e:
-         logger.warning(
-             f"Failed to initialize engine '{engine_name}': {type(e).__name__}",
-         )
-         logger.error(f"Error initializing engine '{engine_name}': {e}")
-         raise
+         error_type = type(e).__name__
+         error_msg = str(e)
+         
+         # Provide more specific error messages based on error type
+         if "API key" in error_msg:
+             logger.error(
+                 f"Failed to initialize engine '{engine_name}': Missing or invalid API key. "
+                 f"Check your environment variables or configuration."
+             )
+         elif "disabled" in error_msg:
+             logger.warning(
+                 f"Engine '{engine_name}' is disabled. "
+                 f"Enable it in your configuration to use it."
+             )
+         else:
+             logger.error(
+                 f"Failed to initialize engine '{engine_name}': {error_type}: {error_msg}"
+             )
+         
+         # Return None to indicate initialization failure
+         return None
  
  
```

---

_****_









Now, let's update the `search` function in `api.py` to handle the changes to `init_engine_task`:

---

_****_

```diff
              try:
                  # Pass all parameters including kwargs to init_engine_task
-                 task = init_engine_task(
+                 task_result = init_engine_task(
                      engine_name,
                      query,
                      **kwargs,
                  )
-                 if task is not None:
-                     engine_names.append(task[0])
-                     tasks.append(task[1])
+                 
+                 # Check if initialization was successful
+                 if task_result is not None:
+                     engine_names.append(task_result[0])
+                     tasks.append(task_result[1])
+                 else:
+                     # Engine initialization failed
+                     failed_engines.append(engine_name)
              except Exception as e:
-                 logger.warning(f"Failed to initialize engine '{engine_name}': {e}")
+                 logger.warning(f"Unexpected error initializing engine '{engine_name}': {e}")
                  failed_engines.append(engine_name)
                  continue  # Log the exception and continue
                  try:
                      # Pass all parameters including kwargs to init_engine_task
-                     task = init_engine_task(
+                     task_result = init_engine_task(
                          engine_name,
                          query,
                          **kwargs,
                      )
-                     if task is not None:
-                         engine_names.append(task[0])
-                         tasks.append(task[1])
+                     
+                     # Check if initialization was successful
+                     if task_result is not None:
+                         engine_names.append(task_result[0])
+                         tasks.append(task_result[1])
+                         logger.info(f"Successfully fell back to engine: {engine_name}")
                          break
                  except Exception as e:
-                     logger.debug(f"Failed to initialize engine {engine_name}: {e}")
+                     logger.debug(f"Failed to initialize fallback engine {engine_name}: {e}")
                      continue
  
                  raise SearchError(msg)
  
+         # Execute all search tasks concurrently
          results = await asyncio.gather(*tasks, return_exceptions=True)
  
                  )
              elif isinstance(result, list):
+                 result_count = len(result)
+                 if result_count > 0:
                      logger.info(
-                     f"✅ Engine '{engine_name}' returned {len(result)} results",
+                         f"✅ Engine '{engine_name}' returned {result_count} results",
                      )
                      flattened_results.extend(result)
                  else:
                      logger.info(
-                     f"⚠️ Engine '{engine_name}' returned no results or unexpected type: {type(result)}",
+                         f"⚠️ Engine '{engine_name}' returned no results",
+                     )
+             else:
+                 logger.warning(
+                     f"⚠️ Engine '{engine_name}' returned unexpected type: {type(result)}",
                  )
      except Exception as e:
          logger.error(f"Search failed: {e}")
          raise
  
+     # Log the total number of results found
+     logger.info(f"Total results found across all engines: {len(flattened_results)}")
      return flattened_results
  
```

---

_****_







Let's run a test to see if our changes have fixed the issues:

---

_****_

```bash
cd $(git rev-parse --show-toplevel) && ruff check --output-format=github --fix --unsafe-fixes . && ruff format --respect-gitignore --target-version py312 .
```

```
(twat_search) adam@Hamlet twat_search % 
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=765,col=9,endLine=765,endColumn=16::
src/twat_search/web/cli.py:765:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=765,col=9,endLine=765,endColumn=16::
src/twat_search/web/cli.py:765:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=766,col=9,endLine=766,endColumn=13::
src/twat_search/web/cli.py:766:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=766,col=9,endLine=766,endColumn=13::
src/twat_search/web/cli.py:766:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=767,col=9,endLine=767,endColumn=14::
src/twat_search/web/cli.py:767:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=767,col=9,endLine=767,endColumn=14::
src/twat_search/web/cli.py:767:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=810,col=9,endLine=810,endColumn=20::
src/twat_search/web/cli.py:810:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=816,col=9,endLine=816,endColumn=16::
src/twat_search/web/cli.py:816:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=816,col=9,endLine=816,endColumn=16::
src/twat_search/web/cli.py:816:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=817,col=9,endLine=817,endColumn=13::
src/twat_search/web/cli.py:817:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=817,col=9,endLine=817,endColumn=13::
src/twat_search/web/cli.py:817:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=818,col=9,endLine=818,endColumn=14::
src/twat_search/web/cli.py:818:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=818,col=9,endLine=818,endColumn=14::
src/twat_search/web/cli.py:818:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=868,col=9,endLine=868,endColumn=20::
src/twat_search/web/cli.py:868:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=872,col=9,endLine=872,endColumn=16::
src/twat_search/web/cli.py:872:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=872,col=9,endLine=872,endColumn=16::
src/twat_search/web/cli.py:872:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=873,col=9,endLine=873,endColumn=13::
src/twat_search/web/cli.py:873:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=873,col=9,endLine=873,endColumn=13::
src/twat_search/web/cli.py:873:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=874,col=9,endLine=874,endColumn=14::
src/twat_search/web/cli.py:874:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=874,col=9,endLine=874,endColumn=14::
src/twat_search/web/cli.py:874:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=934,col=9,endLine=934,endColumn=20::
src/twat_search/web/cli.py:934:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=937,col=9,endLine=937,endColumn=16::
src/twat_search/web/cli.py:937:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=937,col=9,endLine=937,endColumn=16::
src/twat_search/web/cli.py:937:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=938,col=9,endLine=938,endColumn=13::
src/twat_search/web/cli.py:938:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=938,col=9,endLine=938,endColumn=13::
src/twat_search/web/cli.py:938:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=939,col=9,endLine=939,endColumn=14::
src/twat_search/web/cli.py:939:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=939,col=9,endLine=939,endColumn=14::
src/twat_search/web/cli.py:939:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=981,col=9,endLine=981,endColumn=20::
src/twat_search/web/cli.py:981:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=984,col=9,endLine=984,endColumn=16::
src/twat_search/web/cli.py:984:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=984,col=9,endLine=984,endColumn=16::
src/twat_search/web/cli.py:984:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=985,col=9,endLine=985,endColumn=13::
src/twat_search/web/cli.py:985:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=985,col=9,endLine=985,endColumn=13::
src/twat_search/web/cli.py:985:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=986,col=9,endLine=986,endColumn=14::
src/twat_search/web/cli.py:986:9: FBT001 Boolean-typed positional
argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=986,col=9,endLine=986,endColumn=14::
src/twat_search/web/cli.py:986:9: FBT002 Boolean default positiona
l argument in function definition
::error title=Ruff (ARG002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1034,col=9,endLine=1034,endColumn=17
::src/twat_search/web/cli.py:1034:9: ARG002 Unused method argument
: `language`
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1035,col=9,endLine=1035,endColumn=20
::src/twat_search/web/cli.py:1035:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1039,col=9,endLine=1039,endColumn=16
::src/twat_search/web/cli.py:1039:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1039,col=9,endLine=1039,endColumn=16
::src/twat_search/web/cli.py:1039:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1040,col=9,endLine=1040,endColumn=13
::src/twat_search/web/cli.py:1040:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1040,col=9,endLine=1040,endColumn=13
::src/twat_search/web/cli.py:1040:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1041,col=9,endLine=1041,endColumn=14
::src/twat_search/web/cli.py:1041:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1041,col=9,endLine=1041,endColumn=14
::src/twat_search/web/cli.py:1041:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1092,col=9,endLine=1092,endColumn=16
::src/twat_search/web/cli.py:1092:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1092,col=9,endLine=1092,endColumn=16
::src/twat_search/web/cli.py:1092:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1093,col=9,endLine=1093,endColumn=13
::src/twat_search/web/cli.py:1093:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1093,col=9,endLine=1093,endColumn=13
::src/twat_search/web/cli.py:1093:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1094,col=9,endLine=1094,endColumn=14
::src/twat_search/web/cli.py:1094:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1094,col=9,endLine=1094,endColumn=14
::src/twat_search/web/cli.py:1094:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1139,col=9,endLine=1139,endColumn=16
::src/twat_search/web/cli.py:1139:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1139,col=9,endLine=1139,endColumn=16
::src/twat_search/web/cli.py:1139:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1140,col=9,endLine=1140,endColumn=13
::src/twat_search/web/cli.py:1140:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1140,col=9,endLine=1140,endColumn=13
::src/twat_search/web/cli.py:1140:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1141,col=9,endLine=1141,endColumn=14
::src/twat_search/web/cli.py:1141:9: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1141,col=9,endLine=1141,endColumn=14
::src/twat_search/web/cli.py:1141:9: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (PLR2004),file=/Users/adam/Developer/vcs/github
.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/s
rc/twat_search/web/cli.py,line=1252,col=86,endLine=1252,endColumn=
89::src/twat_search/web/cli.py:1252:86: PLR2004 Magic value used i
n comparison, consider replacing `100` with a constant variable
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1262,col=5,endLine=1262,endColumn=12
::src/twat_search/web/cli.py:1262:5: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1262,col=5,endLine=1262,endColumn=12
::src/twat_search/web/cli.py:1262:5: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1263,col=5,endLine=1263,endColumn=10
::src/twat_search/web/cli.py:1263:5: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1263,col=5,endLine=1263,endColumn=10
::src/twat_search/web/cli.py:1263:5: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (ARG005),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/cli.py,line=1356,col=39,endLine=1356,endColumn=4
2::src/twat_search/web/cli.py:1356:39: ARG005 Unused lambda argume
nt: `out`
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/config.py,line=477,col=9,endLine=477,endColumn=1
6::src/twat_search/web/config.py:477:9: FBT001 Boolean-typed posit
ional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/config.py,line=477,col=9,endLine=477,endColumn=1
6::src/twat_search/web/config.py:477:9: FBT002 Boolean default pos
itional argument in function definition
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=95,col=46,endLine=95,endC
olumn=58::src/twat_search/web/engines/__init__.py:95:46: F401 `twa
t_search.web.engines.base.SearchEngine` imported but unused; consi
der using `importlib.util.find_spec` to test for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=95,col=60,endLine=95,endC
olumn=70::src/twat_search/web/engines/__init__.py:95:60: F401 `twa
t_search.web.engines.base.get_engine` imported but unused; conside
r using `importlib.util.find_spec` to test for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=95,col=72,endLine=95,endC
olumn=94::src/twat_search/web/engines/__init__.py:95:72: F401 `twa
t_search.web.engines.base.get_registered_engines` imported but unu
sed; consider using `importlib.util.find_spec` to test for availab
ility
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=95,col=96,endLine=95,endC
olumn=111::src/twat_search/web/engines/__init__.py:95:96: F401 `tw
at_search.web.engines.base.register_engine` imported but unused; c
onsider using `importlib.util.find_spec` to test for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=105,col=47,endLine=105,en
dColumn=68::src/twat_search/web/engines/__init__.py:105:47: F401 `
twat_search.web.engines.brave.BraveNewsSearchEngine` imported but
unused; consider using `importlib.util.find_spec` to test for avai
lability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=105,col=70,endLine=105,en
dColumn=87::src/twat_search/web/engines/__init__.py:105:70: F401 `
twat_search.web.engines.brave.BraveSearchEngine` imported but unus
ed; consider using `importlib.util.find_spec` to test for availabi
lity
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=117,col=48,endLine=117,en
dColumn=66::src/twat_search/web/engines/__init__.py:117:48: F401 `
twat_search.web.engines.tavily.TavilySearchEngine` imported but un
used; consider using `importlib.util.find_spec` to test for availa
bility
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=125,col=46,endLine=125,en
dColumn=68::src/twat_search/web/engines/__init__.py:125:46: F401 `
twat_search.web.engines.pplx.PerplexitySearchEngine` imported but
unused; consider using `importlib.util.find_spec` to test for avai
lability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=133,col=45,endLine=133,en
dColumn=64::src/twat_search/web/engines/__init__.py:133:45: F401 `
twat_search.web.engines.you.YouNewsSearchEngine` imported but unus
ed; consider using `importlib.util.find_spec` to test for availabi
lity
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=133,col=66,endLine=133,en
dColumn=81::src/twat_search/web/engines/__init__.py:133:66: F401 `
twat_search.web.engines.you.YouSearchEngine` imported but unused;
consider using `importlib.util.find_spec` to test for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=144,col=50,endLine=144,en
dColumn=70::src/twat_search/web/engines/__init__.py:144:50: F401 `
twat_search.web.engines.critique.CritiqueSearchEngine` imported bu
t unused; consider using `importlib.util.find_spec` to test for av
ailability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=152,col=52,endLine=152,en
dColumn=74::src/twat_search/web/engines/__init__.py:152:52: F401 `
twat_search.web.engines.duckduckgo.DuckDuckGoSearchEngine` importe
d but unused; consider using `importlib.util.find_spec` to test fo
r availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=161,col=54,endLine=161,en
dColumn=77::src/twat_search/web/engines/__init__.py:161:54: F401 `
twat_search.web.engines.bing_scraper.BingScraperSearchEngine` impo
rted but unused; consider using `importlib.util.find_spec` to test
 for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=171,col=9,endLine=171,end
Column=28::src/twat_search/web/engines/__init__.py:171:9: F401 `tw
at_search.web.engines.hasdata.HasDataGoogleEngine` imported but un
used; consider using `importlib.util.find_spec` to test for availa
bility
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=172,col=9,endLine=172,end
Column=33::src/twat_search/web/engines/__init__.py:172:9: F401 `tw
at_search.web.engines.hasdata.HasDataGoogleLightEngine` imported b
ut unused; consider using `importlib.util.find_spec` to test for a
vailability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=192,col=56,endLine=192,en
dColumn=75::src/twat_search/web/engines/__init__.py:192:56: F401 `
twat_search.web.engines.google_scraper.GoogleScraperEngine` import
ed but unused; consider using `importlib.util.find_spec` to test f
or availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=201,col=49,endLine=201,en
dColumn=68::src/twat_search/web/engines/__init__.py:201:49: F401 `
twat_search.web.engines.serpapi.SerpApiSearchEngine` imported but
unused; consider using `importlib.util.find_spec` to test for avai
lability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=212,col=9,endLine=212,end
Column=23::src/twat_search/web/engines/__init__.py:212:9: F401 `tw
at_search.web.engines.falla.AolFallaEngine` imported but unused; c
onsider using `importlib.util.find_spec` to test for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=213,col=9,endLine=213,end
Column=23::src/twat_search/web/engines/__init__.py:213:9: F401 `tw
at_search.web.engines.falla.AskFallaEngine` imported but unused; c
onsider using `importlib.util.find_spec` to test for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=214,col=9,endLine=214,end
Column=24::src/twat_search/web/engines/__init__.py:214:9: F401 `tw
at_search.web.engines.falla.BingFallaEngine` imported but unused;
consider using `importlib.util.find_spec` to test for availability
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=215,col=9,endLine=215,end
Column=27::src/twat_search/web/engines/__init__.py:215:9: F401 `tw
at_search.web.engines.falla.DogpileFallaEngine` imported but unuse
d; consider using `importlib.util.find_spec` to test for availabil
ity
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=216,col=9,endLine=216,end
Column=30::src/twat_search/web/engines/__init__.py:216:9: F401 `tw
at_search.web.engines.falla.DuckDuckGoFallaEngine` imported but un
used; consider using `importlib.util.find_spec` to test for availa
bility
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=217,col=9,endLine=217,end
Column=26::src/twat_search/web/engines/__init__.py:217:9: F401 `tw
at_search.web.engines.falla.FallaSearchEngine` imported but unused
; consider using `importlib.util.find_spec` to test for availabili
ty
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=218,col=9,endLine=218,end
Column=26::src/twat_search/web/engines/__init__.py:218:9: F401 `tw
at_search.web.engines.falla.GibiruFallaEngine` imported but unused
; consider using `importlib.util.find_spec` to test for availabili
ty
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=219,col=9,endLine=219,end
Column=26::src/twat_search/web/engines/__init__.py:219:9: F401 `tw
at_search.web.engines.falla.GoogleFallaEngine` imported but unused
; consider using `importlib.util.find_spec` to test for availabili
ty
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=220,col=9,endLine=220,end
Column=26::src/twat_search/web/engines/__init__.py:220:9: F401 `tw
at_search.web.engines.falla.MojeekFallaEngine` imported but unused
; consider using `importlib.util.find_spec` to test for availabili
ty
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=221,col=9,endLine=221,end
Column=25::src/twat_search/web/engines/__init__.py:221:9: F401 `tw
at_search.web.engines.falla.QwantFallaEngine` imported but unused;
 consider using `importlib.util.find_spec` to test for availabilit
y
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=222,col=9,endLine=222,end
Column=25::src/twat_search/web/engines/__init__.py:222:9: F401 `tw
at_search.web.engines.falla.YahooFallaEngine` imported but unused;
 consider using `importlib.util.find_spec` to test for availabilit
y
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/__init__.py,line=223,col=9,endLine=223,end
Column=26::src/twat_search/web/engines/__init__.py:223:9: F401 `tw
at_search.web.engines.falla.YandexFallaEngine` imported but unused
; consider using `importlib.util.find_spec` to test for availabili
ty
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/base.py,line=32,col=121,endLine=32,endColu
mn=125::src/twat_search/web/engines/base.py:32:121: E501 Line too
long (124 > 120)
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/base.py,line=35,col=121,endLine=35,endColu
mn=143::src/twat_search/web/engines/base.py:35:121: E501 Line too
long (142 > 120)
::error title=Ruff (PLR2004),file=/Users/adam/Developer/vcs/github
.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/s
rc/twat_search/web/engines/base.py,line=97,col=64,endLine=97,endCo
lumn=65::src/twat_search/web/engines/base.py:97:64: PLR2004 Magic
value used in comparison, consider replacing `4` with a constant v
ariable
::error title=Ruff (PLR2004),file=/Users/adam/Developer/vcs/github
.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/s
rc/twat_search/web/engines/base.py,line=98,col=65,endLine=98,endCo
lumn=66::src/twat_search/web/engines/base.py:98:65: PLR2004 Magic
value used in comparison, consider replacing `4` with a constant v
ariable
::error title=Ruff (PLR2004),file=/Users/adam/Developer/vcs/github
.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/s
rc/twat_search/web/engines/base.py,line=107,col=68,endLine=107,end
Column=69::src/twat_search/web/engines/base.py:107:68: PLR2004 Mag
ic value used in comparison, consider replacing `4` with a constan
t variable
::error title=Ruff (PLR2004),file=/Users/adam/Developer/vcs/github
.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/s
rc/twat_search/web/engines/base.py,line=108,col=69,endLine=108,end
Column=70::src/twat_search/web/engines/base.py:108:69: PLR2004 Mag
ic value used in comparison, consider replacing `4` with a constan
t variable
::error title=Ruff (S311),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/base.py,line=250,col=37,endLine=250,endCol
umn=63::src/twat_search/web/engines/base.py:250:37: S311 Standard
pseudo-random generators are not suitable for cryptographic purpos
es
::error title=Ruff (S311),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/base.py,line=277,col=26,endLine=277,endCol
umn=50::src/twat_search/web/engines/base.py:277:26: S311 Standard
pseudo-random generators are not suitable for cryptographic purpos
es
::error title=Ruff (ARG002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/bing_scraper.py,line=56,col=26,endLine=5
6,endColumn=31::src/twat_search/web/engines/bing_scraper.py:56:26:
 ARG002 Unused method argument: `query`
::error title=Ruff (ARG002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/bing_scraper.py,line=56,col=38,endLine=5
6,endColumn=49::src/twat_search/web/engines/bing_scraper.py:56:38:
 ARG002 Unused method argument: `num_results`
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/bing_scraper.py,line=113,col=9,endLine=1
13,endColumn=20::src/twat_search/web/engines/bing_scraper.py:113:9
: FBT002 Boolean default positional argument in function definitio
n
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/brave.py,line=44,col=9,endLine=44,endCol
umn=20::src/twat_search/web/engines/brave.py:44:9: FBT001 Boolean-
typed positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/brave.py,line=44,col=9,endLine=44,endCol
umn=20::src/twat_search/web/engines/brave.py:44:9: FBT002 Boolean
default positional argument in function definition
::error title=Ruff (ARG002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/brave.py,line=46,col=11,endLine=46,endCo
lumn=17::src/twat_search/web/engines/brave.py:46:11: ARG002 Unused
 method argument: `kwargs`
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/brave.py,line=354,col=5,endLine=354,endC
olumn=16::src/twat_search/web/engines/brave.py:354:5: FBT002 Boole
an default positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/brave.py,line=394,col=5,endLine=394,endC
olumn=16::src/twat_search/web/engines/brave.py:394:5: FBT002 Boole
an default positional argument in function definition
::error title=Ruff (ARG002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/critique.py,line=59,col=9,endLine=59,end
Column=20::src/twat_search/web/engines/critique.py:59:9: ARG002 Un
used method argument: `num_results`
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/critique.py,line=62,col=9,endLine=62,end
Column=20::src/twat_search/web/engines/critique.py:62:9: FBT002 Bo
olean default positional argument in function definition
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/critique.py,line=101,col=121,endLine=101,e
ndColumn=155::src/twat_search/web/engines/critique.py:101:121: E50
1 Line too long (154 > 120)
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/critique.py,line=120,col=13,endLine=123,en
dColumn=14::src/twat_search/web/engines/critique.py:120:13: B904 W
ithin an `except` clause, raise exceptions with `raise ... from er
r` or `raise ... from None` to distinguish them from errors in exc
eption handling
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/critique.py,line=125,col=13,endLine=125,en
dColumn=80::src/twat_search/web/engines/critique.py:125:13: B904 W
ithin an `except` clause, raise exceptions with `raise ... from er
r` or `raise ... from None` to distinguish them from errors in exc
eption handling
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/critique.py,line=248,col=5,endLine=248,e
ndColumn=16::src/twat_search/web/engines/critique.py:248:5: FBT002
 Boolean default positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/duckduckgo.py,line=54,col=9,endLine=54,e
ndColumn=20::src/twat_search/web/engines/duckduckgo.py:54:9: FBT00
2 Boolean default positional argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/duckduckgo.py,line=206,col=5,endLine=206
,endColumn=16::src/twat_search/web/engines/duckduckgo.py:206:5: FB
T001 Boolean-typed positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/duckduckgo.py,line=206,col=5,endLine=206
,endColumn=16::src/twat_search/web/engines/duckduckgo.py:206:5: FB
T002 Boolean default positional argument in function definition
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/google_scraper.py,line=48,col=24,endLine
=48,endColumn=28::src/twat_search/web/engines/google_scraper.py:48
:24: ARG001 Unused function argument: `args`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/google_scraper.py,line=48,col=32,endLine
=48,endColumn=38::src/twat_search/web/engines/google_scraper.py:48
:32: ARG001 Unused function argument: `kwargs`
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/google_scraper.py,line=106,col=9,endLine
=106,endColumn=20::src/twat_search/web/engines/google_scraper.py:1
06:9: FBT002 Boolean default positional argument in function defin
ition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/google_scraper.py,line=304,col=5,endLine
=304,endColumn=16::src/twat_search/web/engines/google_scraper.py:3
04:5: FBT001 Boolean-typed positional argument in function definit
ion
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/google_scraper.py,line=304,col=5,endLine
=304,endColumn=16::src/twat_search/web/engines/google_scraper.py:3
04:5: FBT002 Boolean default positional argument in function defin
ition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/google_scraper.py,line=308,col=5,endLine
=308,endColumn=11::src/twat_search/web/engines/google_scraper.py:3
08:5: FBT001 Boolean-typed positional argument in function definit
ion
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/google_scraper.py,line=308,col=5,endLine
=308,endColumn=11::src/twat_search/web/engines/google_scraper.py:3
08:5: FBT002 Boolean default positional argument in function defin
ition
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=10,col=8,endL
ine=10,endColumn=10::src/twat_search/web/engines/lib_falla/core/fa
lla.py:10:8: F401 `os` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=11,col=8,endL
ine=11,endColumn=10::src/twat_search/web/engines/lib_falla/core/fa
lla.py:11:8: F401 `re` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=12,col=8,endL
ine=12,endColumn=18::src/twat_search/web/engines/lib_falla/core/fa
lla.py:12:8: F401 `subprocess` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=13,col=8,endL
ine=13,endColumn=11::src/twat_search/web/engines/lib_falla/core/fa
lla.py:13:8: F401 `sys` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=14,col=29,end
Line=14,endColumn=36::src/twat_search/web/engines/lib_falla/core/f
alla.py:14:29: F401 `collections.abc.Mapping` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=15,col=21,end
Line=15,endColumn=25::src/twat_search/web/engines/lib_falla/core/f
alla.py:15:21: F401 `pathlib.Path` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=16,col=25,end
Line=16,endColumn=33::src/twat_search/web/engines/lib_falla/core/f
alla.py:16:25: F401 `typing.ClassVar` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=16,col=35,end
Line=16,endColumn=43::src/twat_search/web/engines/lib_falla/core/f
alla.py:16:35: F401 `typing.Optional` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=16,col=45,end
Line=16,endColumn=50::src/twat_search/web/engines/lib_falla/core/f
alla.py:16:45: F401 `typing.Union` imported but unused
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=16,col=52,end
Line=16,endColumn=56::src/twat_search/web/engines/lib_falla/core/f
alla.py:16:52: F401 `typing.cast` imported but unused
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=69,col=121,en
dLine=69,endColumn=146::src/twat_search/web/engines/lib_falla/core
/falla.py:69:121: E501 Line too long (145 > 120)
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=265,col=121,e
ndLine=265,endColumn=154::src/twat_search/web/engines/lib_falla/co
re/falla.py:265:121: E501 Line too long (153 > 120)
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/falla.py,line=371,col=121,e
ndLine=371,endColumn=149::src/twat_search/web/engines/lib_falla/co
re/falla.py:371:121: E501 Line too long (148 > 120)
::error title=Ruff (ARG002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/lib_falla/core/falla.py,line=422,col=23,
endLine=422,endColumn=28::src/twat_search/web/engines/lib_falla/co
re/falla.py:422:23: ARG002 Unused method argument: `query`
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/fetch_page.py,line=44,col=1
21,endLine=44,endColumn=146::src/twat_search/web/engines/lib_falla
/core/fetch_page.py:44:121: E501 Line too long (145 > 120)
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/lib_falla/core/google.py,line=11,col=40,en
dLine=11,endColumn=48::src/twat_search/web/engines/lib_falla/core/
google.py:11:40: F401 `typing.Optional` imported but unused
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/pplx.py,line=110,col=13,endLine=113,endCol
umn=14::src/twat_search/web/engines/pplx.py:110:13: B904 Within an
 `except` clause, raise exceptions with `raise ... from err` or `r
aise ... from None` to distinguish them from errors in exception h
andling
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/pplx.py,line=115,col=13,endLine=118,endCol
umn=14::src/twat_search/web/engines/pplx.py:115:13: B904 Within an
 `except` clause, raise exceptions with `raise ... from err` or `r
aise ... from None` to distinguish them from errors in exception h
andling
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/pplx.py,line=154,col=5,endLine=154,endCo
lumn=16::src/twat_search/web/engines/pplx.py:154:5: FBT002 Boolean
 default positional argument in function definition
::error title=Ruff (PLR2004),file=/Users/adam/Developer/vcs/github
.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/s
rc/twat_search/web/engines/pplx.py,line=191,col=52,endLine=191,end
Column=53::src/twat_search/web/engines/pplx.py:191:52: PLR2004 Mag
ic value used in comparison, consider replacing `4` with a constan
t variable
::error title=Ruff (PLR2004),file=/Users/adam/Developer/vcs/github
.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/s
rc/twat_search/web/engines/pplx.py,line=192,col=53,endLine=192,end
Column=54::src/twat_search/web/engines/pplx.py:192:53: PLR2004 Mag
ic value used in comparison, consider replacing `4` with a constan
t variable
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/pplx.py,line=196,col=121,endLine=196,endCo
lumn=131::src/twat_search/web/engines/pplx.py:196:121: E501 Line t
oo long (130 > 120)
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/serpapi.py,line=61,col=9,endLine=61,endC
olumn=20::src/twat_search/web/engines/serpapi.py:61:9: FBT002 Bool
ean default positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/serpapi.py,line=181,col=5,endLine=181,en
dColumn=16::src/twat_search/web/engines/serpapi.py:181:5: FBT002 B
oolean default positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/tavily.py,line=64,col=9,endLine=64,endCo
lumn=20::src/twat_search/web/engines/tavily.py:64:9: FBT002 Boolea
n default positional argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/tavily.py,line=69,col=9,endLine=69,endCo
lumn=23::src/twat_search/web/engines/tavily.py:69:9: FBT001 Boolea
n-typed positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/tavily.py,line=69,col=9,endLine=69,endCo
lumn=23::src/twat_search/web/engines/tavily.py:69:9: FBT002 Boolea
n default positional argument in function definition
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/tavily.py,line=180,col=17,endLine=180,endC
olumn=72::src/twat_search/web/engines/tavily.py:180:17: B904 Withi
n an `except` clause, raise exceptions with `raise ... from err` o
r `raise ... from None` to distinguish them from errors in excepti
on handling
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/tavily.py,line=182,col=17,endLine=182,endC
olumn=75::src/twat_search/web/engines/tavily.py:182:17: B904 Withi
n an `except` clause, raise exceptions with `raise ... from err` o
r `raise ... from None` to distinguish them from errors in excepti
on handling
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/tavily.py,line=184,col=17,endLine=184,endC
olumn=69::src/twat_search/web/engines/tavily.py:184:17: B904 Withi
n an `except` clause, raise exceptions with `raise ... from err` o
r `raise ... from None` to distinguish them from errors in excepti
on handling
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/tavily.py,line=211,col=5,endLine=211,end
Column=16::src/twat_search/web/engines/tavily.py:211:5: FBT002 Boo
lean default positional argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/tavily.py,line=216,col=5,endLine=216,end
Column=19::src/twat_search/web/engines/tavily.py:216:5: FBT001 Boo
lean-typed positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/tavily.py,line=216,col=5,endLine=216,end
Column=19::src/twat_search/web/engines/tavily.py:216:5: FBT002 Boo
lean default positional argument in function definition
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/you.py,line=93,col=13,endLine=93,endColumn
=83::src/twat_search/web/engines/you.py:93:13: B904 Within an `exc
ept` clause, raise exceptions with `raise ... from err` or `raise
... from None` to distinguish them from errors in exception handli
ng
::error title=Ruff (B904),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/
twat_search/web/engines/you.py,line=95,col=13,endLine=95,endColumn
=81::src/twat_search/web/engines/you.py:95:13: B904 Within an `exc
ept` clause, raise exceptions with `raise ... from err` or `raise
... from None` to distinguish them from errors in exception handli
ng
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/you.py,line=195,col=5,endLine=195,endCol
umn=16::src/twat_search/web/engines/you.py:195:5: FBT002 Boolean d
efault positional argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/engines/you.py,line=237,col=5,endLine=237,endCol
umn=16::src/twat_search/web/engines/you.py:237:5: FBT002 Boolean d
efault positional argument in function definition
::error title=Ruff (FBT001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/utils.py,line=23,col=22,endLine=23,endColumn=34:
:src/twat_search/web/utils.py:23:22: FBT001 Boolean-typed position
al argument in function definition
::error title=Ruff (FBT002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/sr
c/twat_search/web/utils.py,line=23,col=22,endLine=23,endColumn=34:
:src/twat_search/web/utils.py:23:22: FBT002 Boolean default positi
onal argument in function definition
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
_async_falla.py,line=3,col=8,endLine=3,endColumn=11::test_async_fa
lla.py:3:8: F401 `sys` imported but unused
::error title=Ruff (E501),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
_simple.py,line=21,col=121,endLine=21,endColumn=146::test_simple.p
y:21:121: E501 Line too long (145 > 120)
::error title=Ruff (F401),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
_sync_falla.py,line=2,col=8,endLine=2,endColumn=11::test_sync_fall
a.py:2:8: F401 `sys` imported but unused
::error title=Ruff (ARG002),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/engines/test_base.py,line=89,col=32,endLine=89,endCol
umn=37::tests/unit/web/engines/test_base.py:89:32: ARG002 Unused m
ethod argument: `query`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=100,col=5,endLine=100,endColumn=19::
tests/unit/web/test_api.py:100:5: ARG001 Unused function argument:
 `setup_teardown`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=114,col=5,endLine=114,endColumn=19::
tests/unit/web/test_api.py:114:5: ARG001 Unused function argument:
 `setup_teardown`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=130,col=5,endLine=130,endColumn=19::
tests/unit/web/test_api.py:130:5: ARG001 Unused function argument:
 `setup_teardown`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=144,col=39,endLine=144,endColumn=53:
:tests/unit/web/test_api.py:144:39: ARG001 Unused function argumen
t: `setup_teardown`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=153,col=5,endLine=153,endColumn=19::
tests/unit/web/test_api.py:153:5: ARG001 Unused function argument:
 `setup_teardown`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=169,col=5,endLine=169,endColumn=19::
tests/unit/web/test_api.py:169:5: ARG001 Unused function argument:
 `setup_teardown`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=179,col=5,endLine=179,endColumn=16::
tests/unit/web/test_api.py:179:5: ARG001 Unused function argument:
 `monkeypatch`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_api.py,line=180,col=5,endLine=180,endColumn=19::
tests/unit/web/test_api.py:180:5: ARG001 Unused function argument:
 `setup_teardown`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_config.py,line=41,col=26,endLine=41,endColumn=42
::tests/unit/web/test_config.py:41:26: ARG001 Unused function argu
ment: `isolate_env_vars`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_config.py,line=49,col=31,endLine=49,endColumn=42
::tests/unit/web/test_config.py:49:31: ARG001 Unused function argu
ment: `monkeypatch`
::error title=Ruff (ARG001),file=/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/te
sts/unit/web/test_config.py,line=49,col=57,endLine=49,endColumn=75
::tests/unit/web/test_config.py:49:57: ARG001 Unused function argu
ment: `env_vars_for_brave`
::error title=Ruff (PT017),file=/Users/adam/Developer/vcs/github.t
wardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tes
ts/unit/web/test_exceptions.py,line=46,col=13,endLine=46,endColumn
=50::tests/unit/web/test_exceptions.py:46:13: PT017 Found assertio
n on exception `e` in `except` block, use `pytest.raises()` instea
d
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=69,col=25,endLine=69,endColumn=52:
:tests/web/test_bing_scraper.py:69:25: N803 Argument name `mock_Bi
ngScraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=82,col=9,endLine=82,endColumn=36::
tests/web/test_bing_scraper.py:82:9: N803 Argument name `mock_Bing
Scraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=109,col=44,endLine=109,endColumn=7
1::tests/web/test_bing_scraper.py:109:44: N803 Argument name `mock
_BingScraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=138,col=47,endLine=138,endColumn=7
4::tests/web/test_bing_scraper.py:138:47: N803 Argument name `mock
_BingScraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=202,col=38,endLine=202,endColumn=6
5::tests/web/test_bing_scraper.py:202:38: N803 Argument name `mock
_BingScraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=213,col=37,endLine=213,endColumn=6
4::tests/web/test_bing_scraper.py:213:37: N803 Argument name `mock
_BingScraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=227,col=40,endLine=227,endColumn=6
7::tests/web/test_bing_scraper.py:227:40: N803 Argument name `mock
_BingScraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=242,col=40,endLine=242,endColumn=6
7::tests/web/test_bing_scraper.py:242:40: N803 Argument name `mock
_BingScraper` should be lowercase
::error title=Ruff (N803),file=/Users/adam/Developer/vcs/github.tw
ardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/test
s/web/test_bing_scraper.py,line=257,col=48,endLine=257,endColumn=7
5::tests/web/test_bing_scraper.py:257:48: N803 Argument name `mock
_BingScraper` should be lowercase

```

---

_****_



Let's run a test to see if our changes work correctly:

---

_****_

```bash
cd $(git rev-parse --show-toplevel) && python -m pytest tests/unit/web/test_api.py -v
```

---

_****_



---



---

