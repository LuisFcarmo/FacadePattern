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
        try:
            print(f"Buscando produtos em: {url}")
            soup = self.GetSoupFromPageProductsByPage(url)
            products = self.GetProdutos(soup)
            return products
        
        except Exception as e:
            print(f"Erro ao buscar na URL {url}: {e}")
            return [] 
        
    
    
    def GetSoupFromPageProductsByPage(self, url):
        html_content = self.HttpService.get_html_browser(url=url)
        return BeautifulSoup(html_content, 'lxml')
   
    def GetPagesUrls(self, url):
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
    
      