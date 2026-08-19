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

> Projeto de estudo construído durante o **Alura Tech Builder** — do zero até um sistema multi-agente com interface visual, buscas em tempo real na web e em artigos científicos.

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

## 🏗️ Estrutura do projeto

```
📦 projeto/
├── 🚀 app.py                      → ponto de entrada — interface Gradio
├── 📋 requirements.txt            → dependências do projeto
├── 🔐 .env.example                → modelo do arquivo de configuração
│
├── 📁 tools/                      → ferramentas disponíveis para os agentes
│   ├── tavily_tool.py             → busca_web (Tavily — requer API key)
│   └── arxiv_tool.py              → busca_arxiv (ArXiv — gratuito)
│
├── 📁 agents/                     → agentes e pipelines
│   ├── single_agent.py            → agente único com as duas ferramentas
│   ├── multi_agent.py             → pipeline sequencial fixo
│   └── supervisor.py              → supervisor com fluxo dinâmico
│
└── 📁 outputs/                    → exemplos de respostas geradas
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
              │    SUPERVISOR   │  ← cérebro central
              └────────┬────────┘
                       │ decide dinamicamente
          ┌────────────┼────────────┐
          ▼                         ▼
   ┌─────────────┐         ┌─────────────────┐
   │  AGENTE WEB │         │ AGENTE CIENTÍFICO│
   │   (Tavily)  │         │    (ArXiv)       │
   └──────┬──────┘         └────────┬─────────┘
          │                         │
          └───────────┬─────────────┘
                      ▼
             ┌────────────────┐
             │  CONSOLIDADOR  │  ← une as respostas
             └───────┬────────┘
                     ▼
             ┌───────────────┐
             │ RESPOSTA FINAL│
             └───────────────┘
```

---

## 🛠️ Ferramentas

### 🌐 `busca_web` — `tools/tavily_tool.py`

| | |
|---|---|
| API necessária | ✅ Sim — [tavily.com](https://tavily.com) |
| Variável | `TAVILY_API_KEY` |
| Retorna | Título, URL e conteúdo das páginas |

### 🔬 `busca_arxiv` — `tools/arxiv_tool.py`

| | |
|---|---|
| API necessária | ❌ Não — totalmente gratuito |
| Mantido por | Cornell University |
| Retorna | Título, autores, resumo e link do paper |

---

## 🎭 Os agentes

| Arquivo | Tipo | Descrição |
|---|---|---|
| `agents/single_agent.py` | Agente único | Gemini com Tavily + ArXiv, decide sozinho qual usar |
| `agents/multi_agent.py` | Pipeline fixo | Fluxo sequencial: web → científico → consolida |
| `agents/supervisor.py` | Supervisor dinâmico | Supervisor decide o fluxo em tempo real |

---

## 👑 Pipeline fixo vs Supervisor

| | Pipeline fixo | Supervisor |
|---|---|---|
| Fluxo | Sempre igual | Dinâmico |
| Quem decide | Você (no código) | O LLM |
| Eficiência | Executa tudo sempre | Só o necessário |
| Complexidade | Simples | Avançado |

---

## 🚀 Como rodar

### 1. Clone o repositório
```bash
git clone https://github.com/victorsitta/SALVAR-CRIANDO-FERRAMENTAS-E-A-GENTE-PARA-MIM-LANGCHAIN-E-LANGGRAPH.git
cd SALVAR-CRIANDO-FERRAMENTAS-E-A-GENTE-PARA-MIM-LANGCHAIN-E-LANGGRAPH
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o `.env`
```bash
cp .env.example .env
# edite o .env com suas chaves de API
```

```env
GOOGLE_API_KEY=sua_chave_aqui
GEMINI_API_KEY=sua_chave_aqui
TAVILY_API_KEY=sua_chave_aqui
```

### 4. Execute

```bash
# Interface visual (recomendado)
python app.py

# Supervisor no terminal
python agents/supervisor.py

# Pipeline multi-agente fixo
python agents/multi_agent.py

# Agente único
python agents/single_agent.py

# Testar ferramentas isoladas
python tools/tavily_tool.py
python tools/arxiv_tool.py
```

---

## 📚 Conceitos aprendidos

| Conceito | Descrição |
|---|---|
| **LLM** | O cérebro — modelo de linguagem (Gemini) |
| **Ferramenta** | Capacidade extra que o LLM pode acionar |
| **Agente** | LLM + ferramentas + autonomia de decisão |
| **Grafo** | Fluxo de execução entre agentes (LangGraph) |
| **Estado** | Memória compartilhada entre os nós do grafo |
| **Supervisor** | Agente central que orquestra os outros |

---

## ⚠️ Problema resolvido no caminho

O `langchain-community` quebrou ao usar `ArxivQueryRun`:

```
AttributeError: 'Search' object has no attribute 'results'
```

**Causa:** incompatibilidade entre `langchain-community` e a versão nova do pacote `arxiv`.

**Solução:** usar o pacote `arxiv` diretamente com `Client().results(search)` e criar a ferramenta manualmente com `@tool`.

> Lição: verificar sempre se existe um pacote standalone antes de usar `langchain-community`.

---

<div align="center">

**Construído durante o Alura Tech Builder** 🚀

![Made with Love](https://img.shields.io/badge/Feito_com-Curiosidade_%26_Café-FF6B6B?style=for-the-badge)

</div>
