import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# Importa as ferramentas
from TavilyBusca import busca_web
from arxiv_tool import busca_arxiv


# Carrega as variáveis do arquivo .env
load_dotenv()

# Configura a chave do Gemini
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# Cria o modelo Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


# Lista de ferramentas disponíveis para o agente
# A busca_web utiliza o Tavily e a busca_arxiv utiliza o ArXiv
tools = [busca_web, busca_arxiv]


# Instruções do agente
system_prompt = """
Atue como um assistente útil.

Use as ferramentas fornecidas para responder às perguntas do usuário.

- busca_web: Retorna resultados de uma busca na web. Use para notícias, artigos gerais e informações atualizadas.
- busca_arxiv: Busca artigos científicos no ArXiv. Use quando o usuário pedir pesquisas ou estudos científicos.

Use a busca_web sempre que o usuário fizer uma pergunta
sobre um tema específico e retorne os links dos artigos
na resposta.
"""


# Cria o agente ReAct
agente_web = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt
)


# Envia uma pergunta para o agente
resultado = agente_web.invoke({
    "messages": [
        ("user", "Quais são os principais impactos da IA na agricultura?")
    ]
})


# Mostra a resposta final
print("\n--- RESPOSTA FINAL ---")
print(resultado["messages"][-1].content)