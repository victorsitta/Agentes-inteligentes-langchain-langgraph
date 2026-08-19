import os
from dotenv import load_dotenv

from langchain_tavily import TavilySearch # Ferramenta que permite pesquisar informações na internet
from langchain_core.tools import tool # Transforma uma função Python em uma ferramenta que o agente pode usar

# Carrega as variáveis do arquivo .env
load_dotenv()

# Cria uma ferramenta de busca na web
@tool
def busca_web(query: str) -> list:
    """
    Busca na web por um termo específico.
    """
    
    # Cria o mecanismo de busca Tavily
    tavily_search = TavilySearch(
        max_results=2,
        search_depth="advanced"
    )

    # Executa a pesquisa
    resultado_busca = tavily_search.invoke(query)

    # Retorna os resultados encontrados
    return resultado_busca


# Teste independente — só roda ao executar este arquivo diretamente,
# não quando importado por outro módulo
if __name__ == "__main__":

    resultado = busca_web.invoke("IA na Agricultura")

    for item in resultado["results"]:
        print("Título:", item["title"])
        print("URL:", item["url"])
        print("Conteúdo:", item["content"])
        print("-" * 80)