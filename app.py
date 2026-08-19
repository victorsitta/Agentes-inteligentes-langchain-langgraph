"""
Ponto de entrada principal — Interface visual com Gradio.
Conecta o supervisor multi-agente a uma interface web acessível em http://localhost:7860
"""
import gradio as gr
from agents.supervisor import pipeline


def run_graph(user_query: str) -> str:
    """
    Executa o pipeline do supervisor com a pergunta do usuário
    e retorna a resposta final consolidada.
    """
    resultado = pipeline.invoke({
        "user_query": user_query,
        "web_answer": "",
        "scientific_answer": "",
        "final_answer": "",
        "next": ""
    })
    return resultado["final_answer"]


iface = gr.Interface(
    fn=run_graph,
    inputs=gr.Textbox(
        label="Digite sua pergunta:",
        placeholder="Ex: Quais os impactos da IA na medicina?"
    ),
    outputs=gr.Markdown(label="Resposta Final:"),
    title="🤖 Agente de Pesquisa com LangGraph",
    description="Faça uma pergunta e obtenha uma resposta consolidada com fontes da web (Tavily) e artigos científicos (ArXiv).",
    examples=[
        ["Quais são os principais impactos da IA na agricultura?"],
        ["Como machine learning está sendo usado na medicina?"],
        ["Quais os avanços recentes em energia renovável?"]
    ]
)

if __name__ == "__main__":
    iface.launch()
