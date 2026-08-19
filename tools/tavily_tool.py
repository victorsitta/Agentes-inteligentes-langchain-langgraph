import os
from dotenv import load_dotenv

from langchain_tavily import TavilySearch
from langchain_core.tools import tool

# Carrega as variáveis do arquivo .env
load_dotenv()


@tool
def busca_web(query: str) -> list:
    """
    Busca na web por um termo específico.
    Use esta ferramenta para encontrar informações atualizadas na internet.
    """
    tavily_search = TavilySearch(
        max_results=2,
        search_depth="advanced"
    )
    return tavily_search.invoke(query)


# Teste independente — só roda ao executar este arquivo diretamente
if __name__ == "__main__":
    resultado = busca_web.invoke("IA na Agricultura")
    for item in resultado["results"]:
        print("Título:", item["title"])
        print("URL:", item["url"])
        print("Conteúdo:", item["content"])
        print("-" * 80)
