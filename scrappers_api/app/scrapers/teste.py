from app.scrapers.olx_scraper import OLXScraper

scraper = OLXScraper()
resultados = scraper.scrape(
    "ps4",
    min_price=100,
    max_price=1000,
    sort_by="relevance"
)
