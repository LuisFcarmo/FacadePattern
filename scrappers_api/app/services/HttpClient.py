# app/services/http_client.py

import requests
from requests.exceptions import RequestException
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import Stealth


class HttpClient:
    def __init__(self, timeout: int = 15):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.google.com/',
        })

    def get_html_simple(self, url: str) -> str | None:
        print(f"INFO: Tentando busca simples para {url}")
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"ERRO: Falha na busca simples. Detalhes: {e}")
            return None

    def get_html_browser(self, url: str) -> str | None:     
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
    
    def get_page_plawright(self, url):
        print(f"INFO: Usando modo navegador (Playwright) para {url}")
        try:
            with Stealth().use_sync(sync_playwright()) as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=60000, wait_until='domcontentloaded')
                return
            
        except PlaywrightTimeoutError:
            print(f"ERRO: Timeout ao carregar com Playwright.")
            return None
        except Exception as e:
            print(f"ERRO: Falha inesperada com Playwright. Detalhes: {e}")
            return None