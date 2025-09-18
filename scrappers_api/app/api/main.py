from fastapi import FastAPI
from typing import List
from app.services.facade import ScrapingFacade
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(
    title="API de Scraping de Produtos Usados",
    description="Busca produtos na OLX, Enjoei e outros sites."
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


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

