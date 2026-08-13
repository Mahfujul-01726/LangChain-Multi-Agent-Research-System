import streamlit as st
import time
import re
import html
import json
import io
import markdown
from xhtml2pdf import pisa
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearcherAgent — AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (Light Theme) ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

:root {
    --bg: #f6f8fb;
    --bg-soft: #eef2f7;
    --panel: #ffffff;
    --panel-soft: #fbfcfe;
    --border: #e4e9f1;
    --border-accent: #c9e4fb;
    --text: #0f172a;
    --text-dim: #52627a;
    --text-faint: #94a3b8;
    --accent: #0284c7;
    --accent-light: #38bdf8;
    --violet: #7c3aed;
    --green: #16a34a;
    --green-light: #dcfce7;
    --amber: #d97706;
    --red: #dc2626;
    --radius: 16px;
    --shadow: 0 1px 2px rgba(15,23,42,0.04), 0 8px 28px rgba(15,23,42,0.06);
    --shadow-lg: 0 16px 44px rgba(15,23,42,0.10);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(900px 420px at 88% -12%, rgba(56,189,248,0.10), transparent 55%),
        radial-gradient(800px 420px at -8% 0%, rgba(124,58,237,0.07), transparent 55%);
    background-attachment: fixed;
}

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0; max-width: 1320px; }

/* ── Top navigation bar ── */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.85rem 2.4rem;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 100;
}
.nav-brand { display: flex; align-items: center; gap: 0.7rem; }
.nav-logo {
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, var(--accent-light), var(--violet));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem;
    box-shadow: 0 4px 16px rgba(2,132,199,0.25);
}
.nav-title {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.05rem;
    letter-spacing: -0.01em; color: var(--text);
}
.nav-title span {
    background: linear-gradient(135deg, #0284c7, #7c3aed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.nav-right {
    font-family: 'DM Mono', monospace; font-size: 0.66rem; letter-spacing: 0.16em;
    text-transform: uppercase; color: var(--text-dim);
    display: flex; align-items: center; gap: 0.7rem;
}
.pill-live {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: var(--green-light);
    border: 1px solid #bbf7d0;
    color: var(--green);
    padding: 0.25rem 0.7rem; border-radius: 999px;
    font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.12em;
}
.pill-live .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green); box-shadow: 0 0 8px rgba(22,163,74,0.5);
    animation: pulse 1.6s infinite;
}
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }

/* ── Page body wrapper ── */
.page { padding: 2.6rem 3rem 4rem; }

/* ── Hero ── */
.hero { text-align: center; padding: 1.2rem 0 2rem; position: relative; }
.hero-eyebrow {
    font-family: 'DM Mono', monospace; font-size: 0.66rem; font-weight: 500;
    letter-spacing: 0.3em; text-transform: uppercase; color: var(--accent);
    margin-bottom: 0.9rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif; font-size: clamp(2.5rem, 5.2vw, 4.2rem);
    font-weight: 800; line-height: 1.02; letter-spacing: -0.03em;
    color: var(--text); margin: 0 0 0.9rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #0284c7, #7c3aed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1rem; font-weight: 400; color: var(--text-dim);
    max-width: 560px; margin: 0 auto; line-height: 1.65;
}
.hero-tags { display: flex; justify-content: center; gap: 0.55rem; margin-top: 1.2rem; flex-wrap: wrap; }
.hero-tag {
    font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--text-dim);
    border: 1px solid var(--border); border-radius: 999px;
    padding: 0.3rem 0.8rem; background: var(--panel);
}

/* ── Divider ── */
.divider {
    height: 1px; margin: 1.6rem 0 2rem;
    background: linear-gradient(90deg, transparent, #bcd9f0, #ddd0f5, transparent);
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700;
    color: var(--text); margin: 0 0 1.1rem; display: flex; align-items: center; gap: 0.6rem;
}
.section-heading .bar {
    width: 4px; height: 18px; border-radius: 2px;
    background: linear-gradient(180deg, var(--accent-light), var(--violet));
}

/* ── Input card ── */
.input-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow);
}
.input-card .input-label {
    font-family: 'DM Mono', monospace; font-size: 0.64rem; font-weight: 500;
    letter-spacing: 0.2em; text-transform: uppercase; color: var(--accent);
    margin-bottom: 0.7rem;
}
.stTextInput > div > div > input {
    background: var(--panel-soft) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.05rem !important;
    transition: all 0.2s ease !important;
    box-shadow: inset 0 1px 2px rgba(15,23,42,0.04);
}
.stTextInput > div > div > input::placeholder { color: var(--text-faint) !important; }
.stTextInput > div > div > input:focus {
    border-color: var(--accent-light) !important;
    box-shadow: 0 0 0 4px rgba(56,189,248,0.15) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #0284c7 0%, #7c3aed 100%) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.93rem !important; letter-spacing: 0.03em !important;
    border: none !important; border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 10px 28px rgba(2,132,199,0.28) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 14px 36px rgba(124,58,237,0.32) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled { opacity: 0.6 !important; cursor: not-allowed !important; transform: none !important; }

/* ── Example chips ── */
.chips-label {
    font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.18em;
    text-transform: uppercase; color: var(--text-faint); margin: 1.2rem 0 0.6rem;
}
.example-chip {
    display: inline-block;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 0.42rem 0.85rem;
    margin: 0 0.4rem 0.5rem 0;
    font-size: 0.76rem; color: var(--text-dim);
    font-family: 'DM Sans', sans-serif;
    transition: all 0.15s ease;
    cursor: default;
}
.example-chip:hover { border-color: var(--accent-light); color: var(--accent); background: #f0f9ff; }

/* ── Pipeline timeline ── */
.step-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.35rem;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
    transition: all 0.22s ease;
    box-shadow: 0 1px 2px rgba(15,23,42,0.03);
}
.step-card::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: var(--border);
    transition: background 0.3s;
}
.step-card.active { border-color: #7dd3fc; background: #f0f9ff; box-shadow: 0 0 0 3px rgba(56,189,248,0.12); }
.step-card.active::before { background: var(--accent-light); }
.step-card.done { border-color: #bbf7d0; background: #f0fdf4; }
.step-card.done::before { background: var(--green); }
.step-header { display: flex; align-items: center; gap: 0.8rem; }
.step-num {
    font-family: 'DM Mono', monospace; font-size: 0.62rem; font-weight: 500;
    letter-spacing: 0.12em; color: var(--text-faint);
}
.step-title { font-family: 'Syne', sans-serif; font-size: 0.93rem; font-weight: 700; color: var(--text); }
.step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 0.12em; }
.status-waiting { color: var(--text-faint); }
.status-running { color: var(--accent); animation: pulse 1.2s infinite; }
.status-done { color: var(--green); }
.step-desc { font-size: 0.78rem; color: var(--text-dim); margin-top: 0.35rem; }

/* ── Result panels ── */
.result-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.7rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 1px 2px rgba(15,23,42,0.03);
}
.panel-label {
    font-family: 'DM Mono', monospace; font-size: 0.62rem; font-weight: 500;
    letter-spacing: 0.2em; text-transform: uppercase;
    margin-bottom: 1rem; padding-bottom: 0.7rem;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 0.5rem;
}
.panel-label.blue { color: var(--accent); border-bottom-color: #c9e4fb; }
.panel-label.green { color: var(--green); border-bottom-color: #bbf7d0; }
.panel-label.violet { color: var(--violet); border-bottom-color: #ddd0f5; }
.result-content {
    font-size: 0.9rem; line-height: 1.75; color: #334155;
    white-space: pre-wrap; font-family: 'DM Sans', sans-serif;
    max-height: 340px; overflow-y: auto; padding-right: 0.4rem;
}
.result-content::-webkit-scrollbar { width: 6px; }
.result-content::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Report & feedback ── */
.report-panel {
    background: var(--panel);
    border: 1px solid #c9e4fb;
    border-radius: 20px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow-lg);
}
.feedback-panel {
    background: var(--panel);
    border: 1px solid #bbf7d0;
    border-radius: 20px;
    padding: 2rem 2.4rem;
    box-shadow: var(--shadow-lg);
}

/* ── Score metric cards ── */
.metric-row { display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.2rem 0; }
.metric-card {
    flex: 1; min-width: 150px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    text-align: center;
    box-shadow: 0 1px 2px rgba(15,23,42,0.03);
}
.metric-card .metric-value {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.9rem; line-height: 1.1;
}
.metric-card .metric-label {
    font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.18em;
    text-transform: uppercase; color: var(--text-dim); margin-top: 0.4rem;
}

/* ── Loader card ── */
.loader-card {
    background: var(--panel);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius);
    padding: 1.4rem 1.7rem;
    margin: 1.5rem 0;
    box-shadow: var(--shadow);
}
.loader-title {
    font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem;
    color: var(--text); margin-bottom: 0.3rem;
}
.loader-sub { font-size: 0.85rem; color: var(--text-dim); }

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 11px !important;
    color: var(--accent) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    padding: 0.65rem 1.4rem !important;
    box-shadow: 0 1px 2px rgba(15,23,42,0.05) !important;
    transition: all 0.18s ease !important;
}
.stDownloadButton > button:hover {
    background: #f0f9ff !important;
    border-color: var(--accent-light) !important;
}

/* ── Expander ── */
details {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.3rem 0.9rem;
    margin-bottom: 0.9rem;
}
details summary {
    font-family: 'DM Mono', monospace !important; font-size: 0.7rem !important;
    letter-spacing: 0.12em !important; color: var(--text-dim) !important;
    cursor: pointer; padding: 0.35rem 0;
}
details summary:hover { color: var(--accent) !important; }

/* ── Footer ── */
.footer {
    text-align: center; padding: 2.4rem 0 1rem;
    font-family: 'DM Mono', monospace; font-size: 0.62rem;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--text-faint);
}
.footer .sep { color: var(--border); margin: 0 0.5rem; }

/* ── Spinner ── */
.stSpinner > div { color: var(--accent) !important; font-family: 'DM Sans', sans-serif !important; }

/* ── Markdown inside panels ── */
.report-panel h1, .report-panel h2, .report-panel h3,
.feedback-panel h1, .feedback-panel h2, .feedback-panel h3 {
    font-family: 'Syne', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def extract_score(text: str):
    m = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", text or "")
    return float(m.group(1)) if m else None


def safe(text: str) -> str:
    return html.escape(text or "")


def md_to_pdf_bytes(md_text: str) -> bytes:
    html_body = markdown.markdown(md_text or "", extensions=["extra", "tables", "sane_lists"])
    styled = f"""
    <html>
    <head>
    <style>
        @page {{ size: A4; margin: 2cm; }}
        body {{ font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; color: #1e293b; line-height: 1.55; }}
        h1 {{ font-size: 18pt; color: #0f172a; border-bottom: 2px solid #0284c7; padding-bottom: 6px; }}
        h2 {{ font-size: 14pt; color: #0f172a; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; }}
        h3 {{ font-size: 12pt; color: #0f172a; }}
        a {{ color: #0284c7; text-decoration: none; }}
        table {{ border-collapse: collapse; width: 100%; margin: 8px 0; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
        th {{ background: #f1f5f9; }}
        blockquote {{ border-left: 3px solid #0284c7; margin-left: 0; padding-left: 12px; color: #475569; }}
        code {{ font-family: monospace; background: #f1f5f9; padding: 1px 4px; }}
        pre {{ background: #f1f5f9; padding: 10px; border-radius: 6px; }}
        li {{ margin-bottom: 4px; }}
    </style>
    </head>
    <body>{html_body}</body>
    </html>
    """
    pdf = io.BytesIO()
    pisa.CreatePDF(src=styled, dest=pdf)
    return pdf.getvalue()


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-brand">
        <div class="nav-logo">🔬</div>
        <div class="nav-title">Researcher<span>Agent</span></div>
    </div>
    <div class="nav-right">
        <span class="pill-live"><span class="dot"></span>Multi-Agent Pipeline Active</span>
        <span>LangChain · Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="page">', unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI Research System</div>
    <h1>Research. Draft. <span>Refine.</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing, and
        critiquing — to deliver a polished, well-sourced research report on any topic.
    </p>
    <div class="hero-tags">
        <span class="hero-tag">Search Agent</span>
        <span class="hero-tag">Reader Agent</span>
        <span class="hero-tag">Writer Chain</span>
        <span class="hero-tag">Critic Chain</span>
    </div>
</div>

<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:

    st.markdown('<div class="section-heading"><span class="bar"></span>Research Request</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    st.markdown('<div class="input-label">Topic</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Roadmap for AGI development in next 5 years",
        key="topic_input",
        label_visibility="collapsed",
    )

    run_btn = st.button("⚡ Run Research Pipeline", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chips-label">Try a topic →</div>', unsafe_allow_html=True)

    examples = [
        "Future of LLM in Tech Industry",
        "Latest AI Agents in 2026",
        "Roadmap for AGI in the next 5 years",
        "Impact of AI on the job market",
    ]

    for ex in examples:
        st.markdown(f'<span class="example-chip">{safe(ex)}</span>', unsafe_allow_html=True)

with col_pipeline:

    st.markdown('<div class="section-heading"><span class="bar"></span>Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent", s("search"), "Gathers recent, reliable web information")
    step_card("02", "Reader Agent", s("reader"), "Scrapes & extracts deep content from sources")
    step_card("03", "Writer Chain", s("writer"), "Synthesizes findings into a structured report")
    step_card("04", "Critic Chain", s("critic"), "Reviews the report and scores its quality")


# ── Run pipeline (step-by-step with live progress) ────────────────────────────
if run_btn:

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


if st.session_state.running and not st.session_state.done:

    topic_val = st.session_state.topic_input
    results = dict(st.session_state.results)
    done_steps = len(results)

    # ── Loader UI ──
    st.markdown("""
    <div class="loader-card">
        <div class="loader-title">⚙️ Running Research Pipeline</div>
        <div class="loader-sub">Executing the 4-agent workflow — status updates live below.</div>
    </div>
    """, unsafe_allow_html=True)

    progress = st.progress(max(0.03, done_steps * 0.25), text="Starting pipeline…")
    status_ph = st.empty()

    # ── Step 1: Search Agent ──
    if done_steps == 0:
        progress.progress(0.1, text="🔍 Searching the web…")
        status_ph.info("🔍 **Search Agent** is gathering recent, reliable results…")
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [
                ("user",
                 f"Find recent, reliable and detailed information about: {topic_val}")
            ]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = results
        st.rerun()

    # ── Step 2: Reader Agent ──
    elif done_steps == 1:
        progress.progress(0.35, text="📄 Extracting deep content…")
        status_ph.info("📄 **Reader Agent** is scraping the most relevant source…")
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = results
        st.rerun()

    # ── Step 3: Writer Chain ──
    elif done_steps == 2:
        progress.progress(0.6, text="✍️ Drafting the report…")
        status_ph.info("✍️ **Writer Chain** is synthesizing findings into a structured report…")
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = results
        st.rerun()

    # ── Step 4: Critic Chain ──
    elif done_steps == 3:
        progress.progress(0.85, text="🧐 Reviewing the report…")
        status_ph.info("🧐 **Critic Chain** is reviewing and scoring the report…")
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = results
        st.session_state.running = False
        st.session_state.done = True
        st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-heading"><span class="bar"></span>Results</div>', unsafe_allow_html=True)

    # Score metric (if critic output contains a score)
    score = extract_score(r.get("critic", ""))
    if score is not None:
        pct = round(score * 10)
        color = "#16a34a" if score >= 7 else ("#d97706" if score >= 5 else "#dc2626")
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-value" style="color:{color}">{score:.1f}<span style="font-size:1rem;color:var(--text-faint)">/10</span></div>
                <div class="metric-label">Quality Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color:var(--accent)">4</div>
                <div class="metric-label">Agents Run</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color:var(--violet)">{len(r['writer'].split())}</div>
                <div class="metric-label">Report Words</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Raw outputs
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f"""
            <div class="result-panel">
                <div class="panel-label blue">🔍 Search Agent Output</div>
                <div class="result-content">{safe(r["search"])}</div>
            </div>
            """, unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f"""
            <div class="result-panel">
                <div class="panel-label violet">📄 Reader Agent Output</div>
                <div class="result-content">{safe(r["reader"])}</div>
            </div>
            """, unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown(f"""
        <div class="report-panel">
            <div class="panel-label blue">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        dl1, dl2 = st.columns(2)
        with dl1:
            try:
                pdf_bytes = md_to_pdf_bytes(r["writer"])
                st.download_button(
                    label="⬇ Download Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"research_report_{int(time.time())}.pdf",
                    mime="application/pdf",
                )
            except Exception:
                st.download_button(
                    label="⬇ Download Report (.md)",
                    data=r["writer"],
                    file_name=f"research_report_{int(time.time())}.md",
                    mime="text/markdown",
                )
        with dl2:
            bundle = json.dumps({
                "topic": st.session_state.topic_input,
                "search_results": r.get("search", ""),
                "scraped_content": r.get("reader", ""),
                "report": r.get("writer", ""),
                "critic_feedback": r.get("critic", ""),
            }, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇ Download All Data (.json)",
                data=bundle,
                file_name=f"research_bundle_{int(time.time())}.json",
                mime="application/json",
            )

    # Critic feedback
    if "critic" in r:
        st.markdown(f"""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ResearcherAgent <span class="sep">·</span> Powered by LangChain Multi-Agent Pipeline <span class="sep">·</span> Built with Streamlit
</div>
""", unsafe_allow_html=True)