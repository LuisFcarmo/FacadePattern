from typing import List
import json
from app.models.product import Product
from app.scrapers.interfaces.IScraper import IScraper
from typing import List, Optional, Literal
from app.scrapers.builders import OLXURLBuilder
from app.services.PlaywrightService import PlawrightService, Routines
from app.services.HttpClient import HttpClient
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class OLXScraper(IScraper):
    """
        A web scraper for extracting product listings from OLX Brazil.

        This scraper is designed to handle OLX's dynamic page loading,
        including pagination that appears after scrolling. It uses a combination
        of Playwright for initial page rendering and concurrent requests for
        scraping individual pages efficiently.
    """

    _SORT_MAP = { "newest": 1 }
        
    def __init__(self):
        super().__init__()
        self.HttpService = HttpClient()
        self.PlawrightService = PlawrightService()
        
    def scrape(
        self,
        product_name: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        state: str = "go",  
        sort_by: Literal["relevance", "newest", "price_asc", "price_desc"] = "relevance",
        page: int = 1
    ) -> List[Product]:
        """
            Orchestrates the scraping process for a given product search on OLX.

            It builds the initial search URL, finds all pagination links, and then
            scrapes each page concurrently to gather all product data.

            Args:
                product_name (str): The name of the product to search for.
                min_price (Optional[int]): The minimum price filter.
                max_price (Optional[int]): The maximum price filter.
                state (str): The Brazilian state code (e.g., "go" for Goiás) to search in.
                sort_by (Literal): The sorting order for the results.
                page (int): The starting page number (currently not implemented by OLX in the same way).

            Returns:
                List[Product]: A list of all `Product` objects found across all pages.
        """
        target_state = state or "go"
        total_products = []
        url_builder = OLXURLBuilder(state_code=target_state)
        
        url_builder.with_query(product_name)

        if min_price is not None and max_price is not None:
            url_builder.with_price_range(min_price, max_price)

        if sort_by == "newest":
            url_builder.sort_by_date()

        target_url = url_builder.build()
        pages_url = self.GetPagesUrls(target_url)
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(self.scrape_single_page, pages_url)
            for product_list_per_page in results:
                total_products.extend(product_list_per_page)
        
        print("Busca finalizada!")
        return total_products

    def scrape_single_page(self, url:str):
        """
            Scrapes a single OLX results page for product data.

            Args:
                url (str): The URL of the results page to scrape.

            Returns:
                List[Product]: A list of products found on the page, or an empty list if an error occurs.
        """
        try:
            print(f"Buscando produtos em: {url}")
            soup = self.GetSoupFromPageProductsByPage(url)
            products = self.GetProdutos(soup)
            return products
        
        except Exception as e:
            print(f"Erro ao buscar na URL {url}: {e}")
            return [] 
        
    
    
    def GetSoupFromPageProductsByPage(self, url):
        """
            Fetches page content using a browser and returns a BeautifulSoup object.

            Args:
                url (str): The URL to fetch.

            Returns:
                BeautifulSoup: A parsed object of the page's HTML.
        """
        html_content = self.HttpService.get_html_browser(url=url)
        return BeautifulSoup(html_content, 'lxml')
   
    def GetPagesUrls(self, url):
        """
            Retrieves all pagination URLs from the initial search results page.

            OLX lazy-loads its pagination controls, so this method uses Playwright
            to simulate infinite scrolling to reveal all available page links before
            extracting them.

            Args:
                url (str): The initial search URL.

            Returns:
                List[str]: A list of all unique URLs for each page of the search results.
        """
        Pages_Urls = []
        html_content = self.PlawrightService.ExecutePlaywrightRoutineInPage(
            url=url,
            routines=[Routines.scroll_infinito]
        )
        
        soup = BeautifulSoup(html_content, 'lxml')
        buttons_pagination = soup.select('button[class*="Pagination_pageButton__9hd5x"]')
        
        for button_pagination in buttons_pagination:
            a_tag = button_pagination.find("a")
            
            if a_tag:
                Pages_Urls.append(a_tag.get('href'))
        
        return Pages_Urls
        
    def GetProdutos(self, soup):
        """
            Extracts product details from the BeautifulSoup object of a results page.

            Args:
                soup (BeautifulSoup): The parsed HTML of the page.

            Returns:
                List[Product]: A list of `Product` objects extracted from the page.
        """
        products = []
        container_selector = 'div[class*="adListContainer"]' 
        ad_container = soup.select_one(container_selector)

        if ad_container:
            lista_de_anuncios = ad_container.select('section[class*="olx-adcard"]')
                        
            for ad_card in lista_de_anuncios:
                link_element = ad_card.select_one('a[class*="olx-adcard__link"]')
                title_element = ad_card.select_one('h2[class*="olx-adcard__title"]').text
                price_element = ad_card.select_one('h3[class*="olx-adcard__price"]').text
                location_element = ad_card.select_one('p[class*="adcard__location"]').text
                date_element = ad_card.select_one('p[class*="olx-adcard__date"]').text
                image_element = ad_card.select_one("img")
                if image_element:
                    image_element = image_element["src"]
                
                if link_element:
                    url = link_element.get('href')

                products.append(Product(
                    title=title_element,
                    price=price_element,
                    local=location_element,
                    date=date_element,
                    link=url,
                    image=image_element
                ))
        
            
            
        products_dict = [p.__dict__ for p in products]
        return products_dict
    
      