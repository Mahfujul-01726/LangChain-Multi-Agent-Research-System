# LangChain Multi-Agent Research System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python 3.11+"/>
  <img src="https://img.shields.io/badge/LangChain-0.2+-green?logo=langchain" alt="LangChain"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-blue" alt="OpenAI GPT-4o-mini"/>
  <img src="https://img.shields.io/badge/Streamlit-UI-red" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/License-Apache--2.0-blue" alt="License"/>
</p>

<p align="center">
  An autonomous, multi-agent research system built with LangChain that searches the web, extracts deep content, writes structured reports, and evaluates its own output — end to end.
</p>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Agent Responsibilities](#agent-responsibilities)
- [How It Works](#how-it-works)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Output](#output)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**LangChain Multi-Agent Research System** orchestrates four specialized AI components to produce polished, well-sourced research reports on any topic:

1. A **Search Agent** discovers relevant, up-to-date web results.
2. A **Reader Agent** scrapes and extracts clean, readable content from the most relevant sources.
3. A **Writer Chain** synthesizes the gathered research into a structured, professional report.
4. A **Critic Chain** reviews the report, assigns a quality score, and provides concrete improvement feedback.

The pipeline is exposed through two interfaces: an interactive, fully-styled **Streamlit web app** and a lightweight **CLI script**.

---

## Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent Orchestration** | Dedicated agents for searching, reading, writing, and critiquing, coordinated through a single pipeline |
| 🔍 **Automated Web Research** | Real-time web search powered by the Tavily API |
| 📄 **Resilient Content Extraction** | Three-tier scraping pipeline with graceful fallbacks (trafilatura → readability → raw HTML) |
| ✍️ **AI Report Generation** | Structured reports with introduction, key findings, conclusion, and cited sources |
| 🧐 **Self-Evaluation** | Built-in critic that scores reports from 1–10 and lists strengths and improvement areas |
| 🖥️ **Interactive UI** | Custom-designed Streamlit interface with live pipeline status and report downloads |
| 🧩 **Modular Design** | Clean separation between agents, tools, and pipelines for easy extension |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Interfaces (app.py / main.py)           │
│            Streamlit UI  ·  CLI Entry Point              │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────┐
│          Research Pipeline (pipeline.py)                 │
│          Sequential multi-agent orchestration            │
└──────────────────────────┬───────────────────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
┌─────▼─────┐       ┌──────▼──────┐      ┌──────▼─────┐
│  Search   │       │   Reader    │      │  Writer    │
│  Agent    │       │   Agent     │      │  Chain     │
└─────┬─────┘       └──────┬──────┘      └──────┬─────┘
      │                    │                    │
      │      ┌─────────────▼─────────────┐      │
      └─────▶│       Tools Layer        │◀─────┘
             │                          │
             │ • web_search (Tavily)    │
             │ • scrape_url (3-tier)    │
             └─────────────┬─────────────┘
                           │
                    ┌──────▼──────┐
                    │   Critic    │
                    │   Chain     │
                    └─────────────┘
```

---

## Agent Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **Search Agent** | Queries the Tavily API for recent, reliable results (titles, URLs, snippets) on the given topic |
| **Reader Agent** | Selects the most relevant URL and extracts deep, readable content using a layered scraping strategy |
| **Writer Chain** | Transforms combined search + scraped content into a structured, professional research report |
| **Critic Chain** | Evaluates the report strictly — assigns a score out of 10, highlights strengths, and suggests improvements |

---

## How It Works

```
User Input → ① Search → ② Read → ③ Write → ④ Critique → Final Report + Feedback
```

1. **Input** — A research topic is provided via the UI or CLI.
2. **Search** — The Search Agent gathers recent, reliable sources from the web.
3. **Read** — The Reader Agent scrapes the most promising source for deeper content.
4. **Write** — The Writer Chain merges search results and scraped content into a structured report (Introduction · Key Findings · Conclusion · Sources).
5. **Critique** — The Critic Chain reviews the report, scoring it and suggesting concrete improvements.
6. **Output** — The final report, score, and feedback are rendered in the UI and available for download.

---

## Technologies

| Technology | Purpose |
|------------|---------|
| [LangChain](https://www.langchain.com/) | Agent creation and chain orchestration |
| [OpenAI GPT-4o-mini](https://platform.openai.com/) | Language model powering agents and chains |
| [Tavily](https://tavily.com/) | Web search and information retrieval |
| [Trafilatura](https://trafilatura.readthedocs.io/) | Primary article/blog content extraction |
| [Readability-lxml](https://pypi.org/project/readability-lxml/) | Secondary content extraction strategy |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing and fallback extraction |
| [Streamlit](https://streamlit.io/) | Interactive web application |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment configuration management |
| [Rich](https://github.com/Textualize/rich) | Rich terminal output formatting |

---

## Prerequisites

- **Python 3.11 or higher**
- An **OpenAI API Key** (model access via `langchain-openai`)
- A **Tavily API Key** (web search)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/LangChain-Multi-Agent-Research-System.git
cd LangChain-Multi-Agent-Research-System
```

### 2. Create a Virtual Environment

**Option A — Conda:**

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
```

**Option B — venv:**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> **Security Note:** The `.env` file is already excluded via `.gitignore` and must **never** be committed to version control.

Obtain your API keys here:

| Service | Where to get it |
|---------|-----------------|
| OpenAI | https://platform.openai.com/api-keys |
| Tavily | https://tavily.com |

---

## Usage

### Option 1 — Streamlit Web UI (Recommended)

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser, enter a topic, and click **Run Research Pipeline**. The interface shows live status for each pipeline step and lets you download the final report as Markdown.

### Option 2 — CLI Script

```bash
python main.py
```

Edit the `topic` variable in `main.py` to research a different subject. The pipeline logs each stage to the terminal with rich formatting.

---

## Project Structure

```
.
├── app.py                      # Streamlit web interface
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── LICENSE                     # Apache License 2.0
├── .gitignore                  # Git ignore rules
├── demo.excalidraw             # Editable architecture diagram
│
└── src/
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── agents.py           # Search/Reader agents, Writer & Critic chains
    ├── tools/
    │   ├── __init__.py
    │   └── tools.py            # web_search, scrape_url (3-tier extraction)
    └── pipelines/
        ├── __init__.py
        └── pipeline.py         # Research pipeline orchestration
```

---

## Output

Each run produces:

- **A structured research report** with:
  - Introduction and background
  - Key findings (minimum 3, well-explained)
  - A well-sourced conclusion
  - Full list of referenced source URLs
- **Critic feedback** including:
  - A quality score out of **10**
  - Listed strengths
  - Concrete areas for improvement
  - A one-line verdict
- **Downloadable Markdown report** via the web UI

---

## Roadmap

- [ ] Streaming token-by-token report generation
- [ ] Support for alternative LLM providers (Anthropic, Gemini, local models)
- [ ] Configurable number of search results and scraping depth
- [ ] Multi-URL reading for broader coverage
- [ ] Export to PDF / DOCX
- [ ] Unit tests and CI pipeline

---

## Contributing

Contributions are welcome! Whether it's a bug fix, new feature, or documentation improvement, please feel free to open a pull request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

Please ensure your code follows the existing style and that no secrets are committed.

---

## License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built on [LangChain](https://www.langchain.com/) — agent & chain orchestration
- Search powered by [Tavily](https://tavily.com/)
- UI built with [Streamlit](https://streamlit.io/)
- LLM inference via [OpenAI](https://openai.com/)
- Inspired by agentic AI research patterns

---

**Happy Researching! 🚀**
