"""
Pipeline multi-agente com fluxo fixo e sequencial:
agente_web → agente_cientifico → consolidador
"""
import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from tools import busca_web, busca_arxiv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


class AgentState(TypedDict):
    user_query: str
    web_answer: str
    scientific_answer: str
    final_answer: str


def funcao_agente_web(state: AgentState) -> dict:
    agente = create_react_agent(
        model=llm,
        tools=[busca_web],
        prompt="Busque informações atualizadas na web sobre o tema solicitado. Retorne os links encontrados."
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
        prompt="Busque artigos científicos no ArXiv sobre o tema solicitado. Retorne os títulos e resumos."
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
    {state["web_answer"]}

    --- ARTIGOS CIENTÍFICOS ---
    {state["scientific_answer"]}

    Combine as duas fontes em uma resposta única, clara e bem estruturada.
    """
    resposta = llm.invoke([HumanMessage(content=prompt)])
    conteudo = resposta.content
    if isinstance(conteudo, list):
        conteudo = " ".join(b["text"] for b in conteudo if isinstance(b, dict) and b.get("type") == "text")
    return {"final_answer": conteudo}


# Monta o grafo
grafo = StateGraph(AgentState)
grafo.add_node("agente_web", funcao_agente_web)
grafo.add_node("agente_cientifico", funcao_agente_cientifico)
grafo.add_node("agente_consolidador", funcao_agente_consolidador)
grafo.set_entry_point("agente_web")
grafo.add_edge("agente_web", "agente_cientifico")
grafo.add_edge("agente_cientifico", "agente_consolidador")
grafo.add_edge("agente_consolidador", END)
pipeline = grafo.compile()


if __name__ == "__main__":
    resultado = pipeline.invoke({
        "user_query": "Quais são os principais impactos da IA na agricultura?",
        "web_answer": "",
        "scientific_answer": "",
        "final_answer": ""
    })
    print("\n--- RESPOSTA FINAL CONSOLIDADA ---")
    print(resultado["final_answer"])
