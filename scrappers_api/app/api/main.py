from fastapi import FastAPI
from typing import List

app = FastAPI(
    title="API de Scraping de Produtos Usados",
    description="Busca produtos na OLX, Enjoei e outros sites."
)

@app.get("/search")
def search_products():
    
    produto_alvo = "ps4"
    filtros = {
        "min_price": 100,
        "max_price": 1000,
        "sort_by": "relevance"
    }
    facade = ScrapingFacade()

    return facade.search_products(product_name=produto_alvo, **filtros)

@app.get("/", include_in_schema=False)
async def read_root():
    return FileResponse(os.path.join(STATIC_DIR, 'index.html'))

