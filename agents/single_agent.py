"""
Agente único com duas ferramentas (Tavily + ArXiv).
O Gemini decide sozinho qual ferramenta usar para responder.
"""
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from tools import busca_web, busca_arxiv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

system_prompt = """
Atue como um assistente útil com acesso a duas ferramentas:

- busca_web: para notícias, artigos gerais e informações atualizadas da internet.
- busca_arxiv: para pesquisas, estudos e artigos científicos do ArXiv.

Escolha a ferramenta mais adequada para cada pergunta e retorne os links encontrados.
"""

agente = create_react_agent(
    model=llm,
    tools=[busca_web, busca_arxiv],
    prompt=system_prompt
)

if __name__ == "__main__":
    resultado = agente.invoke({
        "messages": [("user", "Quais são os principais impactos da IA na agricultura?")]
    })
    print("\n--- RESPOSTA FINAL ---")
    print(resultado["messages"][-1].content)
