from abc import ABC, abstractmethod
from typing import List
from app.models.product import Product
from typing import List, Optional, Literal

class IScraper(ABC):
    @abstractmethod
    def scrape(
        self,
        product_name: str,
        *,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        state: Optional[str] = None,
        sort_by: Optional[Literal["relevance", "newest", "price_asc", "price_desc"]] = None
    ) -> List[Product]:
        pass