from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import Stealth
import time

class PlawrightService:
    """
        A service class to encapsulate Playwright operations, providing a structured
        way to execute browser automation routines on a given web page.
    """
    def ExecutePlaywrightRoutineInPage(self, url, routines=None):
        """
            Launches a headless browser, navigates to a URL, executes a series of routines,
            and returns the final page's HTML content.

            Args:
                url (str): The URL of the page to navigate to.
                routines (Optional[List[Callable[[Page], None]]]): A list of functions (routines) to be
                                                                executed on the page. Each function
                                                                must accept a Playwright Page object
                                                                as its only argument. Defaults to None.

            Returns:
                Optional[str]: The HTML content of the page after executing the routines,
                            or None if an error (e.g., timeout) occurs.
        """
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
    """
        A collection of static methods representing common browser automation
        routines that can be passed to the PlawrightService.
    """
    @staticmethod
    def scroll_infinito(page, passo=1000, delay=1):
        """
            Performs an "infinite scroll" on a page until no new content is loaded.

            It repeatedly scrolls down by a fixed step and waits for a delay, stopping
            when the page's scroll height no longer increases.

            Args:
                page (Page): The Playwright Page object to scroll.
                step (int): The number of pixels to scroll down in each step. Defaults to 1000.
                delay (float): The delay in seconds between each scroll action to allow
                            content to load. Defaults to 1.0.
        """
        ultima_altura = page.evaluate("document.body.scrollHeight")
        while True:
            page.evaluate(f"window.scrollBy(0, {passo})")
            time.sleep(delay)
            nova_altura = page.evaluate("document.body.scrollHeight")
            if nova_altura == ultima_altura:
                break
            ultima_altura = nova_altura
