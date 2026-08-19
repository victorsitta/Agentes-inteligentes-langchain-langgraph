import os
from typing import TypedDict, Literal

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Importa as ferramentas já criadas
from TavilyBusca import busca_web
from arxiv_tool import busca_arxiv

# -------------------------------------------------------
# CONFIGURAÇÃO INICIAL
# -------------------------------------------------------

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configura a chave do Google para o Gemini
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Cria o modelo Gemini que será usado por todos os agentes
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# -------------------------------------------------------
# ESTADO COMPARTILHADO
# O estado é como uma "memória" que passa entre os agentes.
# Cada agente pode ler e escrever nesse estado.
# -------------------------------------------------------

class AgentState(TypedDict):
    user_query: str        # Pergunta original do usuário
    web_answer: str        # Resposta do agente web (Tavily)
    scientific_answer: str # Resposta do agente científico (ArXiv)
    final_answer: str      # Resposta final consolidada
    next: str              # Próximo agente a ser chamado (decidido pelo supervisor)


# -------------------------------------------------------
# AGENTE WEB
# Responsável por buscar informações atualizadas na internet
# usando a ferramenta Tavily.
# -------------------------------------------------------

def funcao_agente_web(state: AgentState) -> dict:

    agente_web = create_react_agent(
        model=llm,
        tools=[busca_web],
        prompt="""Você é um assistente de busca na web.
        Use a ferramenta busca_web para encontrar informações
        atualizadas sobre o tema solicitado.
        Retorne um resumo com os principais pontos e os links encontrados."""
    )

    resultado = agente_web.invoke({
        "messages": [("user", state["user_query"])]
    })

    resposta = resultado["messages"][-1].content

    # Trata o caso do Gemini retornar lista em vez de string
    if isinstance(resposta, list):
        resposta = " ".join(
            b["text"] for b in resposta
            if isinstance(b, dict) and b.get("type") == "text"
        )

    return {"web_answer": resposta}


# -------------------------------------------------------
# AGENTE CIENTÍFICO
# Responsável por buscar artigos acadêmicos no ArXiv.
# -------------------------------------------------------

def funcao_agente_cientifico(state: AgentState) -> dict:

    agente_cientifico = create_react_agent(
        model=llm,
        tools=[busca_arxiv],
        prompt="""Você é um assistente de pesquisa científica.
        Use a ferramenta busca_arxiv para encontrar artigos
        acadêmicos relevantes sobre o tema solicitado.
        Retorne os títulos, autores e um breve resumo de cada artigo."""
    )

    resultado = agente_cientifico.invoke({
        "messages": [("user", state["user_query"])]
    })

    resposta = resultado["messages"][-1].content

    # Trata o caso do Gemini retornar lista em vez de string
    if isinstance(resposta, list):
        resposta = " ".join(
            b["text"] for b in resposta
            if isinstance(b, dict) and b.get("type") == "text"
        )

    return {"scientific_answer": resposta}


# -------------------------------------------------------
# AGENTE CONSOLIDADOR
# Lê as respostas dos outros agentes e gera uma resposta
# final completa e organizada para o usuário.
# -------------------------------------------------------

def funcao_agente_consolidador(state: AgentState) -> dict:

    # Monta o prompt com as informações coletadas pelos outros agentes
    prompt = f"""
    Você é um assistente especialista em síntese de informações.

    Pergunta do usuário: {state["user_query"]}

    --- INFORMAÇÕES DA WEB ---
    {state["web_answer"] or "Nenhuma informação da web disponível."}

    --- ARTIGOS CIENTÍFICOS ---
    {state["scientific_answer"] or "Nenhum artigo científico disponível."}

    Com base nas informações acima, gere uma resposta completa, clara
    e bem organizada. Combine as duas fontes e destaque os pontos
    mais importantes.
    """

    resposta = llm.invoke([HumanMessage(content=prompt)])
    conteudo = resposta.content

    # Trata o caso do Gemini retornar lista em vez de string
    if isinstance(conteudo, list):
        conteudo = " ".join(
            b["text"] for b in conteudo
            if isinstance(b, dict) and b.get("type") == "text"
        )

    return {"final_answer": conteudo}


# -------------------------------------------------------
# SUPERVISOR
# É o agente central e mais importante do sistema.
# Ele analisa o estado atual e decide qual agente
# deve ser chamado a seguir — ou se já é hora de encerrar.
#
# Fluxo de decisão:
#   - Nenhuma busca feita ainda → chama agente_web
#   - Web feita mas sem artigos → chama agente_cientifico
#   - Ambas as buscas feitas → chama agente_consolidador
#   - Resposta final pronta → encerra (FINISH)
# -------------------------------------------------------

def supervisor(state: AgentState) -> dict:

    # Se ainda não buscou na web, começa por aí
    if not state.get("web_answer"):
        return {"next": "agente_web"}

    # Se já tem a web mas não tem os artigos científicos, busca no ArXiv
    if not state.get("scientific_answer"):
        return {"next": "agente_cientifico"}

    # Se já tem as duas buscas, consolida a resposta final
    if not state.get("final_answer"):
        return {"next": "agente_consolidador"}

    # Tudo pronto, encerra o fluxo
    return {"next": "FINISH"}


# -------------------------------------------------------
# ROTEADOR
# Função auxiliar que lê o campo "next" do estado
# e direciona o grafo para o próximo nó correto.
# O supervisor escreve em "next", o roteador lê e executa.
# -------------------------------------------------------

def roteador(state: AgentState) -> Literal["agente_web", "agente_cientifico", "agente_consolidador", "__end__"]:
    proximo = state.get("next", "FINISH")
    if proximo == "FINISH":
        return "__end__"
    return proximo


# -------------------------------------------------------
# MONTAGEM DO GRAFO
# Aqui conectamos todos os nós e definimos como o fluxo
# se move entre eles.
# -------------------------------------------------------

grafo = StateGraph(AgentState)

# Adiciona cada agente como um nó do grafo
grafo.add_node("supervisor", supervisor)
grafo.add_node("agente_web", funcao_agente_web)
grafo.add_node("agente_cientifico", funcao_agente_cientifico)
grafo.add_node("agente_consolidador", funcao_agente_consolidador)

# O supervisor é o ponto de entrada — sempre começa por ele
grafo.set_entry_point("supervisor")

# Após cada agente terminar, volta para o supervisor decidir o próximo passo
grafo.add_edge("agente_web", "supervisor")
grafo.add_edge("agente_cientifico", "supervisor")
grafo.add_edge("agente_consolidador", "supervisor")

# O supervisor usa o roteador para decidir o próximo nó
grafo.add_conditional_edges("supervisor", roteador)

# Compila o grafo em um pipeline executável
pipeline = grafo.compile()


# -------------------------------------------------------
# EXECUÇÃO
# Só roda quando o arquivo é executado diretamente.
# -------------------------------------------------------

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
