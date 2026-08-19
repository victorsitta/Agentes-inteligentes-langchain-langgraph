import gradio as gr

# Importa o pipeline do supervisor já pronto
from supervisor import pipeline


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


# Cria a interface Gradio
iface = gr.Interface(
    fn=run_graph,
    inputs=gr.Textbox(label="Digite sua pergunta:"),
    outputs=gr.Markdown(label="Resposta Final:"),
    title="Agente de Pesquisa com LangGraph",
    description="Faça uma pergunta e obtenha uma resposta consolidada com fontes da web e artigos científicos."
)

# Inicia a interface
iface.launch()
