from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import Stealth
import time

class PlawrightService:
    def ExecutePlaywrightRoutineInPage(self, url, routines=None):
        routines = routines or []

        try:
            with Stealth().use_sync(sync_playwright()) as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=60000, wait_until='domcontentloaded')

                for routine in routines:
                    routine(page)

                html = page.content()
                browser.close()
                return html

        except PlaywrightTimeoutError:
            print(f"ERRO: Timeout ao carregar com Playwright.")
            return None
        except Exception as e:
            print(f"ERRO: Falha inesperada com Playwright. Detalhes: {e}")
            return None

class Routines:
    @staticmethod
    def scroll_infinito(page, passo=1000, delay=1):
        ultima_altura = page.evaluate("document.body.scrollHeight")
        while True:
            page.evaluate(f"window.scrollBy(0, {passo})")
            time.sleep(delay)
            nova_altura = page.evaluate("document.body.scrollHeight")
            if nova_altura == ultima_altura:
                break
            ultima_altura = nova_altura
