import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from TavilyBusca import busca_web
from arxiv_tool import busca_arxiv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configura a chave do Gemini
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Cria o modelo Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# --- Define o estado compartilhado entre os agentes ---
class AgentState(TypedDict):
    user_query: str
    web_answer: str
    scientific_answer: str
    final_answer: str


# --- Agente Web (Tavily) ---
def funcao_agente_web(state: AgentState) -> dict:
    """
    Busca informações atualizadas na web usando Tavily.
    """
    system_prompt = """Atue como um assistente útil.
    Use as ferramentas fornecidas para responder às perguntas do usuário.
    - busca_web: Retorna os resultados de uma busca na web.
    Use a busca_web sempre que o usuário fizer uma pergunta sobre um tema específico
    e retorne os links dos artigos na resposta.
    """

    agente_web = create_react_agent(
        model=llm,
        tools=[busca_web],
        prompt=system_prompt
    )

    resultado = agente_web.invoke({
        "messages": [("user", state["user_query"])]
    })

    resposta = resultado["messages"][-1].content
    if isinstance(resposta, list):
        resposta = " ".join(b["text"] for b in resposta if isinstance(b, dict) and b.get("type") == "text")

    return {"web_answer": resposta}


# --- Agente Científico (ArXiv) ---
def funcao_agente_cientifico(state: AgentState) -> dict:
    """
    Busca artigos científicos no ArXiv.
    """
    system_prompt = """Atue como um assistente de pesquisa científica.
    Use as ferramentas fornecidas para responder às perguntas do usuário.
    - busca_arxiv: Retorna artigos científicos do ArXiv.
    Use a busca_arxiv sempre que o usuário fizer uma pergunta sobre um
    tema específico e retorne o título dos artigos na resposta.
    """

    agente_cientifico = create_react_agent(
        model=llm,
        tools=[busca_arxiv],
        prompt=system_prompt
    )

    resultado = agente_cientifico.invoke({
        "messages": [("user", state["user_query"])]
    })

    resposta = resultado["messages"][-1].content
    if isinstance(resposta, list):
        resposta = " ".join(b["text"] for b in resposta if isinstance(b, dict) and b.get("type") == "text")

    return {"scientific_answer": resposta}


# --- Agente Consolidador ---
def funcao_agente_consolidador(state: AgentState) -> dict:
    """
    Lê as respostas do agente web e científico e gera uma resposta final consolidada.
    """
    prompt_consolidacao = f"""
    Você é um assistente especialista em síntese de informações.

    Com base nas informações abaixo, gere uma resposta completa, clara e organizada
    para a seguinte pergunta do usuário: {state["user_query"]}

    --- INFORMAÇÕES DA WEB ---
    {state["web_answer"]}

    --- ARTIGOS CIENTÍFICOS ---
    {state["scientific_answer"]}

    Combine as duas fontes em uma resposta única e bem estruturada,
    destacando os pontos mais importantes de cada uma.
    """

    resposta = llm.invoke([HumanMessage(content=prompt_consolidacao)])
    conteudo = resposta.content

    if isinstance(conteudo, list):
        conteudo = " ".join(b["text"] for b in conteudo if isinstance(b, dict) and b.get("type") == "text")

    return {"final_answer": conteudo}


# --- Monta o grafo LangGraph ---
grafo = StateGraph(AgentState)

# Adiciona os nós
grafo.add_node("agente_web", funcao_agente_web)
grafo.add_node("agente_cientifico", funcao_agente_cientifico)
grafo.add_node("agente_consolidador", funcao_agente_consolidador)

# Define o ponto de entrada
grafo.set_entry_point("agente_web")

# Define a ordem de execução
grafo.add_edge("agente_web", "agente_cientifico")
grafo.add_edge("agente_cientifico", "agente_consolidador")
grafo.add_edge("agente_consolidador", END)

# Compila o grafo
pipeline = grafo.compile()


# --- Execução ---
if __name__ == "__main__":
    resultado = pipeline.invoke({
        "user_query": "Quais são os principais impactos da IA na agricultura?",
        "web_answer": "",
        "scientific_answer": "",
        "final_answer": ""
    })

    print("\n--- RESPOSTA FINAL CONSOLIDADA ---")
    print(resultado["final_answer"])
