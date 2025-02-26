## SpecStory

## Search Engine Initialization Errors (26/02/2025, 13:40:27)

_**User**_

>>> bing_anyws
[02/26/25 13:37:29] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['bing_anyws']                                                                              cli.py:168
                    INFO     🔍 Querying engine: bing_anyws                                                                                                  api.py:74
                    INFO     Searching Bing (anywebsearch) with query: 'FontLab review'                                                            anywebsearch.py:366
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:367
                    ERROR    Error during Bing (anywebsearch) search: Invalid search engine name:                                                  anywebsearch.py:407
                    ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158
No results found!
>>> bing_scraper
[02/26/25 13:37:30] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['bing_scraper']                                                                            cli.py:168
                    DEBUG    Parameters safe_search=True set but not used by Bing Scraper                                                          bing_scraper.py:151
                    INFO     🔍 Querying engine: bing_scraper                                                                                                api.py:74
                    INFO     Searching Bing with query: 'FontLab review'                                                                           bing_scraper.py:227
                    DEBUG    Using max_results=5, max_retries=3, delay=1.0                                                                         bing_scraper.py:228
⠹ Searching for 'FontLab review'...                    INFO     No results returned from Bing Scraper                                                                                 bing_scraper.py:243
                    INFO     ✅ Engine 'bing_scraper' returned 0 results                                                                                    api.py:160
No results found!
>>> bing_searchit
[02/26/25 13:37:32] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['bing_searchit']                                                                           cli.py:168
                    ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> brave
[02/26/25 13:37:33] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['brave']                                                                                   cli.py:168
                    INFO     🔍 Querying engine: brave                                                                                                       api.py:74
⠋ Searching for 'FontLab review'...                    DEBUG    connect_tcp.started host='api.search.brave.com' port=443 local_address=None timeout=10 socket_options=None                   _trace.py:87
                    DEBUG    connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x1081db800>                               _trace.py:87
                    DEBUG    start_tls.started ssl_context=<ssl.SSLContext object at 0x1058090d0> server_hostname='api.search.brave.com' timeout=10       _trace.py:87
⠼ Searching for 'FontLab review'...                    DEBUG    start_tls.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x10381f560>                                 _trace.py:87
                    DEBUG    send_request_headers.started request=<Request [b'GET']>                                                                      _trace.py:87
                    DEBUG    send_request_headers.complete                                                                                                _trace.py:87
                    DEBUG    send_request_body.started request=<Request [b'GET']>                                                                         _trace.py:87
                    DEBUG    send_request_body.complete                                                                                                   _trace.py:87
                    DEBUG    receive_response_headers.started request=<Request [b'GET']>                                                                  _trace.py:87
⠧ Searching for 'FontLab review'...                    DEBUG    receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Wed, 26 Feb 2025 12:37:34 GMT'),       _trace.py:87
                             (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'),                              
                             (b'x-ratelimit-limit', b'1, 2000'), (b'x-ratelimit-policy', b'1;w=1, 2000;w=2419200,'), (b'x-ratelimit-remaining', b'0,                  
                             1913'), (b'x-ratelimit-reset', b'1, 213745'), (b'server-timing', b'search-roundtrip;dur=78.915'), (b'content-encoding',                  
                             b'gzip'), (b'vary', b'Accept-Encoding'), (b'Vary', b'Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, Sec-Fetch-User'),                   
                             (b'X-Content-Type-Options', b'nosniff'), (b'Referrer-Policy', b'strict-origin-when-cross-origin'),                                       
                             (b'Strict-Transport-Security', b'max-age=31536000; includeSubDomains; preload'), (b'X-Download-Options', b'noopen'),                     
                             (b'X-Frame-Options', b'SAMEORIGIN'), (b'X-XSS-Protection', b'1; mode=block')])                                                           
                    INFO     HTTP Request: GET https://api.search.brave.com/res/v1/web/search?q=FontLab+review&count=5&country=US&safe_search=strict   _client.py:1740
                             "HTTP/1.1 200 OK"                                                                                                                        
                    DEBUG    receive_response_body.started request=<Request [b'GET']>                                                                     _trace.py:87
                    DEBUG    receive_response_body.complete                                                                                               _trace.py:87
                    DEBUG    response_closed.started                                                                                                      _trace.py:87
                    DEBUG    response_closed.complete                                                                                                     _trace.py:87
                    DEBUG    close.started                                                                                                                _trace.py:87
                    DEBUG    close.complete                                                                                                               _trace.py:87
                    INFO     ✅ Engine 'brave' returned 5 results                                                                                           api.py:160
┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Engine ┃ Status     ┃ Title                                                                 ┃ URL                                                                  ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ brave  │ ✅ Success │ Review: FontLab 7 — Alex John Lucas a Typeface Designer               │ https://alexjohnlucas.com/type/fontlab-7                             │
│        │ ✅ Success │ FontLab VI and 7 Reviews                                              │ https://help.fontlab.com/fontlab/7/manual/FontLab-Reviews/           │
│        │ ✅ Success │ r/typedesign on Reddit: I hate FontLab                                │ https://www.reddit.com/r/typedesign/comments/uzpyqa/i_hate_fontlab/  │
│        │ ✅ Success │ Which is better to create true type fonts, Fontlab or Fontographer? - │ https://www.quora.com/Which-is-better-to-create-true-type-fonts-Font │
│        │            │ Quora                                                                 │ lab-or-Fontographer                                                  │
│        │ ✅ Success │ FontLab 8.4.3 Build 8984 - Download, Review, Screenshots              │ https://www.softpedia.com/get/Others/Font-Utils/FontLab-Studio.shtml │
└────────┴────────────┴───────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────┘
{
    'engine': 'brave',
    'status': '✅ Success',
    'url': 'https://alexjohnlucas.com/type/fontlab-7',
    'title': 'Review: FontLab 7 — Alex John Lucas a Typeface Designer',
(...
)}
>>> brave_anyws
[02/26/25 13:37:35] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['brave_anyws']                                                                             cli.py:168
                    INFO     🔍 Querying engine: brave_anyws                                                                                                 api.py:74
                    ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158
No results found!
>>> brave_news
[02/26/25 13:37:36] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['brave_news']                                                                              cli.py:168
                    ERROR    Error initializing engine 'brave_news': Engine 'brave_news': Brave API key is required. Set it via one of these env vars:       api.py:82
                             BRAVE_API_KEY                                                                                                                            
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> critique
[02/26/25 13:37:37] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['critique']                                                                                cli.py:168
                    ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> duckduckgo
[02/26/25 13:37:38] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['duckduckgo']                                                                              cli.py:168
                    INFO     🔍 Querying engine: duckduckgo                                                                                                  api.py:74
                    DEBUG    Loaded CA certs                                                                                                               utils.rs:31
                    DEBUG    starting new connection: https://html.duckduckgo.com/                                                                      connect.rs:381
                    DEBUG    resolving html.duckduckgo.com                                                                                                  dns.rs:126
                    DEBUG    connecting to 52.142.124.215:443                                                                                              http.rs:730
                    DEBUG    connected to 52.142.124.215:443                                                                                               http.rs:733
⠋ Searching for 'FontLab review'...                    DEBUG    pooling idle connection for PoolKey { uri: https://html.duckduckgo.com/, alpn_protos: None, network: default }                pool.rs:380
⠏ Searching for 'FontLab review'...[02/26/25 13:37:39] DEBUG    inserting secure cookie 'kl'                                                                                           cookie_store.rs:82
                    INFO     response: https://html.duckduckgo.com/html 200                                                                                 lib.rs:450
                    DEBUG    _get_url() https://html.duckduckgo.com/html 200                                                                  duckduckgo_search.py:150
                    ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158
No results found!
>>> google_anyws
[02/26/25 13:37:40] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['google_anyws']                                                                            cli.py:168
                    INFO     🔍 Querying engine: google_anyws                                                                                                api.py:74
                    INFO     Searching Google (anywebsearch) with query: 'FontLab review'                                                          anywebsearch.py:291
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:292
                    DEBUG    Starting new HTTPS connection (1): www.google.com:443                                                              connectionpool.py:1049
⠼ Searching for 'FontLab review'...                    DEBUG    https://www.google.com:443 "GET /search?q=FontLab+review&num=8&hl=en&start=0&safe=active HTTP/1.1" 200 None         connectionpool.py:544
⠦ Searching for 'FontLab review'...[02/26/25 13:37:41] DEBUG    Received 5 raw results from Google (anywebsearch)                                                                     anywebsearch.py:312
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='alexjohnlucas.com/type/fontlab-7/', input_type=str]                                                                         
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='reddit.com/r/typedesign/.../uzpyqa/i_hate_fontlab/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='help.fontlab.com/fontlab...reference/testimonials/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='quora.com/Which-software...-use-FontLab-or-Glyphs/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='help.fontlab.com/fontlab...manual/FontLab-Reviews/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    INFO     Returning 0 validated results from Google (anywebsearch)                                                              anywebsearch.py:325
                    INFO     ✅ Engine 'google_anyws' returned 0 results                                                                                    api.py:160
No results found!
>>> google_hasdata
[02/26/25 13:37:42] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    WARNING  Engine 'google_hasdata' is not available. The dependency may not be installed.                                                 cli.py:161
                    DEBUG    Attempting to search with engines: None                                                                                        cli.py:168
                    INFO     🔍 Querying engine: brave                                                                                                       api.py:74
                    ERROR    Error initializing engine 'brave_news': Engine 'brave_news': Brave API key is required. Set it via one of these env vars:       api.py:82
                             BRAVE_API_KEY                                                                                                                            
                    INFO     🔍 Querying engine: brave_anyws                                                                                                 api.py:74
                    ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82
                    INFO     🔍 Querying engine: google_anyws                                                                                                api.py:74
                    INFO     🔍 Querying engine: google_scraper                                                                                              api.py:74
                    ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82
                    INFO     🔍 Querying engine: tavily                                                                                                      api.py:74
                    ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82
                    ERROR    Error initializing engine 'you': Engine 'you': You.com API key is required. Set it via one of these env vars: YOU_API_KEY       api.py:82
                    ERROR    Error initializing engine 'you_news': Engine 'you_news': You.com API key is required. Set it via one of these env vars:         api.py:82
                             YOU_API_KEY                                                                                                                              
                    ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82
                    INFO     🔍 Querying engine: duckduckgo                                                                                                  api.py:74
                    DEBUG    Parameters safe_search=True set but not used by Bing Scraper                                                          bing_scraper.py:151
                    INFO     🔍 Querying engine: bing_scraper                                                                                                api.py:74
                    INFO     🔍 Querying engine: bing_anyws                                                                                                  api.py:74
                    ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82
                    INFO     🔍 Querying engine: qwant_anyws                                                                                                 api.py:74
                    ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82
                    INFO     🔍 Querying engine: yandex_anyws                                                                                                api.py:74
                    ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82
                    ERROR    Error initializing engine 'google_hasdata_full': Engine 'google_hasdata_full': HasData API key is required. Set it via one of   api.py:82
                             these env vars: HASDATA_API_KEY                                                                                                          
                    ERROR    Error initializing engine 'google_hasdata': Engine 'google_hasdata': HasData API key is required. Set it via one of these env   api.py:82
                             vars: HASDATA_API_KEY                                                                                                                    
⠋ Searching for 'FontLab review'...                    INFO     Searching Google (anywebsearch) with query: 'FontLab review'                                                          anywebsearch.py:291
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:292
                    DEBUG    Starting new HTTPS connection (1): www.google.com:443                                                              connectionpool.py:1049
⠧ Searching for 'FontLab review'...                    DEBUG    https://www.google.com:443 "GET /search?q=FontLab+review&num=8&hl=en&start=0&safe=active HTTP/1.1" 200 None         connectionpool.py:544
                    DEBUG    Received 5 raw results from Google (anywebsearch)                                                                     anywebsearch.py:312
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='alexjohnlucas.com/type/fontlab-7/', input_type=str]                                                                         
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='reddit.com/r/typedesign/.../uzpyqa/i_hate_fontlab/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='help.fontlab.com/fontlab...reference/testimonials/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='quora.com/Which-software...-use-FontLab-or-Glyphs/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='help.fontlab.com/fontlab...manual/FontLab-Reviews/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    INFO     Returning 0 validated results from Google (anywebsearch)                                                              anywebsearch.py:325
                    INFO     Searching Google with query: 'FontLab review'                                                                       google_scraper.py:235
                    DEBUG    Using max_results=5, language=en, region=us, safe=active, sleep_interval=0.0, ssl_verify=True, proxy=None,          google_scraper.py:236
                             unique=True                                                                                                                              
                    DEBUG    Starting new HTTPS connection (1): www.google.com:443                                                              connectionpool.py:1049
⠸ Searching for 'FontLab review'...[02/26/25 13:37:43] DEBUG    https://www.google.com:443 "GET /search?q=FontLab+review&num=7&hl=en&start=0&safe=active&gl=us HTTP/1.1" 200 None   connectionpool.py:544
⠴ Searching for 'FontLab review'...                    DEBUG    Received 5 raw results from Google Scraper                                                                          google_scraper.py:263
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    INFO     Returning 0 validated results from Google Scraper                                                                   google_scraper.py:292
                    DEBUG    Loaded CA certs                                                                                                               utils.rs:31
                    DEBUG    starting new connection: https://html.duckduckgo.com/                                                                      connect.rs:381
                    DEBUG    resolving html.duckduckgo.com                                                                                                  dns.rs:126
                    DEBUG    connecting to 52.142.124.215:443                                                                                              http.rs:730
⠦ Searching for 'FontLab review'...                    DEBUG    connected to 52.142.124.215:443                                                                                               http.rs:733
⠧ Searching for 'FontLab review'...                    DEBUG    pooling idle connection for PoolKey { uri: https://html.duckduckgo.com/, alpn_protos: None, network: default }                pool.rs:380
⠇ Searching for 'FontLab review'...[02/26/25 13:37:44] DEBUG    inserting secure cookie 'kl'                                                                                           cookie_store.rs:82
                    INFO     response: https://html.duckduckgo.com/html 200                                                                                 lib.rs:450
                    DEBUG    _get_url() https://html.duckduckgo.com/html 200                                                                  duckduckgo_search.py:150
                    INFO     Searching Bing with query: 'FontLab review'                                                                           bing_scraper.py:227
                    DEBUG    Using max_results=5, max_retries=3, delay=1.0                                                                         bing_scraper.py:228
⠙ Searching for 'FontLab review'...                    INFO     No results returned from Bing Scraper                                                                                 bing_scraper.py:243
                    INFO     Searching Bing (anywebsearch) with query: 'FontLab review'                                                            anywebsearch.py:366
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:367
                    ERROR    Error during Bing (anywebsearch) search: Invalid search engine name:                                                  anywebsearch.py:407
                    INFO     Searching Qwant (anywebsearch) with query: 'FontLab review'                                                           anywebsearch.py:521
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:522
                    ERROR    Error during Qwant (anywebsearch) search: Invalid search engine name:                                                 anywebsearch.py:562
                    DEBUG    connect_tcp.started host='api.search.brave.com' port=443 local_address=None timeout=10 socket_options=None                   _trace.py:87
                    DEBUG    connect_tcp.started host='api.tavily.com' port=443 local_address=None timeout=10 socket_options=None                         _trace.py:87
                    DEBUG    connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x10a5773e0>                               _trace.py:87
                    DEBUG    start_tls.started ssl_context=<ssl.SSLContext object at 0x107a998d0> server_hostname='api.search.brave.com' timeout=10       _trace.py:87
⠸ Searching for 'FontLab review'...                    DEBUG    connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x10a379a00>                               _trace.py:87
                    DEBUG    start_tls.started ssl_context=<ssl.SSLContext object at 0x10a5d3bd0> server_hostname='api.tavily.com' timeout=10             _trace.py:87
⠴ Searching for 'FontLab review'...[02/26/25 13:37:45] DEBUG    start_tls.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x106d8f620>                                 _trace.py:87
                    DEBUG    send_request_headers.started request=<Request [b'GET']>                                                                      _trace.py:87
                    DEBUG    send_request_headers.complete                                                                                                _trace.py:87
                    DEBUG    send_request_body.started request=<Request [b'GET']>                                                                         _trace.py:87
                    DEBUG    send_request_body.complete                                                                                                   _trace.py:87
                    DEBUG    receive_response_headers.started request=<Request [b'GET']>                                                                  _trace.py:87
                    DEBUG    start_tls.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x10a62fe90>                                 _trace.py:87
                    DEBUG    send_request_headers.started request=<Request [b'POST']>                                                                     _trace.py:87
                    DEBUG    send_request_headers.complete                                                                                                _trace.py:87
                    DEBUG    send_request_body.started request=<Request [b'POST']>                                                                        _trace.py:87
                    DEBUG    send_request_body.complete                                                                                                   _trace.py:87
                    DEBUG    receive_response_headers.started request=<Request [b'POST']>                                                                 _trace.py:87
⠏ Searching for 'FontLab review'...                    DEBUG    receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Wed, 26 Feb 2025 12:37:45 GMT'),       _trace.py:87
                             (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'),                              
                             (b'x-ratelimit-limit', b'1, 2000'), (b'x-ratelimit-policy', b'1;w=1, 2000;w=2419200,'), (b'x-ratelimit-remaining', b'0,                  
                             1912'), (b'x-ratelimit-reset', b'1, 213733'), (b'server-timing', b'search-roundtrip;dur=48.986'), (b'content-encoding',                  
                             b'gzip'), (b'vary', b'Accept-Encoding'), (b'Vary', b'Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, Sec-Fetch-User'),                   
                             (b'X-Content-Type-Options', b'nosniff'), (b'Referrer-Policy', b'strict-origin-when-cross-origin'),                                       
                             (b'Strict-Transport-Security', b'max-age=31536000; includeSubDomains; preload'), (b'X-Download-Options', b'noopen'),                     
                             (b'X-Frame-Options', b'SAMEORIGIN'), (b'X-XSS-Protection', b'1; mode=block')])                                                           
                    INFO     HTTP Request: GET https://api.search.brave.com/res/v1/web/search?q=FontLab+review&count=5&country=US&safe_search=strict   _client.py:1740
                             "HTTP/1.1 200 OK"                                                                                                                        
                    DEBUG    receive_response_body.started request=<Request [b'GET']>                                                                     _trace.py:87
                    DEBUG    receive_response_body.complete                                                                                               _trace.py:87
                    DEBUG    response_closed.started                                                                                                      _trace.py:87
                    DEBUG    response_closed.complete                                                                                                     _trace.py:87
                    DEBUG    close.started                                                                                                                _trace.py:87
                    DEBUG    close.complete                                                                                                               _trace.py:87
⠧ Searching for 'FontLab review'...[02/26/25 13:37:47] DEBUG    receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Wed, 26 Feb 2025 12:37:47 GMT'),       _trace.py:87
                             (b'Content-Type', b'application/json'), (b'Content-Length', b'2492'), (b'Connection', b'keep-alive'), (b'Server', b'nginx'),             
                             (b'content-security-policy', b"default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src                      
                             'self';base-uri 'self';form-action 'self'; require-trusted-types-for 'script'; upgrade-insecure-requests;"),                             
                             (b'Strict-Transport-Security', b'max-age=31536000 ; includeSubDomains'), (b'X-Content-Type-Options', b'nosniff'),                        
                             (b'X-Frame-Options', b'DENY')])                                                                                                          
                    INFO     HTTP Request: POST https://api.tavily.com/search "HTTP/1.1 200 OK"                                                        _client.py:1740
                    DEBUG    receive_response_body.started request=<Request [b'POST']>                                                                    _trace.py:87
                    DEBUG    receive_response_body.complete                                                                                               _trace.py:87
                    DEBUG    response_closed.started                                                                                                      _trace.py:87
                    DEBUG    response_closed.complete                                                                                                     _trace.py:87
                    DEBUG    close.started                                                                                                                _trace.py:87
                    DEBUG    close.complete                                                                                                               _trace.py:87
                    INFO     ✅ Engine 'brave' returned 5 results                                                                                           api.py:160
                    ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158
                    INFO     ✅ Engine 'google_anyws' returned 0 results                                                                                    api.py:160
                    INFO     ✅ Engine 'google_scraper' returned 0 results                                                                                  api.py:160
                    ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158
                    ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158
                    INFO     ✅ Engine 'bing_scraper' returned 0 results                                                                                    api.py:160
                    ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158
                    ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158
                    ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158
┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Engine ┃ Status     ┃ Title                                                                 ┃ URL                                                                  ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ brave  │ ✅ Success │ Review: FontLab 7 — Alex John Lucas a Typeface Designer               │ https://alexjohnlucas.com/type/fontlab-7                             │
│        │ ✅ Success │ FontLab VI and 7 Reviews                                              │ https://help.fontlab.com/fontlab/7/manual/FontLab-Reviews/           │
│        │ ✅ Success │ r/typedesign on Reddit: I hate FontLab                                │ https://www.reddit.com/r/typedesign/comments/uzpyqa/i_hate_fontlab/  │
│        │ ✅ Success │ Which is better to create true type fonts, Fontlab or Fontographer? - │ https://www.quora.com/Which-is-better-to-create-true-type-fonts-Font │
│        │            │ Quora                                                                 │ lab-or-Fontographer                                                  │
│        │ ✅ Success │ FontLab 8.4.3 Build 8984 - Download, Review, Screenshots              │ https://www.softpedia.com/get/Others/Font-Utils/FontLab-Studio.shtml │
└────────┴────────────┴───────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────┘
{
    'engine': 'brave',
    'status': '✅ Success',
    'url': 'https://alexjohnlucas.com/type/fontlab-7',
(...)
    }
>>> google_hasdata_full
[02/26/25 13:37:48] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    WARNING  Engine 'google_hasdata_full' is not available. The dependency may not be installed.                                            cli.py:161
                    DEBUG    Attempting to search with engines: None                                                                                        cli.py:168
                    INFO     🔍 Querying engine: brave                                                                                                       api.py:74
                    ERROR    Error initializing engine 'brave_news': Engine 'brave_news': Brave API key is required. Set it via one of these env vars:       api.py:82
                             BRAVE_API_KEY                                                                                                                            
                    INFO     🔍 Querying engine: brave_anyws                                                                                                 api.py:74
                    ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82
                    INFO     🔍 Querying engine: google_anyws                                                                                                api.py:74
                    INFO     🔍 Querying engine: google_scraper                                                                                              api.py:74
                    ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82
                    INFO     🔍 Querying engine: tavily                                                                                                      api.py:74
                    ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82
                    ERROR    Error initializing engine 'you': Engine 'you': You.com API key is required. Set it via one of these env vars: YOU_API_KEY       api.py:82
                    ERROR    Error initializing engine 'you_news': Engine 'you_news': You.com API key is required. Set it via one of these env vars:         api.py:82
                             YOU_API_KEY                                                                                                                              
                    ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82
                    INFO     🔍 Querying engine: duckduckgo                                                                                                  api.py:74
                    DEBUG    Parameters safe_search=True set but not used by Bing Scraper                                                          bing_scraper.py:151
                    INFO     🔍 Querying engine: bing_scraper                                                                                                api.py:74
                    INFO     🔍 Querying engine: bing_anyws                                                                                                  api.py:74
                    ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82
                    INFO     🔍 Querying engine: qwant_anyws                                                                                                 api.py:74
                    ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82
                    INFO     🔍 Querying engine: yandex_anyws                                                                                                api.py:74
                    ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82
                    ERROR    Error initializing engine 'google_hasdata_full': Engine 'google_hasdata_full': HasData API key is required. Set it via one of   api.py:82
                             these env vars: HASDATA_API_KEY                                                                                                          
                    ERROR    Error initializing engine 'google_hasdata': Engine 'google_hasdata': HasData API key is required. Set it via one of these env   api.py:82
                             vars: HASDATA_API_KEY                                                                                                                    
⠋ Searching for 'FontLab review'...                    INFO     Searching Google (anywebsearch) with query: 'FontLab review'                                                          anywebsearch.py:291
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:292
                    DEBUG    Starting new HTTPS connection (1): www.google.com:443                                                              connectionpool.py:1049
⠧ Searching for 'FontLab review'...[02/26/25 13:37:49] DEBUG    https://www.google.com:443 "GET /search?q=FontLab+review&num=8&hl=en&start=0&safe=active HTTP/1.1" 200 None         connectionpool.py:544
                    DEBUG    Received 5 raw results from Google (anywebsearch)                                                                     anywebsearch.py:312
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='alexjohnlucas.com/type/fontlab-7/', input_type=str]                                                                         
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='reddit.com/r/typedesign/.../uzpyqa/i_hate_fontlab/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='help.fontlab.com/fontlab...reference/testimonials/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='quora.com/Which-software...-use-FontLab-or-Glyphs/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    WARNING  Validation error for result: 1 validation error for AnyWebSearchResult                                                anywebsearch.py:228
                             url                                                                                                                                      
                               Input should be a valid URL, relative URL without a base [type=url_parsing,                                                            
                             input_value='help.fontlab.com/fontlab...manual/FontLab-Reviews/', input_type=str]                                                        
                                 For further information visit https://errors.pydantic.dev/2.10/v/url_parsing                                                         
                    INFO     Returning 0 validated results from Google (anywebsearch)                                                              anywebsearch.py:325
                    INFO     Searching Google with query: 'FontLab review'                                                                       google_scraper.py:235
                    DEBUG    Using max_results=5, language=en, region=us, safe=active, sleep_interval=0.0, ssl_verify=True, proxy=None,          google_scraper.py:236
                             unique=True                                                                                                                              
                    DEBUG    Starting new HTTPS connection (1): www.google.com:443                                                              connectionpool.py:1049
⠼ Searching for 'FontLab review'...                    DEBUG    https://www.google.com:443 "GET /search?q=FontLab+review&num=7&hl=en&start=0&safe=active&gl=us HTTP/1.1" 200 None   connectionpool.py:544
                    DEBUG    Received 5 raw results from Google Scraper                                                                          google_scraper.py:263
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    INFO     Returning 0 validated results from Google Scraper                                                                   google_scraper.py:292
[02/26/25 13:37:50] DEBUG    Loaded CA certs                                                                                                               utils.rs:31
                    DEBUG    starting new connection: https://html.duckduckgo.com/                                                                      connect.rs:381
                    DEBUG    resolving html.duckduckgo.com                                                                                                  dns.rs:126
                    DEBUG    connecting to 52.142.124.215:443                                                                                              http.rs:730
⠴ Searching for 'FontLab review'...                    DEBUG    connected to 52.142.124.215:443                                                                                               http.rs:733
⠦ Searching for 'FontLab review'...                    DEBUG    pooling idle connection for PoolKey { uri: https://html.duckduckgo.com/, alpn_protos: None, network: default }                pool.rs:380
⠇ Searching for 'FontLab review'...[02/26/25 13:37:51] DEBUG    inserting secure cookie 'kl'                                                                                           cookie_store.rs:82
                    INFO     response: https://html.duckduckgo.com/html 200                                                                                 lib.rs:450
                    DEBUG    _get_url() https://html.duckduckgo.com/html 200                                                                  duckduckgo_search.py:150
                    INFO     Searching Bing with query: 'FontLab review'                                                                           bing_scraper.py:227
                    DEBUG    Using max_results=5, max_retries=3, delay=1.0                                                                         bing_scraper.py:228
⠦ Searching for 'FontLab review'...                    INFO     No results returned from Bing Scraper                                                                                 bing_scraper.py:243
                    INFO     Searching Bing (anywebsearch) with query: 'FontLab review'                                                            anywebsearch.py:366
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:367
                    ERROR    Error during Bing (anywebsearch) search: Invalid search engine name:                                                  anywebsearch.py:407
                    INFO     Searching Qwant (anywebsearch) with query: 'FontLab review'                                                           anywebsearch.py:521
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:522
                    ERROR    Error during Qwant (anywebsearch) search: Invalid search engine name:                                                 anywebsearch.py:562
                    DEBUG    connect_tcp.started host='api.search.brave.com' port=443 local_address=None timeout=10 socket_options=None                   _trace.py:87
                    DEBUG    connect_tcp.started host='api.tavily.com' port=443 local_address=None timeout=10 socket_options=None                         _trace.py:87
                    DEBUG    connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x10c7d96d0>                               _trace.py:87
                    DEBUG    start_tls.started ssl_context=<ssl.SSLContext object at 0x10d4dd8d0> server_hostname='api.search.brave.com' timeout=10       _trace.py:87
⠇ Searching for 'FontLab review'...                    DEBUG    connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x11008fce0>                               _trace.py:87
                    DEBUG    start_tls.started ssl_context=<ssl.SSLContext object at 0x11001fbd0> server_hostname='api.tavily.com' timeout=10             _trace.py:87
⠸ Searching for 'FontLab review'...[02/26/25 13:37:52] DEBUG    start_tls.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x10ff44170>                                 _trace.py:87
                    DEBUG    send_request_headers.started request=<Request [b'GET']>                                                                      _trace.py:87
                    DEBUG    start_tls.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x11008fc20>                                 _trace.py:87
                    DEBUG    send_request_headers.complete                                                                                                _trace.py:87
                    DEBUG    send_request_body.started request=<Request [b'GET']>                                                                         _trace.py:87
                    DEBUG    send_request_body.complete                                                                                                   _trace.py:87
                    DEBUG    receive_response_headers.started request=<Request [b'GET']>                                                                  _trace.py:87
                    DEBUG    send_request_headers.started request=<Request [b'POST']>                                                                     _trace.py:87
                    DEBUG    send_request_headers.complete                                                                                                _trace.py:87
                    DEBUG    send_request_body.started request=<Request [b'POST']>                                                                        _trace.py:87
                    DEBUG    send_request_body.complete                                                                                                   _trace.py:87
                    DEBUG    receive_response_headers.started request=<Request [b'POST']>                                                                 _trace.py:87
⠴ Searching for 'FontLab review'...                    DEBUG    receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Wed, 26 Feb 2025 12:37:52 GMT'),       _trace.py:87
                             (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'),                              
                             (b'x-ratelimit-limit', b'1, 2000'), (b'x-ratelimit-policy', b'1;w=1, 2000;w=2419200,'), (b'x-ratelimit-remaining', b'0,                  
                             1911'), (b'x-ratelimit-reset', b'1, 213726'), (b'server-timing', b'search-roundtrip;dur=47.098'), (b'content-encoding',                  
                             b'gzip'), (b'vary', b'Accept-Encoding'), (b'Vary', b'Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, Sec-Fetch-User'),                   
                             (b'X-Content-Type-Options', b'nosniff'), (b'Referrer-Policy', b'strict-origin-when-cross-origin'),                                       
                             (b'Strict-Transport-Security', b'max-age=31536000; includeSubDomains; preload'), (b'X-Download-Options', b'noopen'),                     
                             (b'X-Frame-Options', b'SAMEORIGIN'), (b'X-XSS-Protection', b'1; mode=block')])                                                           
                    INFO     HTTP Request: GET https://api.search.brave.com/res/v1/web/search?q=FontLab+review&count=5&country=US&safe_search=strict   _client.py:1740
                             "HTTP/1.1 200 OK"                                                                                                                        
                    DEBUG    receive_response_body.started request=<Request [b'GET']>                                                                     _trace.py:87
                    DEBUG    receive_response_body.complete                                                                                               _trace.py:87
                    DEBUG    response_closed.started                                                                                                      _trace.py:87
                    DEBUG    response_closed.complete                                                                                                     _trace.py:87
                    DEBUG    close.started                                                                                                                _trace.py:87
                    DEBUG    close.complete                                                                                                               _trace.py:87
⠴ Searching for 'FontLab review'...[02/26/25 13:37:54] DEBUG    receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Wed, 26 Feb 2025 12:37:54 GMT'),       _trace.py:87
                             (b'Content-Type', b'application/json'), (b'Content-Length', b'2492'), (b'Connection', b'keep-alive'), (b'Server', b'nginx'),             
                             (b'content-security-policy', b"default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src                      
                             'self';base-uri 'self';form-action 'self'; require-trusted-types-for 'script'; upgrade-insecure-requests;"),                             
                             (b'Strict-Transport-Security', b'max-age=31536000 ; includeSubDomains'), (b'X-Content-Type-Options', b'nosniff'),                        
                             (b'X-Frame-Options', b'DENY')])                                                                                                          
                    INFO     HTTP Request: POST https://api.tavily.com/search "HTTP/1.1 200 OK"                                                        _client.py:1740
                    DEBUG    receive_response_body.started request=<Request [b'POST']>                                                                    _trace.py:87
                    DEBUG    receive_response_body.complete                                                                                               _trace.py:87
                    DEBUG    response_closed.started                                                                                                      _trace.py:87
                    DEBUG    response_closed.complete                                                                                                     _trace.py:87
                    DEBUG    close.started                                                                                                                _trace.py:87
                    DEBUG    close.complete                                                                                                               _trace.py:87
                    INFO     ✅ Engine 'brave' returned 5 results                                                                                           api.py:160
                    ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158
                    INFO     ✅ Engine 'google_anyws' returned 0 results                                                                                    api.py:160
                    INFO     ✅ Engine 'google_scraper' returned 0 results                                                                                  api.py:160
                    ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158
                    ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158
                    INFO     ✅ Engine 'bing_scraper' returned 0 results                                                                                    api.py:160
                    ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158
                    ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158
                    ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158
┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Engine ┃ Status     ┃ Title                                                                 ┃ URL                                                                  ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ brave  │ ✅ Success │ Review: FontLab 7 — Alex John Lucas a Typeface Designer               │ https://alexjohnlucas.com/type/fontlab-7                             │
│        │ ✅ Success │ FontLab VI and 7 Reviews                                              │ https://help.fontlab.com/fontlab/7/manual/FontLab-Reviews/           │
│        │ ✅ Success │ r/typedesign on Reddit: I hate FontLab                                │ https://www.reddit.com/r/typedesign/comments/uzpyqa/i_hate_fontlab/  │
│        │ ✅ Success │ Which is better to create true type fonts, Fontlab or Fontographer? - │ https://www.quora.com/Which-is-better-to-create-true-type-fonts-Font │
│        │            │ Quora                                                                 │ lab-or-Fontographer                                                  │
│        │ ✅ Success │ FontLab 8.4.3 Build 8984 - Download, Review, Screenshots              │ https://www.softpedia.com/get/Others/Font-Utils/FontLab-Studio.shtml │
└────────┴────────────┴───────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────┘
{
    'engine': 'brave',
    'status': '✅ Success',
    'url': 'https://alexjohnlucas.com/type/fontlab-7',
(...)
    }
>>> google_scraper
[02/26/25 13:37:55] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['google_scraper']                                                                          cli.py:168
                    INFO     🔍 Querying engine: google_scraper                                                                                              api.py:74
                    INFO     Searching Google with query: 'FontLab review'                                                                       google_scraper.py:235
                    DEBUG    Using max_results=5, language=en, region=us, safe=active, sleep_interval=0.0, ssl_verify=True, proxy=None,          google_scraper.py:236
                             unique=True                                                                                                                              
                    DEBUG    Starting new HTTPS connection (1): www.google.com:443                                                              connectionpool.py:1049
⠸ Searching for 'FontLab review'...                    DEBUG    https://www.google.com:443 "GET /search?q=FontLab+review&num=7&hl=en&start=0&safe=active&gl=us HTTP/1.1" 200 None   connectionpool.py:544
⠴ Searching for 'FontLab review'...                    DEBUG    Received 5 raw results from Google Scraper                                                                          google_scraper.py:263
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212
                    INFO     Returning 0 validated results from Google Scraper                                                                   google_scraper.py:292
                    INFO     ✅ Engine 'google_scraper' returned 0 results                                                                                  api.py:160
No results found!
>>> google_searchit
[02/26/25 13:37:56] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['google_searchit']                                                                         cli.py:168
                    ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> google_serpapi
[02/26/25 13:37:57] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['google_serpapi']                                                                          cli.py:168
                    ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> pplx
[02/26/25 13:37:58] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['pplx']                                                                                    cli.py:168
                    ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> qwant_anyws
[02/26/25 13:37:59] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['qwant_anyws']                                                                             cli.py:168
                    INFO     🔍 Querying engine: qwant_anyws                                                                                                 api.py:74
                    INFO     Searching Qwant (anywebsearch) with query: 'FontLab review'                                                           anywebsearch.py:521
                    DEBUG    Using max_results=5, language=en                                                                                      anywebsearch.py:522
                    ERROR    Error during Qwant (anywebsearch) search: Invalid search engine name:                                                 anywebsearch.py:562
                    ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158
No results found!
>>> qwant_searchit
[02/26/25 13:38:00] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['qwant_searchit']                                                                          cli.py:168
                    ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> tavily
[02/26/25 13:38:01] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['tavily']                                                                                  cli.py:168
                    INFO     🔍 Querying engine: tavily                                                                                                      api.py:74
⠋ Searching for 'FontLab review'...                    DEBUG    connect_tcp.started host='api.tavily.com' port=443 local_address=None timeout=10 socket_options=None                         _trace.py:87
⠹ Searching for 'FontLab review'...[02/26/25 13:38:02] DEBUG    connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x11026d8b0>                               _trace.py:87
                    DEBUG    start_tls.started ssl_context=<ssl.SSLContext object at 0x10d7d06d0> server_hostname='api.tavily.com' timeout=10             _trace.py:87
⠼ Searching for 'FontLab review'...                    DEBUG    start_tls.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x10d862690>                                 _trace.py:87
                    DEBUG    send_request_headers.started request=<Request [b'POST']>                                                                     _trace.py:87
                    DEBUG    send_request_headers.complete                                                                                                _trace.py:87
                    DEBUG    send_request_body.started request=<Request [b'POST']>                                                                        _trace.py:87
                    DEBUG    send_request_body.complete                                                                                                   _trace.py:87
                    DEBUG    receive_response_headers.started request=<Request [b'POST']>                                                                 _trace.py:87
⠏ Searching for 'FontLab review'...[02/26/25 13:38:04] DEBUG    receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Wed, 26 Feb 2025 12:38:04 GMT'),       _trace.py:87
                             (b'Content-Type', b'application/json'), (b'Content-Length', b'2491'), (b'Connection', b'keep-alive'), (b'Server', b'nginx'),             
                             (b'content-security-policy', b"default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src                      
                             'self';base-uri 'self';form-action 'self'; require-trusted-types-for 'script'; upgrade-insecure-requests;"),                             
                             (b'Strict-Transport-Security', b'max-age=31536000 ; includeSubDomains'), (b'X-Content-Type-Options', b'nosniff'),                        
                             (b'X-Frame-Options', b'DENY')])                                                                                                          
                    INFO     HTTP Request: POST https://api.tavily.com/search "HTTP/1.1 200 OK"                                                        _client.py:1740
                    DEBUG    receive_response_body.started request=<Request [b'POST']>                                                                    _trace.py:87
                    DEBUG    receive_response_body.complete                                                                                               _trace.py:87
                    DEBUG    response_closed.started                                                                                                      _trace.py:87
                    DEBUG    response_closed.complete                                                                                                     _trace.py:87
                    DEBUG    close.started                                                                                                                _trace.py:87
                    DEBUG    close.complete                                                                                                               _trace.py:87
                    ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158
No results found!
>>> yandex_anyws
[02/26/25 13:38:05] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['yandex_anyws']                                                                            cli.py:168
                    INFO     🔍 Querying engine: yandex_anyws                                                                                                api.py:74
                    ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158
No results found!
>>> yandex_searchit
[02/26/25 13:38:06] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['yandex_searchit']                                                                         cli.py:168
                    ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> you
[02/26/25 13:38:08] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['you']                                                                                     cli.py:168
                    ERROR    Error initializing engine 'you': Engine 'you': You.com API key is required. Set it via one of these env vars: YOU_API_KEY       api.py:82
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!
>>> you_news
[02/26/25 13:38:09] DEBUG    Using selector: KqueueSelector                                                                                      selector_events.py:64
                    DEBUG    Attempting to search with engines: ['you_news']                                                                                cli.py:168
                    ERROR    Error initializing engine 'you_news': Engine 'you_news': You.com API key is required. Set it via one of these env vars:         api.py:82
                             YOU_API_KEY                                                                                                                              
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  api.py:167
                    ERROR    Search failed: No search engines could be initialized. Make sure at least one engine dependency is installed.                  cli.py:174
                                         ❌ Search Errors                                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Error                                                                                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ No search engines could be initialized. Make sure at least one engine dependency is installed. │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
No results found!




this must be old log@api.py api.py — we have refactored params in the  modules, the former "name" attr of engine is now "engine_code"

---

_**Assistant**_

<think>From examining the user's query and attached file, I can see that there's an issue with several search engines failing with the error "X object has no attribute 'name'". This suggests that there's a discrepancy between the code and how it's being used.

The user mentioned:
> this must be old log@api.py api.py — we have refactored params in the modules, the former "name" attr of engine is now "engine_code"

This indicates that there has been a refactoring where the attribute "name" has been renamed to "engine_code" in the search engine classes, but it seems like the api.py file is still trying to access the old "name" attribute, leading to the attribute errors.

The attached file `src/twat_search/web/api.py` shows part of the search functionality. Looking at the current cursor position in the file, I should examine the code below this position to find where it might be accessing the "name" attribute that's causing these errors. Let me read the file and understand the logic to determine what changes are needed.</think>I'll examine the issue with the search engines failing due to the missing 'name' attribute. Let me look at the current implementation in the API module to see what needs to be updated.

---

_****_

Read file: src/twat_search/web/api.py

---

_****_



Now I need to examine the engine base class to understand the issue with the "name" attribute:

---

_****_

<details>
            <summary>Searched codebase "SearchEngine class with engine_code attribute" • **25** results</summary>
        
| File | Lines |
|------|-------|
| `src/twat_search/web/engines/base.py` | L1-54 |
| `src/twat_search/web/engines/base.py` | L67-105 |
| `.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L1002-1055 |
| `src/twat_search/web/engines/anywebsearch.py` | L111-165 |
| `src/twat_search/web/engines/searchit.py` | L214-266 |
| `src/twat_search/web/engines/base.py` | L105-125 |
| `src/twat_search/web/engines/__init__.py` | L1-82 |
| `src/twat_search/web/engines/brave.py` | L138-147 |
| `src/twat_search/web/engine_constants.py` | L1-59 |
| `twat_search.txt` | L580-615 |
| `tests/unit/web/engines/test_base.py` | L66-79 |
| `src/twat_search/web/engines/searchit.py` | L596-632 |
| `src/twat_search/web/engines/brave.py` | L147-156 |
| `src/twat_search/web/engines/anywebsearch.py` | L333-367 |
| `src/twat_search/web/engines/anywebsearch.py` | L563-604 |
| `src/twat_search/web/engines/bing_scraper.py` | L84-132 |
| `.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L459-510 |
| `src/twat_search/web/engines/anywebsearch.py` | L408-447 |
| `src/twat_search/web/engines/base.py` | L54-67 |
| `src/twat_search/web/engine_constants.py` | L59-97 |
| `src/twat_search/web/engines/serpapi.py` | L42-96 |
| `src/twat_search/web/engines/searchit.py` | L439-475 |
| `src/twat_search/web/engines/google_scraper.py` | L82-132 |
| `src/twat_search/web/engines/searchit.py` | L360-396 |
| `twat_search.txt` | L487-524 |

</details>

---

_****_



Now I need to look at engine implementations to see what's failing:

---

_****_

<details>
            <summary>Grep search for "'name' attribute has no attribute" • **0** files</summary>
        
No results found
</details>

---

_****_



Let me look at the error messages in the logs to understand the issue better:

---

_****_

<details>
            <summary>Grep search for "object has no attribute 'name'" • **2** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L13 | `ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L28 | `ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L89 | `ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L108 | `ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L131 | `ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L178 | `ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L181 | `ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L183 | `ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L187 | `ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L192 | `ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L194 | `ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L196 | `ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L238 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L239 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L240 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L241 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L242 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L310 | `ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L313 | `ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L314 | `ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L316 | `ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L317 | `ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L318 | `ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L343 | `ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L346 | `ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L348 | `ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L352 | `ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L357 | `ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L359 | `ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L361 | `ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L403 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L404 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L405 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L406 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L407 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L475 | `ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L478 | `ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L479 | `ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L481 | `ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L482 | `ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L483 | `ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L510 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L511 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L512 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L513 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L514 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L521 | `ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L534 | `ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L547 | `ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L564 | `ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L569 | `ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L605 | `ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L611 | `ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L616 | `ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_13-40-search-engine-initialization-errors.md` | L663 | `⟪ 104 characters skipped ⟫earch engines failing with the error "X object has no attribute 'name'". This suggests that there's a discrepancy between the code and how it's being used.` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3023 | `ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3038 | `ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3325 | `ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3344 | `ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3367 | `ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3414 | `ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3417 | `ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3419 | `ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3423 | `ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3428 | `ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3430 | `ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3432 | `ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3474 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3475 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3476 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3477 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3478 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3546 | `ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3549 | `ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3550 | `ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3552 | `ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3553 | `ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3554 | `ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3806 | `ERROR    Error initializing engine 'google_serpapi': 'SerpApiSearchEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3809 | `ERROR    Error initializing engine 'google_searchit': 'GoogleSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3811 | `ERROR    Error initializing engine 'pplx': 'PerplexitySearchEngine' object has no attribute 'name'                                       api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3815 | `ERROR    Error initializing engine 'critique': 'CritiqueSearchEngine' object has no attribute 'name'                                     api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3820 | `ERROR    Error initializing engine 'bing_searchit': 'BingSearchitEngine' object has no attribute 'name'                                  api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3822 | `ERROR    Error initializing engine 'qwant_searchit': 'QwantSearchitEngine' object has no attribute 'name'                                api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3824 | `ERROR    Error initializing engine 'yandex_searchit': 'YandexSearchitEngine' object has no attribute 'name'                              api.py:82` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3866 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3867 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3868 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3869 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3870 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3938 | `ERROR    Search with engine 'brave_anyws' failed: 'BraveAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3941 | `ERROR    Search with engine 'tavily' failed: 'TavilySearchEngine' object has no attribute 'name'                                        api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3942 | `ERROR    Search with engine 'duckduckgo' failed: 'DuckDuckGoSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3944 | `ERROR    Search with engine 'bing_anyws' failed: 'BingAnyWebSearchEngine' object has no attribute 'name'                                api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3945 | `ERROR    Search with engine 'qwant_anyws' failed: 'QwantAnyWebSearchEngine' object has no attribute 'name'                              api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L3946 | `ERROR    Search with engine 'yandex_anyws' failed: 'YandexAnyWebSearchEngine' object has no attribute 'name'                            api.py:158` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L4200 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L4201 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L4202 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L4203 | `WARNING  Unexpected error converting result: 'GoogleScraperEngine' object has no attribute 'name'                            google_scraper.py:212` |

</details>

---

_****_





Let me check where in the api.py file it's trying to access the 'name' attribute that's now 'engine_code':

---

_****_

<details>
            <summary>Grep search for "name" • **1** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L5 | `from twat_search.web.engines import standardize_engine_name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L10 | `logger = logging.getLogger(__name__)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L14 | `engine_name: str, engines: list[str], kwargs: dict, common_params: dict` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L18 | `- parameters prefixed with the engine name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L22 | `# Standardize engine name for parameter lookup` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L23 | `std_engine_name = standardize_engine_name(engine_name)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L25 | `# Look for parameters with both standardized and original name prefixes` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L28 | `if k.startswith(std_engine_name + "_"):` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L29 | `engine_specific[k[len(std_engine_name) + 1 :]] = v` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L30 | `elif k.startswith(engine_name + "_"):  # For backward compatibility` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L31 | `engine_specific[k[len(engine_name) + 1 :]] = v` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L34 | `std_engines = [standardize_engine_name(e) for e in engines]` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L45 | `engine_name: str,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L56 | `# Standardize engine name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L57 | `std_engine_name = standardize_engine_name(engine_name)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L59 | `# Try both standardized and original names for backward compatibility` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L60 | `engine_config = config.engines.get(std_engine_name)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L62 | `engine_config = config.engines.get(engine_name)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L64 | `logger.warning(f"Engine '{engine_name}' not configured.")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L68 | `engine_params = get_engine_params(engine_name, engines, kwargs, common_params)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L69 | `# Use standardized name to get the engine` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L71 | `std_engine_name, engine_config, **engine_params` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L73 | `logger.info(f"🔍 Querying engine: {engine_name}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L74 | `return (engine_name, engine_instance.search(query))` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L77 | `f"Engine '{engine_name}' is not available: {e}. The dependency may not be installed."` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L81 | `logger.error(f"Error initializing engine '{engine_name}': {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L101 | `engines: List of engine names to use (or None for all enabled)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L124 | `# Standardize engine names` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L125 | `engines = [standardize_engine_name(e) for e in engines]` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L140 | `engine_names = []` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L141 | `for engine_name in engines:` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L143 | `engine_name, config, engines, kwargs, common_params, query` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L146 | `engine_names.append(task[0])` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L155 | `for engine_name, result in zip(engine_names, results, strict=False):` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L157 | `logger.error(f"Search with engine '{engine_name}' failed: {result}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L159 | `logger.info(f"✅ Engine '{engine_name}' returned {len(result)} results")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/api.py` | L163 | `f"⚠️ Engine '{engine_name}' returned no results or unexpected type: {type(result)}"` |

</details>

---

_****_



Now I need to examine any place in the code where we might encounter the errors:

---

_****_

<details>
            <summary>Grep search for "self.name" • **11** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/README.md` | L582 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L450 | `logger.warning(f"Empty result received from {self.name}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L461 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L474 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L481 | `raise EngineError(self.name, "Brave API key is required for Brave search")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L561 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L568 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L606 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L607 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L646 | `raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L647 | `raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L670 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L671 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L672 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L710 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L749 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L756 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L790 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L791 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L792 | `raise EngineError(self.name, f"Invalid JSON response: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L821 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L863 | `f"Parameters {', '.join(unused_params)} set but not used by {self.name}"` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L865 | `logger.warning(f"Empty result received from {self.name}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L880 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L891 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L948 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L949 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L988 | `raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L989 | `raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L990 | `raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L3070 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-24-planning-tests-for-twat-search-web-package.md` | L303 | `+                 source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L1998 | `105 |             raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2001 | `107 |             raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2006 | `105 |             raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2008 | `107 |             raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2390 | `171 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2393 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2398 | `171 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2400 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2403 | `175 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2408 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2410 | `175 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-09-generating-a-name-for-the-chat.md` | L505 | `self.name = dict(airports).get(self.code)` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-09-generating-a-name-for-the-chat.md` | L506 | `self.city = self.name.split(',')[0] if self.name else None` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-09-generating-a-name-for-the-chat.md` | L641 | `self.name = name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/mock_engine.py` | L44 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L740 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L762 | `-             raise EngineError(self.name, f"Invalid input: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L765 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L767 | `-             raise EngineError(self.name, f"Network error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L770 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L772 | `-             raise EngineError(self.name, f"Parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L775 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L777 | `-             raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L780 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/web/test_api.py` | L60 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L915 | `logger.debug(f"Initialized {self.name} engine with params: {self.params}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L935 | `logger.debug(f"Searching with {self.name} for: {query}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L969 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L980 | `logger.error(f"Search error with {self.name}: {str(e)}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L1997 | `logger.debug(f"Initialized {self.name} engine with params: {self.params}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L2024 | `logger.debug(f"Searching with {self.name} for: {query}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L2061 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L2072 | `logger.error(f"Search error with {self.name}: {str(e)}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3538 | `+         logger.debug(f"Initialized {self.name} engine")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3561 | `+                         self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3613 | `+                         source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3625 | `+             raise EngineError(self.name, f"Search failed: {str(e)}") from e` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3908 | `logger.debug(f"Initialized {self.name} engine")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3963 | `-                         self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3977 | `+         logger.info(f"Searching with {self.name} for: {query}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4065 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4082 | `-             raise EngineError(self.name, f"Search failed: {str(e)}") from e` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4085 | `+             raise EngineError(self.name, error_msg) from e` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4429 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4483 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2731 | `-             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2737 | `-             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2742 | `-             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2747 | `-             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2752 | `-             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2779 | `-                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L344 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L415 | `+                 self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L480 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L491 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L494 | `+                     self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L498 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L542 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L552 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L651 | `+                 self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L703 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L714 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L717 | `+                     self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L721 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L787 | `+                 self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L846 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L857 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |

</details>

---

_****_





Let me look for modules that might include error-raising that use this attribute:

---

_****_

<details>
            <summary>Grep search for "EngineError.*self.name" • **12** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L461 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L474 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L481 | `raise EngineError(self.name, "Brave API key is required for Brave search")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L561 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L568 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L606 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L607 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L646 | `raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L647 | `raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L670 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L671 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L672 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L710 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L749 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L756 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L790 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L791 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L792 | `raise EngineError(self.name, f"Invalid JSON response: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L821 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L880 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L891 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L948 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L949 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L988 | `raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L989 | `raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L990 | `raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/pplx.py` | L105 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L288 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L332 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L363 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L407 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L440 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L443 | `raise EngineError(self.name, "Brave API key is required for Brave search")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L487 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L518 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L562 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L595 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L644 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/duckduckgo.py` | L171 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L1998 | `105 |             raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2001 | `107 |             raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2006 | `105 |             raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2008 | `107 |             raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2390 | `171 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2393 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2398 | `171 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2400 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2403 | `175 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2408 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2410 | `175 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L108 | `raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L110 | `raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L202 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L209 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L211 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L232 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L267 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L271 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L275 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L279 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L908 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L915 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1058 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1065 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1208 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1215 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1435 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1442 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1586 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1593 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L344 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L491 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L498 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L714 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L721 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L857 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L864 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L2823 | `+                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L2825 | `+                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L2827 | `+                 raise EngineError(self.name, f"Error: {str(e)}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L2867 | `-                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L2874 | `-                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3684 | `173 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3688 | `175 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3694 | `173 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3696 | `175 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3700 | `177 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3706 | `175 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3708 | `177 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4618 | `+             raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4620 | `+             raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4713 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4720 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4722 | `+                 raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L584 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L1259 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L1355 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L1473 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L596 | `+             raise EngineError(self.name, f"Invalid input: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L598 | `+             raise EngineError(self.name, f"Network error: {exc}") from exc` |

</details>

---

_****_





Let me check where SearchResult is created with source=self.name:

---

_****_

<details>
            <summary>Grep search for "SearchResult.*source=self.name" • **0** files</summary>
        
No results found
</details>

---

_****_







Let me search for the implementation of SearchResult:

---

_****_

<details>
            <summary>Grep search for "source=self.name" • **26** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/README.md` | L582 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L3070 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-24-planning-tests-for-twat-search-web-package.md` | L303 | `+                 source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/mock_engine.py` | L44 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/web/test_api.py` | L60 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/web/engines/test_base.py` | L33 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L198 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L580 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L480 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L542 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L552 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L703 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L846 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L1049 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/duckduckgo.py` | L132 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L464 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L1352 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L1629 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L1668 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L2125 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L462 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L938 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1658 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-05-consolidating-you-py-and-youcom-py.md` | L213 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-05-consolidating-you-py-and-youcom-py.md` | L361 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L149 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L171 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L896 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1046 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1196 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1423 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1574 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L2854 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3049 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3150 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4273 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4684 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4701 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L319 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/tavily.py` | L150 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-36-implementing-duckduckgo-search-engine.md` | L362 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L217 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/pplx.py` | L126 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L438 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/serpapi.py` | L148 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L969 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L2061 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3613 | `+                         source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4065 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4429 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4483 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L949 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1099 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1249 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1476 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1627 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L2586 | `+                 source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L3144 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4032 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4309 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4348 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4805 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13279 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13341 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13351 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13502 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13645 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13848 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L14742 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L14890 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L19471 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L22356 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L22551 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L22652 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L23775 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L24186 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L24203 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L27009 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L29486 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L30578 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L32130 | `+                         source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L32582 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L32946 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L33000 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L34094 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L41427 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L48718 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L49194 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L49914 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2779 | `-                 source=self.name,` |

</details>

---

_****_





Based on my analysis, I need to update the code to fix the "no attribute 'name'" errors. I'll update the api.py file to use 'engine_code' instead of 'name':

---

_****_



---

_****_





Now I need to look at the engine classes that are raising errors:

---

_****_

<details>
            <summary>Searched codebase "raise EngineError" • **25** results</summary>
        
| File | Lines |
|------|-------|
| `tests/unit/web/test_exceptions.py` | L19-34 |
| `tests/unit/web/test_exceptions.py` | L34-45 |
| `tests/unit/web/engines/test_base.py` | L100-106 |
| `tests/unit/web/engines/test_base.py` | L106-113 |
| `src/twat_search/web/engines/base.py` | L105-125 |
| `src/twat_search/web/engines/base.py` | L1-54 |
| `tests/unit/web/test_exceptions.py` | L1-19 |
| `src/twat_search/web/engines/hasdata.py` | L155-168 |
| `tests/unit/web/engines/test_base.py` | L51-66 |
| `tests/unit/web/test_exceptions.py` | L45-68 |
| `tests/unit/web/test_api.py` | L158-170 |
| `tests/unit/web/test_api.py` | L149-158 |
| `tests/web/test_bing_scraper.py` | L251-290 |
| `src/twat_search/web/engines/__init__.py` | L215-247 |
| `src/twat_search/web/engines/__init__.py` | L153-215 |
| `src/twat_search/web/api.py` | L42-83 |
| `tests/unit/web/engines/test_base.py` | L36-51 |
| `tests/unit/web/test_api.py` | L130-137 |
| `tests/unit/web/engines/test_base.py` | L1-36 |
| `src/twat_search/web/engines/base.py` | L67-105 |
| `src/twat_search/web/engines/__init__.py` | L247-298 |
| `.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L459-510 |
| `tests/unit/mock_engine.py` | L1-48 |
| `.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L917-996 |
| `tests/web/test_bing_scraper.py` | L218-251 |

</details>

---

_****_





Now I need to check the EngineError class:

---

_****_

<details>
            <summary>Searched codebase "class EngineError" • **25** results</summary>
        
| File | Lines |
|------|-------|
| `tests/unit/web/test_exceptions.py` | L19-34 |
| `tests/unit/web/test_exceptions.py` | L34-45 |
| `tests/unit/web/engines/test_base.py` | L100-106 |
| `tests/unit/web/engines/test_base.py` | L106-113 |
| `src/twat_search/web/engines/hasdata.py` | L155-168 |
| `tests/unit/web/test_exceptions.py` | L1-19 |
| `src/twat_search/web/engines/base.py` | L105-125 |
| `src/twat_search/web/engines/base.py` | L1-54 |
| `tests/unit/web/test_exceptions.py` | L45-68 |
| `tests/unit/web/engines/test_base.py` | L51-66 |
| `tests/web/test_bing_scraper.py` | L251-290 |
| `src/twat_search/web/engines/critique.py` | L183-212 |
| `tests/unit/web/test_api.py` | L158-170 |
| `src/twat_search/web/engines/__init__.py` | L153-215 |
| `tests/unit/web/engines/test_base.py` | L1-36 |
| `.specstory/history/2025-02-25_06-34-implementing-safe-import-patterns-in-modules.md` | L632-688 |
| `src/twat_search/web/cli.py` | L615-648 |
| `tests/web/test_bing_scraper.py` | L218-251 |
| `.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L459-510 |
| `src/twat_search/web/cli.py` | L310-364 |
| `src/twat_search/web/engines/base.py` | L67-105 |
| `tests/unit/web/test_api.py` | L149-158 |
| `src/twat_search/web/api.py` | L42-83 |
| `src/twat_search/web/engines/__init__.py` | L215-247 |
| `.specstory/history/2025-02-25_07-17-implementing-phase-1-from-todo-md.md` | L917-996 |

</details>

---

_****_







Let me find the exceptions.py file:

---

_****_

<details>
            <summary>Searched codebase "src/twat_search/web/exceptions.py" • **25** results</summary>
        
| File | Lines |
|------|-------|
| `src/twat_search/web/engines/hasdata.py` | L155-168 |
| `src/twat_search/web/api.py` | L117-170 |
| `src/twat_search/web/engines/base.py` | L105-125 |
| `src/twat_search/web/engines/you.py` | L75-107 |
| `tests/unit/web/test_exceptions.py` | L1-19 |
| `src/twat_search/web/engines/base.py` | L1-54 |
| `src/twat_search/web/engines/tavily.py` | L156-194 |
| `src/twat_search/web/api.py` | L42-83 |
| `twat_search.txt` | L961-995 |
| `src/twat_search/web/api.py` | L83-117 |
| `src/twat_search/web/engines/critique.py` | L183-212 |
| `src/twat_search/__init__.py` | L1-26 |
| `src/twat_search/web/engines/anywebsearch.py` | L25-81 |
| `twat_search.txt` | L852-879 |
| `src/twat_search/web/engines/tavily.py` | L101-156 |
| `src/twat_search/web/engines/searchit.py` | L302-360 |
| `src/twat_search/web/engines/brave.py` | L75-120 |
| `src/twat_search/web/engines/google_scraper.py` | L240-290 |
| `twat_search.txt` | L440-460 |
| `src/twat_search/web/engines/duckduckgo.py` | L172-221 |
| `src/twat_search/web/engines/hasdata.py` | L93-155 |
| `src/twat_search/web/engines/anywebsearch.py` | L645-678 |
| `src/twat_search/web/engines/searchit.py` | L554-596 |
| `src/twat_search/web/engines/anywebsearch.py` | L522-563 |
| `src/twat_search/web/engines/anywebsearch.py` | L745-777 |

</details>

---

_****_



Let me find the actual exceptions.py file by using file search:

---

_****_

<details>
            <summary>Searched codebase "exceptions.py" • **2** results</summary>
        
| File |
|------|
| `undefined` |
| `undefined` |

</details>

---

_****_





Now let me read the exceptions.py file to understand how EngineError is defined:

---

_****_

Read file: src/twat_search/web/exceptions.py

---

_****_



Now that I understand the problem better, I need to look at some of the engine implementations that are failing, specifically the ones using `self.name` instead of `self.engine_code`:

---

_****_

Read file: src/twat_search/web/engines/tavily.py

---

_****_



I'll also check the class to see if the `self.name` attribute is defined:

---

_****_

Read file: src/twat_search/web/engines/tavily.py

---

_****_





Now I need to check one more place where the `name` attribute is used in the constructor:

---

_****_

Read file: src/twat_search/web/engines/tavily.py

---

_****_





Let me check a bit further down:

---

_****_

Read file: src/twat_search/web/engines/tavily.py

---

_****_







Now I also need to check where `source=self.name` is used:

---

_****_

Read file: src/twat_search/web/engines/tavily.py

---

_****_





Based on what I've found, I need to update the tavily.py file. The issue is that all the places where `self.name` is referenced should be updated to `self.engine_code`:

---

_****_

```diff
          if not self.config.api_key:
              raise EngineError(
-                 self.name,
+                 self.engine_code,
                  f"Tavily API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
              )
                      item.get("content", "").strip(), width=500, placeholder="..."
                  ),
-                 source=self.name,
+                 source=self.engine_code,
                  rank=rank,
                  raw=item,
                  data = response.json()
              except httpx.HTTPStatusError as e:
-                 raise EngineError(self.name, f"HTTP error: {e}")
+                 raise EngineError(self.engine_code, f"HTTP error: {e}")
              except httpx.RequestError as e:
-                 raise EngineError(self.name, f"Request error: {e}")
+                 raise EngineError(self.engine_code, f"Request error: {e}")
              except Exception as e:
-                 raise EngineError(self.name, f"Error: {e!s}")
+                 raise EngineError(self.engine_code, f"Error: {e!s}")
  
          results = []
      Search using Tavily AI search.
  
-     This function’s API and signature remain identical.
+     This function's API and signature remain identical.
      """
      config = EngineConfig(
```

---

_****_







Now let me find other search engines that might have the same issue. Let's look for all files in the engines directory:

---

_****_

<details>
            <summary>Listed directory src/twat_search/web/engines • **16** results</summary>
        
| Name |
|-------|
| 📄 `tavily.py` |
| 📁 `__pycache__` |
| 📄 `bing_scraper.py` |
| 📄 `__init__.py` |
| 📄 `you.py` |
| 📄 `serpapi.py` |
| 📄 `searchit.py` |
| 📄 `pplx.py` |
| 📄 `hasdata.py` |
| 📄 `google_scraper.py` |
| 📄 `duckduckgo.py` |
| 📄 `critique.py` |
| 📄 `brave.py` |
| 📄 `anywebsearch.py` |
| 📄 `base.py` |
| 📄 `.DS_Store` |

</details>

---

_****_









Now let me look for the EngineError usage in the codebase:

---

_****_

<details>
            <summary>Grep search for "raise EngineError\(self\.name" • **10** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L461 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L474 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L481 | `raise EngineError(self.name, "Brave API key is required for Brave search")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L561 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L568 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L606 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L607 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L646 | `raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L647 | `raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L670 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L671 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L672 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L710 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L749 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L756 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L790 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L791 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L792 | `raise EngineError(self.name, f"Invalid JSON response: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L821 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L880 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L891 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L948 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L949 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L988 | `raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L989 | `raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L990 | `raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L1998 | `105 |             raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2001 | `107 |             raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2006 | `105 |             raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2008 | `107 |             raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2390 | `171 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2393 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2398 | `171 |                 raise EngineError(self.name, f"HTTP error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2400 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2403 | `175 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2408 | `173 |                 raise EngineError(self.name, f"Request error: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/CLEANUP.txt` | L2410 | `175 |                 raise EngineError(self.name, f"Error: {e!s}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L584 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L1259 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L1355 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-16-implementing-functions-for-brave-search-engines.md` | L1473 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L388 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L438 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L467 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L517 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L546 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L595 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L624 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L674 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L596 | `+             raise EngineError(self.name, f"Invalid input: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L598 | `+             raise EngineError(self.name, f"Network error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L600 | `+             raise EngineError(self.name, f"Parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L602 | `+             raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L232 | `raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L267 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L271 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L275 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L279 | `raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L908 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L915 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1058 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1065 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1208 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1215 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1435 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1442 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1586 | `+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1593 | `+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L494 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L527 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L531 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L535 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L539 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L970 | `+             raise EngineError(self.name, f"Error running searchit scraper: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L998 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1044 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1072 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1118 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1146 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1191 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1219 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1265 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1726 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1768 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1798 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1840 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1872 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1875 | `+             raise EngineError(self.name, "Brave API key is required for Brave search")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1917 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1947 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1989 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L2021 | `+             raise EngineError(self.name, "Search query cannot be empty")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L2024 | `+             raise EngineError(self.name, "Yandex API key and folder ID are required for Yandex search")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L2066 | `+             raise EngineError(self.name, error_msg) from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L108 | `raise EngineError(self.name, f"Failed to fetch image from URL: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L110 | `raise EngineError(self.name, f"Error processing image: {e}")` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L202 | `raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L209 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L211 | `raise EngineError(self.name, f"Search failed: {exc}") from exc` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L344 | `raise EngineError(self.name, f"Response parsing error: {exc}") from exc` |

</details>

---

_****_










Let me also look for instances of `source=self.name`:

---

_****_

<details>
            <summary>Grep search for "source=self\.name" • **25** files</summary>
        
| File | Line | Match |
|------|------|-------|
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/twat_search.txt` | L3070 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/README.md` | L582 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/serpapi.py` | L148 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/anywebsearch.py` | L217 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/mock_engine.py` | L44 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/web/test_api.py` | L60 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/searchit.py` | L319 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/duckduckgo.py` | L132 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L149 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/critique.py` | L171 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/google_scraper.py` | L198 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-26_12-18-update-engine-imports-and-exports-in-init-py.md` | L2779 | `-                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L896 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1046 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1196 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1423 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_01-58-creating-and-tracking-project-tasks.md` | L1574 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_07-34-integrating-hasdata-google-serp-apis.md` | L438 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_06-07-implementing-bing-scraper-engine.md` | L580 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L480 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L542 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L552 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L703 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L846 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_03-54-integrating-search-engines-into-twat-search.md` | L1049 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L462 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L938 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_08-19-implementing-search-engines-from-nextengines-md.md` | L1658 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L464 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L1352 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L1629 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L1668 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-27-implementing-tests-for-twat-search-package.md` | L2125 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-05-consolidating-you-py-and-youcom-py.md` | L213 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-05-consolidating-you-py-and-youcom-py.md` | L361 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-36-implementing-duckduckgo-search-engine.md` | L362 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L2854 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3049 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L3150 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4273 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4684 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_04-48-unifying-search-engine-parameters-in-twat-search.md` | L4701 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L969 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L2061 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L3613 | `+                         source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4065 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4429 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_05-43-implementing-the-webscout-search-engine.md` | L4483 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L949 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1099 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1249 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1476 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L1627 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L2586 | `+                 source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L3144 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4032 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4309 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4348 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L4805 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13279 | `+                                     source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13341 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13351 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13502 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13645 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L13848 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L14742 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L14890 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L19471 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L22356 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L22551 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L22652 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L23775 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L24186 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L24203 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L27009 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L29486 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L30578 | `source=self.name` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L32130 | `+                         source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L32582 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L32946 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L33000 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L34094 | `+                             source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L41427 | `+                                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L48718 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L49194 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history.txt` | L49914 | `+                 source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/tests/unit/web/engines/test_base.py` | L33 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/src/twat_search/web/engines/pplx.py` | L126 | `source=self.name,` |
| `file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_search/.specstory/history/2025-02-25_02-24-planning-tests-for-twat-search-web-package.md` | L303 | `+                 source=self.name` |

</details>

---

_****_












Based on the results, there are multiple instances of `self.name` throughout the codebase that need to be updated to `self.engine_code`. Let me create a script to automate the update:

---

_****_

```diff
- 
+ #!/usr/bin/env python
+ # this_file: fix_name_attribute.py
+ 
+ """
+ Script to fix the 'name' attribute references in search engine classes.
+ 
+ This script replaces references to 'self.name' with 'self.engine_code' 
+ to reflect the refactoring of the attribute name in the SearchEngine class.
+ """
+ 
+ import glob
+ import re
+ import os
+ 
+ 
+ def fix_file(file_path):
+     """Fix 'self.name' references in a file."""
+     print(f"Processing {file_path}...")
+     
+     with open(file_path, "r", encoding="utf-8") as file:
+         content = file.read()
+     
+     # Replace self.name references
+     original_content = content
+     content = re.sub(r"self\.name(?!\w)", "self.engine_code", content)
+     
+     if content != original_content:
+         print(f"  Found and replaced references in {file_path}")
+         with open(file_path, "w", encoding="utf-8") as file:
+             file.write(content)
+     else:
+         print(f"  No references found in {file_path}")
+ 
+ 
+ def main():
+     """Main function to process engine files."""
+     engine_dir = "src/twat_search/web/engines"
+     
+     if not os.path.exists(engine_dir):
+         print(f"Error: Directory {engine_dir} does not exist")
+         return
+     
+     # Process all Python files in the engines directory
+     for file_path in glob.glob(f"{engine_dir}/*.py"):
+         # Skip __init__.py and base.py as they might have different logic
+         if os.path.basename(file_path) not in ["__init__.py", "base.py"]:
+             fix_file(file_path)
+     
+     print("Done!")
+ 
+ 
+ if __name__ == "__main__":
+     main() 
```

---

_****_





Let me fix the linter errors:

---

_****_

```diff
  
  
- def fix_file(file_path):
+ def fix_file(file_path: str) -> None:
      """Fix 'self.name' references in a file."""
      print(f"Processing {file_path}...")
  
  
- def main():
+ def main() -> None:
      """Main function to process engine files."""
      engine_dir = "src/twat_search/web/engines"
```

---

_****_










Now run the script to fix all instances of `self.name` in the search engine files:

---

_****_

```bash
python fix_name_attribute.py
```

```
Processing src/twat_search/web/engines/serpapi.py...
  Found and replaced references in src/twat_search/web/engines/ser
papi.py                                                           Processing src
/twat_search/web/engines/pplx.py...
  Found and replaced references in src/twat_search/web/engines/ppl
x.py                                                              Processing src
/twat_search/web/engines/anywebsearch.py...
  Found and replaced references in src/twat_search/web/engines/any
websearch.py                                                      Processing src
/twat_search/web/engines/tavily.py...
  No references found in src/twat_search/web/engines/tavily.py
Processing src/twat_search/web/engines/brave.py...
  No references found in src/twat_search/web/engines/brave.py
Processing src/twat_search/web/engines/you.py...
  No references found in src/twat_search/web/engines/you.py
Processing src/twat_search/web/engines/searchit.py...
  Found and replaced references in src/twat_search/web/engines/sea
rchit.py                                                          Processing src
/twat_search/web/engines/bing_scraper.py...
  No references found in src/twat_search/web/engines/bing_scraper.
py                                                                Processing src
/twat_search/web/engines/hasdata.py...
  No references found in src/twat_search/web/engines/hasdata.py
Processing src/twat_search/web/engines/critique.py...
  Found and replaced references in src/twat_search/web/engines/cri
tique.py                                                          Processing src
/twat_search/web/engines/duckduckgo.py...
  Found and replaced references in src/twat_search/web/engines/duc
kduckgo.py                                                        Processing src
/twat_search/web/engines/google_scraper.py...
  Found and replaced references in src/twat_search/web/engines/goo
gle_scraper.py                                                    Done!
%                                                                 

```

---

_****_












Now let's check if we need to make any other changes, like updating the `api.py` file to handle both attributes:

---

_****_

Read file: src/twat_search/web/api.py

---

_****_







Let's check the `get_engine` function in the base.py file and how it's being used:

---

_****_

Read file: src/twat_search/web/engines/base.py

---

_****_









Now I need to check how engines are registered:

---

_****_

Read file: src/twat_search/web/engines/base.py

---

_****_





---



---
