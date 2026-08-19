<div align="center">

# 🤖 Agentes Inteligentes com LangChain & LangGraph

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=00D9FF&center=true&vCenter=true&width=600&lines=Agentes+com+LangChain+%2B+LangGraph;Busca+Web+com+Tavily;Artigos+Cient%C3%ADficos+com+ArXiv;Interface+visual+com+Gradio;Supervisor+Multi-Agente" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-FF6B6B?style=for-the-badge&logo=graph&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)

<br/>

> **Projeto de estudo** construído durante o Alura Tech Builder — do zero até um sistema multi-agente com interface visual, buscas em tempo real na web e em artigos científicos.

</div>

---

## 🧠 O que foi construído

Um sistema de **agentes de inteligência artificial** que combina:

- 🌐 **Busca na web em tempo real** via Tavily
- 🔬 **Busca de artigos científicos** via ArXiv (sem API key)
- 🤖 **Raciocínio e respostas** via Google Gemini 2.5 Flash
- 🎛️ **Orquestração inteligente** com LangGraph
- 🖥️ **Interface visual** com Gradio

---

## 🏗️ Arquitetura do projeto

```
📦 APRENDENDO - Criar Agente LLM
├── 🔧 TavilyBusca.py         → Ferramenta de busca na web
├── 🔬 arxiv_tool.py           → Ferramenta de busca científica
├── 🤖 agente_react.py         → Agente único com as duas ferramentas
├── 🔀 usando_varios_agentes.py → Pipeline com 3 agentes em sequência
├── 👑 supervisor.py            → Supervisor inteligente multi-agente
├── 🖥️  Vizualizacao.py         → Interface Gradio
├── 🧪 main.py                  → Teste inicial com Gemini
├── 🔐 .env                     → Chaves de API (não enviado ao GitHub)
└── 📁 outputs/
    └── agricultura/
        └── impactos_ia_agricultura.md
```

---

## 🔄 Como o sistema funciona

### Fluxo do Supervisor

```
         ┌─────────────────────────────────────┐
         │           USUÁRIO PERGUNTA           │
         └──────────────┬──────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │    SUPERVISOR   │ ← cérebro central
              └────────┬────────┘
                       │ decide
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌─────────────┐           ┌─────────────────┐
   │  AGENTE WEB │           │ AGENTE CIENTÍFICO│
   │   (Tavily)  │           │    (ArXiv)       │
   └──────┬──────┘           └────────┬─────────┘
          │                           │
          └───────────┬───────────────┘
                      ▼
             ┌────────────────┐
             │  CONSOLIDADOR  │ ← une as respostas
             └───────┬────────┘
                     │
                     ▼
             ┌───────────────┐
             │ RESPOSTA FINAL│
             └───────────────┘
```

---

## 🛠️ Ferramentas criadas

### 🌐 `busca_web` — TavilyBusca.py

Busca informações atualizadas na internet usando a API do Tavily.

```python
@tool
def busca_web(query: str) -> list:
    """Busca na web por um termo específico."""
    tavily_search = TavilySearch(max_results=2, search_depth="advanced")
    return tavily_search.invoke(query)
```

| Propriedade | Detalhe |
|---|---|
| API necessária | ✅ Sim — [tavily.com](https://tavily.com) |
| Variável no .env | `TAVILY_API_KEY` |
| Retorna | Título, URL e conteúdo das páginas |

---

### 🔬 `busca_arxiv` — arxiv_tool.py

Busca artigos científicos diretamente no repositório ArXiv.

```python
@tool
def busca_arxiv(query: str) -> str:
    """Busca artigos científicos no ArXiv."""
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=3)
    for paper in client.results(search):
        # retorna título, autores, resumo e link
```

| Propriedade | Detalhe |
|---|---|
| API necessária | ❌ Não — totalmente gratuito |
| Mantido por | Cornell University |
| Retorna | Título, autores, resumo e link do paper |

---

## 🎭 Os agentes

| Arquivo | Tipo | Ferramentas | Descrição |
|---|---|---|---|
| `main.py` | Cadeia simples | Nenhuma | Primeira versão — só Gemini com prompt |
| `agente_react.py` | Agente ReAct | Tavily + ArXiv | Agente único com duas ferramentas |
| `usando_varios_agentes.py` | Multi-agente fixo | Tavily + ArXiv | Fluxo sequencial fixo com consolidador |
| `supervisor.py` | Multi-agente dinâmico | Tavily + ArXiv | Supervisor decide o fluxo em tempo real |

---

## 👑 Supervisor vs Pipeline fixo

| | Pipeline fixo | Supervisor |
|---|---|---|
| Fluxo | Sempre igual | Dinâmico |
| Decisão | Você | O LLM |
| Eficiência | Executa tudo | Só o necessário |
| Complexidade | Simples | Avançado |

---

## 🖥️ Interface visual

O `Vizualizacao.py` conecta o supervisor a uma interface web usando Gradio:

```python
iface = gr.Interface(
    fn=run_graph,
    inputs=gr.Textbox(label="Digite sua pergunta:"),
    outputs=gr.Markdown(label="Resposta Final:"),
    title="Agente de Pesquisa com LangGraph"
)
iface.launch()  # abre em http://localhost:7860
```

---

## 🚀 Como rodar

### 1. Clone o repositório
```bash
git clone https://github.com/victorsitta/SALVAR-CRIANDO-FERRAMENTAS-E-A-GENTE-PARA-MIM-LANGCHAIN-E-LANGGRAPH.git
```

### 2. Instale as dependências
```bash
pip install langchain langchain-google-genai langchain-tavily arxiv python-dotenv gradio langgraph
```

### 3. Configure o `.env`
```env
GOOGLE_API_KEY=sua_chave_aqui
GEMINI_API_KEY=sua_chave_aqui
TAVILY_API_KEY=sua_chave_aqui
```

### 4. Execute

```bash
# Interface visual (recomendado)
python Vizualizacao.py

# Supervisor no terminal
python supervisor.py

# Agente único
python agente_react.py

# Testar ferramenta ArXiv
python arxiv_tool.py

# Testar ferramenta Tavily
python TavilyBusca.py
```

---

## 📚 Conceitos aprendidos

```
LLM          → o cérebro (Gemini)
Ferramenta   → capacidade extra que o LLM pode usar
Agente       → LLM + ferramentas + autonomia de decisão
Grafo        → fluxo de execução entre agentes
Supervisor   → agente central que orquestra os outros
Estado       → memória compartilhada entre os agentes
```

---

## ⚠️ Problema encontrado no caminho

O `langchain-community` estava sendo usado para o ArXiv mas quebrou por incompatibilidade com versões novas do pacote `arxiv`:

```
AttributeError: 'Search' object has no attribute 'results'
```

**Solução:** abandonar o `langchain-community` e usar o pacote `arxiv` diretamente com `Client().results(search)`.

> Lição: sempre verificar se existe um pacote standalone mais atualizado antes de usar `langchain-community`.

---

<div align="center">

**Construído durante o Alura Tech Builder** 🚀

![Made with Love](https://img.shields.io/badge/Feito_com-Curiosidade_%26_Café-FF6B6B?style=for-the-badge)

</div>
