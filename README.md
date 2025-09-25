# 🚀 Projeto de Web Scraping com Padrão Façade

Uma aplicação de **web scraping** robusta e extensível em **Python**, projetada para extrair dados de produtos de múltiplos sites de e-commerce de forma eficiente e organizada.

---

## 📌 Visão Geral

Este projeto utiliza uma **arquitetura moderna** para resolver desafios comuns de web scraping, como:

- Renderização de conteúdo dinâmico com **JavaScript**.  
- Consulta simultânea a várias fontes de dados.  

O núcleo do design é o **padrão de projeto Façade**, que simplifica a interação com um subsistema complexo de múltiplos scrapers.

---

## ✨ Funcionalidades Principais

- **Arquitetura Extensível** → Adicione novos scrapers para outros sites sem alterar o código cliente.  
- **Ponto de Entrada Simplificado** → Use a classe `ScrapingFacade` para buscar produtos em todas as fontes com uma única chamada.  
- **Scraping Concorrente** → Utiliza `ThreadPoolExecutor` para raspar múltiplas páginas em paralelo, melhorando a performance.  
- **Suporte a Páginas Dinâmicas** → Emprega o **Playwright** para renderizar sites baseados em JavaScript.  
- **Filtros de Busca** → Permite filtrar por **nome do produto, faixa de preço e localização**.  

---

## 🏗 Arquitetura: O Padrão Façade

O padrão **Façade (Fachada)** fornece uma interface unificada e simplificada para um conjunto de interfaces em um subsistema.  

👉 Em vez de o cliente interagir diretamente com vários scrapers complexos (`OLXScraper`, `MercadoLivreScraper`, etc.), ele se comunica apenas com a `ScrapingFacade`.  

A fachada encapsula toda a complexidade de inicializar, configurar e executar cada scraper, agregando os resultados de todas as fontes antes de retorná-los.

### ✅ Vantagens
- **Baixo Acoplamento**: O cliente é desacoplado dos scrapers específicos.  
- **Simplicidade de Uso**: A complexidade do subsistema é ocultada.  
- **Manutenção Centralizada**: A orquestração dos scrapers fica em um único local.  

---

## 🖥 Exemplo de Uso

```python
from app.facades.scraping_facade import ScrapingFacade

# 1. Instanciar a fachada
facade = ScrapingFacade()

# 2. Realizar a busca de forma unificada
resultados = facade.search_products(
    product_name="PS4",
    state="go",
    min_price=800,
    max_price=1500
)

# 3. Imprimir os resultados consolidados
for produto in resultados:
    print(produto)
```

---

## 📂 Estrutura do Projeto

```
/
├── app/
│   ├── facades/
│   │   └── scraping_facade.py   # A fachada que simplifica a interface
│   ├── models/
│   │   └── product.py           # O modelo de dados do produto
│   ├── scrapers/
│   │   ├── builders/            # Construtores de URL
│   │   ├── interfaces/          # Contratos para os scrapers
│   │   └── olx_scraper.py       # Implementação do scraper da OLX
│   └── services/
│       ├── HttpClient.py        # Cliente para requisições HTTP
│       └── PlaywrightService.py # Serviço para automação com Playwright
├── .env                         # Arquivo de configuração (local)
├── main.py                      # Ponto de entrada da aplicação
└── requirements.txt             # Dependências do projeto
```

---

## ⚙️ Configuração e Execução

### 1. Pré-requisitos
- Python **3.9+**  
- Git  

### 2. Instalação
Clone o repositório e navegue até o diretório:
```bash
git clone <url-do-seu-repositorio>
cd <nome-do-repositorio>
```

Instale as dependências do Python:
```bash
pip install -r requirements.txt
```

Instale os navegadores necessários para o Playwright:
```bash
playwright install
```

### 3. Variáveis de Ambiente
Crie um arquivo chamado **.env** na raiz do projeto e adicione as variáveis necessárias.

Exemplo de `.env`:
```env
# URL base para o scraper da OLX
OLX_SCRAPER_BASE_URL=https://www.olx.com.br
```

### 4. Execução
Para iniciar a aplicação:
```bash
python main.py
```

---

## 🤝 Como Contribuir

Contribuições são **bem-vindas**!  

1. Faça um **fork** do projeto.  
2. Crie uma nova branch:  
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Faça o commit das alterações:  
   ```bash
   git commit -m 'Adiciona nova funcionalidade'
   ```
4. Faça o push para a branch:  
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. Abra um **Pull Request**.  

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**.  
Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
