# app/services/http_client.py

import requests
from requests.exceptions import RequestException
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import Stealth


class HttpClient:
    """
        A wrapper for making HTTP requests.
        
        This client provides two methods for fetching HTML content:
        1. `get_html_simple`: A fast method using the `requests` library for static pages.
        2. `get_html_browser`: A more robust method using Playwright for dynamic,
        JavaScript-rendered pages.
    """
    def __init__(self, timeout: int = 15):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.google.com/',
        })

    def get_html_simple(self, url: str) -> str | None:
        """
            Fetches HTML content using a simple GET request.

            Args:
                url (str): The URL to retrieve.

            Returns:
                Optional[str]: The HTML content as a string if the request is successful,
                            otherwise None.
        """

        print(f"INFO: Tentando busca simples para {url}")
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"ERRO: Falha na busca simples. Detalhes: {e}")
            return None

    def get_html_browser(self, url: str) -> str | None:     
        """
            Fetches HTML content by rendering the page in a headless browser (Playwright).
            
            This method is suitable for websites that load content dynamically with JavaScript.

            Args:
                url (str): The URL to retrieve.

            Returns:
                Optional[str]: The rendered HTML content as a string if successful,
                            otherwise None.
        """
        print(f"INFO: Usando modo navegador (Playwright) para {url}")
        try:
            with Stealth().use_sync(sync_playwright()) as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=60000, wait_until='domcontentloaded')
                html_content = page.content()
                browser.close()
                return html_content
            
        except PlaywrightTimeoutError:
            print(f"ERRO: Timeout ao carregar com Playwright.")
            return None
        except Exception as e:
            print(f"ERRO: Falha inesperada com Playwright. Detalhes: {e}")
            return None
    