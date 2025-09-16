from urllib.parse import urlencode
from dotenv import load_dotenv
import os
load_dotenv()

class OLXURLBuilder:
    def __init__(self, state_code: str = "go"):
        self.base_url = f"{os.getenv("OLX_SCRAPER_BASE_URL")}/estado-{state_code}"
        self.params = {}

    def with_query(self, query: str):
        self.params['q'] = query
        return self 

    def with_price_range(self, min_price: int, max_price: int):
        self.params['ps'] = min_price
        self.params['pe'] = max_price
        return self

    def sort_by_date(self):
        self.params['sf'] = 1
        return self

    def build(self) -> str:
        if not self.params:
            return self.base_url
        
        query_string = urlencode(self.params)
        return f"{self.base_url}?{query_string}"