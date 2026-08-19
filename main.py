import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configura as chaves
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Cria o modelo Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Cria a ferramenta de busca na web com Tavily
@tool
def busca_web(query: str) -> list:
    """
    Busca informações atualizadas na internet sobre um tema específico.
    Use esta ferramenta sempre que precisar de dados recentes ou externos.
    """
    tavily_search = TavilySearch(
        max_results=3,
        search_depth="advanced"
    )
    return tavily_search.invoke(query)

# Lista de ferramentas disponíveis para o agente
ferramentas = [busca_web]

# Cria o prompt do agente
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente inteligente. Use a ferramenta de busca para encontrar informações atualizadas antes de responder."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Cria o agente com suporte a ferramentas
agente = create_tool_calling_agent(llm, ferramentas, prompt)

# Cria o executor do agente
executor = AgentExecutor(agent=agente, tools=ferramentas, verbose=True)

# Executa o agente com uma pergunta
resposta = executor.invoke({
    "input": "Quais são os principais impactos da IA na Agricultura?"
})

print("\n--- RESPOSTA FINAL ---")
print(resposta["output"])
