"""
Supervisor multi-agente com fluxo dinâmico.
O supervisor decide em tempo real qual agente chamar a seguir,
baseado no estado atual da conversa.

Fluxo:
  Supervisor → agente_web → Supervisor → agente_cientifico → Supervisor → consolidador → FIM
"""
import os
from typing import TypedDict, Literal

from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from tools import busca_web, busca_arxiv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


# Estado compartilhado entre todos os agentes
class AgentState(TypedDict):
    user_query: str         # Pergunta original do usuário
    web_answer: str         # Resposta do agente web
    scientific_answer: str  # Resposta do agente científico
    final_answer: str       # Resposta final consolidada
    next: str               # Próximo nó (decidido pelo supervisor)


def funcao_agente_web(state: AgentState) -> dict:
    agente = create_react_agent(
        model=llm,
        tools=[busca_web],
        prompt="Busque informações atualizadas na web. Retorne resumo e links."
    )
    resultado = agente.invoke({"messages": [("user", state["user_query"])]})
    resposta = resultado["messages"][-1].content
    if isinstance(resposta, list):
        resposta = " ".join(b["text"] for b in resposta if isinstance(b, dict) and b.get("type") == "text")
    return {"web_answer": resposta}


def funcao_agente_cientifico(state: AgentState) -> dict:
    agente = create_react_agent(
        model=llm,
        tools=[busca_arxiv],
        prompt="Busque artigos científicos no ArXiv. Retorne títulos, autores e resumos."
    )
    resultado = agente.invoke({"messages": [("user", state["user_query"])]})
    resposta = resultado["messages"][-1].content
    if isinstance(resposta, list):
        resposta = " ".join(b["text"] for b in resposta if isinstance(b, dict) and b.get("type") == "text")
    return {"scientific_answer": resposta}


def funcao_agente_consolidador(state: AgentState) -> dict:
    prompt = f"""
    Você é um especialista em síntese de informações.

    Pergunta: {state["user_query"]}

    --- INFORMAÇÕES DA WEB ---
    {state["web_answer"] or "Nenhuma informação da web disponível."}

    --- ARTIGOS CIENTÍFICOS ---
    {state["scientific_answer"] or "Nenhum artigo científico disponível."}

    Combine as duas fontes em uma resposta completa, clara e bem estruturada.
    """
    resposta = llm.invoke([HumanMessage(content=prompt)])
    conteudo = resposta.content
    if isinstance(conteudo, list):
        conteudo = " ".join(b["text"] for b in conteudo if isinstance(b, dict) and b.get("type") == "text")
    return {"final_answer": conteudo}


def supervisor(state: AgentState) -> dict:
    """Decide qual agente chamar a seguir baseado no estado atual."""
    if not state.get("web_answer"):
        return {"next": "agente_web"}
    if not state.get("scientific_answer"):
        return {"next": "agente_cientifico"}
    if not state.get("final_answer"):
        return {"next": "agente_consolidador"}
    return {"next": "FINISH"}


def roteador(state: AgentState) -> Literal["agente_web", "agente_cientifico", "agente_consolidador", "__end__"]:
    """Lê o campo 'next' e direciona o grafo para o próximo nó."""
    proximo = state.get("next", "FINISH")
    return "__end__" if proximo == "FINISH" else proximo


# Monta o grafo
grafo = StateGraph(AgentState)
grafo.add_node("supervisor", supervisor)
grafo.add_node("agente_web", funcao_agente_web)
grafo.add_node("agente_cientifico", funcao_agente_cientifico)
grafo.add_node("agente_consolidador", funcao_agente_consolidador)
grafo.set_entry_point("supervisor")
grafo.add_edge("agente_web", "supervisor")
grafo.add_edge("agente_cientifico", "supervisor")
grafo.add_edge("agente_consolidador", "supervisor")
grafo.add_conditional_edges("supervisor", roteador)

# Pipeline exportável para outros módulos (ex: app.py)
pipeline = grafo.compile()


if __name__ == "__main__":
    print("Iniciando pipeline com supervisor...\n")
    resultado = pipeline.invoke({
        "user_query": "Quais são os principais impactos da IA na agricultura?",
        "web_answer": "",
        "scientific_answer": "",
        "final_answer": "",
        "next": ""
    })
    print("\n--- RESPOSTA FINAL CONSOLIDADA ---")
    print(resultado["final_answer"])
