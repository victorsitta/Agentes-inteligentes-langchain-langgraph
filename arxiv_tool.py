import os
import arxiv
from dotenv import load_dotenv

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configura a chave do Gemini
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# Ferramenta pronta para o agente usar
@tool
def busca_arxiv(query: str) -> str:
    """
    Busca artigos científicos no ArXiv sobre um tema específico.
    Use esta ferramenta quando o usuário perguntar sobre pesquisas,
    estudos ou artigos científicos.
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


# ---------------------------------------------------------
# Teste independente — só roda ao executar este arquivo
# diretamente, não quando importado por outro módulo
# ---------------------------------------------------------
if __name__ == "__main__":

    # Modelo Gemini para o agente de teste
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    # Instruções do agente de teste
    system_prompt = """
    Atue como um assistente de pesquisa científica.

    Use a ferramenta fornecida para responder às perguntas do usuário.

    - busca_arxiv: realiza buscas de artigos científicos no ArXiv.

    Use a busca_arxiv sempre que o usuário fizer uma pergunta
    sobre um tema científico e retorne os títulos dos artigos encontrados.
    """

    # Cria o agente de teste usando apenas o ArXiv
    agente_cientifico = create_react_agent(
        model=llm,
        tools=[busca_arxiv],
        prompt=system_prompt
    )

    # Executa o teste
    resultado = agente_cientifico.invoke({
        "messages": [
            ("user", "AI impact in agriculture")
        ]
    })

    print("\n--- RESPOSTA DO AGENTE CIENTÍFICO ---")
    resposta = resultado["messages"][-1].content
    # Trata resposta em formato de lista (Gemini 2.5 pode retornar assim)
    if isinstance(resposta, list):
        for bloco in resposta:
            if isinstance(bloco, dict) and bloco.get("type") == "text":
                print(bloco["text"])
    else:
        print(resposta)
