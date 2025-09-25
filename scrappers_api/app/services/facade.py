from typing import List
from app.models.product import Product
from app.scrapers.interfaces import IScraper
from app.scrapers.olx_scraper import OLXScraper

class ScrapingFacade:
    """
        A facade that provides a single, simplified interface to control all web scrapers.
        
        This class initializes all available scraper modules and orchestrates the
        product search process across all of them, aggregating the results.
    """
    def __init__(self):
        """
            Initializes the facade by registering all scraper instances.
        """
        self.scrapers = [
            OLXScraper(),
        ]

    def search_products(self, product_name: str, **kwargs) -> List[Product]:
        """
            Searches for a product across all registered scrapers.

            It iterates through each scraper, executes its scrape method, and collects
            all results into a single list.

            Args:
                product_name (str): The name of the product to search for.
                **kwargs: Additional keyword arguments that can be passed down to
                        the individual scrapers (e.g., location, max_price).

            Returns:
                List[Product]: A list containing all Product objects found by the scrapers.
        """
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
        
