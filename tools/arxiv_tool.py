import os
import arxiv
from dotenv import load_dotenv

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Carrega as variáveis do arquivo .env
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


@tool
def busca_arxiv(query: str) -> str:
    """
    Busca artigos científicos no ArXiv sobre um tema específico.
    Use esta ferramenta quando o usuário perguntar sobre pesquisas,
    estudos ou artigos científicos.
    Não requer chave de API — totalmente gratuito.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance
    )

    resultados = []
    for paper in client.results(search):
        resultados.append(
            f"Título: {paper.title}\n"
            f"Autores: {', '.join(a.name for a in paper.authors[:3])}\n"
            f"Resumo: {paper.summary[:500]}...\n"
            f"Link: {paper.entry_id}\n"
        )

    if not resultados:
        return "Nenhum artigo encontrado."

    return "\n---\n".join(resultados)


# Teste independente — só roda ao executar este arquivo diretamente
if __name__ == "__main__":
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    system_prompt = """
    Atue como um assistente de pesquisa científica.
    Use a ferramenta busca_arxiv para encontrar artigos sobre o tema solicitado.
    Retorne os títulos dos artigos encontrados.
    """

    agente = create_react_agent(model=llm, tools=[busca_arxiv], prompt=system_prompt)

    resultado = agente.invoke({
        "messages": [("user", "AI impact in agriculture")]
    })

    resposta = resultado["messages"][-1].content
    if isinstance(resposta, list):
        for bloco in resposta:
            if isinstance(bloco, dict) and bloco.get("type") == "text":
                print(bloco["text"])
    else:
        print(resposta)
