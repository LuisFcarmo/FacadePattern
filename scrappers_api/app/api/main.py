from fastapi import FastAPI
from typing import List

app = FastAPI(
    title="API de Scraping de Produtos Usados",
    description="Busca produtos na OLX, Enjoei e outros sites."
)

@app.get("/search")
async def search_products():
    return "oii"

