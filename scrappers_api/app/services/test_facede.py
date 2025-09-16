from app.services.facade import ScrapingFacade

def executar_busca():
    facade = ScrapingFacade()

    produto_alvo = "ps4"
    filtros = {
        "min_price": 100,
        "max_price": 1000,
        "sort_by": "relevance"
    }

    resultados_finais = facade.search_products(produto_alvo, **filtros)

    if resultados_finais:
        print("\n--- Resultados Encontrados ---")
        for produto in resultados_finais:
            print(f"Nome:  {produto['title_element']}")
            print(f"Preço: R$ {produto['price_element']}")
            print(f"Link:  {produto['url']}")
            print("-" * 20)
    else:
        print("\nNenhum resultado encontrado para esta busca.")


if __name__ == "__main__":
    executar_busca()