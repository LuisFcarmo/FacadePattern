from typing import List
from app.models.product import Product
from app.scrapers.interfaces import IScraper
from app.scrapers.olx_scraper import OLXScraper

class ScrapingFacade:
    #FACE QUE CONTROLA TODOS OS NOSSOS RASPADORES
    def __init__(self):
        self.scrapers = [
            OLXScraper(),
        ]

    def search_products(self, product_name: str, **kwargs) -> List[Product]:
        print(f"--- FACADE: Iniciando busca por '{product_name}' em {len(self.scrapers)} fonte(s) ---")
        
        all_products: List[Product] = []
        
        for scraper in self.scrapers:
            scraper_name = scraper.__class__.__name__
            print(f"-> Executando {scraper_name}...")
            try:
                results = scraper.scrape(product_name, **kwargs)
                print(f"   {scraper_name} encontrou {len(results)} resultados.")
                all_products.extend(results)
                
            except Exception as e:
                print(f"   ERRO no {scraper_name}: {e}")
        
