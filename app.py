import streamlit as st
import time
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ─── Streamlit Cloud secrets fallback ───────────────────────────────────────────
def get_secret(key: str) -> str:
    """Read from env first, then Streamlit secrets (for Streamlit Cloud deployment)."""
    val = os.getenv(key, "")
    if not val:
        try:
            val = st.secrets.get(key, "")
        except Exception:
            val = ""
    return val

# Inject secrets into env so all downstream modules (LangChain, Mistral, etc.) can read them
for _k in ["MISTRAL_API_KEY", "SARVAM_API_KEY", "GROQ_API_KEY"]:
    if not os.getenv(_k):
        _v = get_secret(_k)
        if _v:
            os.environ[_k] = _v

# ─── Dependency pre-check (runs inside Streamlit's Python) ──────────────────────
_REQUIRED = {
    "numpy":                "numpy",
    "groq":                 "groq",
    "chromadb":             "chromadb",
    "langchain":            "langchain",
    "langchain_mistralai":  "langchain-mistralai",
    "langchain_community":  "langchain-community",
    "langchain_huggingface":"langchain-huggingface",
    "sentence_transformers":"sentence-transformers",
    "pydub":                "pydub",
    "deep_translator":      "deep-translator",
    "mistralai":            "mistralai",
}

_missing = []
for _mod, _pkg in _REQUIRED.items():
    try:
        __import__(_mod)
    except ImportError:
        _missing.append(_pkg)

if _missing:
    st.set_page_config(page_title="Nuance — Setup Required", page_icon="🚨", layout="centered")
    st.error("### Missing packages in Streamlit's Python environment")
    st.code(f"{sys.executable} -m pip install {' '.join(_missing)}", language="bash")
    st.warning(
        f"**Streamlit is using Python at:** `{sys.executable}`\n\n"
        "This is likely a different Python/venv than your terminal. "
        "Run the command above, then restart Streamlit."
    )
    st.info(
        "**Quick fix — always launch Streamlit like this:**\n"
        "```\n"
        "# Activate your venv first:\n"
        ".venv\\Scripts\\activate   # Windows\n"
        "source .venv/bin/activate  # Mac/Linux\n"
        "\n"
        "# Then run:\n"
        "streamlit run app.py\n"
        "```"
    )
    st.stop()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nuance AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

*,*::before,*::after{box-sizing:border-box}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#070B12!important;color:#E2E8F0!important}
[data-testid="stSidebar"]{background:#0A0F1A!important;border-right:1px solid #151F35!important}
h1,h2,h3,h4{font-family:'Syne',sans-serif!important}
p,span,div,label,li{font-family:'DM Sans',sans-serif!important}
code,pre{font-family:'DM Mono',monospace!important}

#MainMenu,footer,header,[data-testid="stDecoration"],footer a,footer p{visibility:hidden;display:none!important}
[data-testid="collapsedControl"]{display:flex!important;visibility:visible!important}
[data-testid="stSidebarCollapseButton"]{display:flex!important;visibility:visible!important}
[data-testid="stSidebarCollapseButton"] button,[data-testid="collapsedControl"] button{font-size:0!important;width:2rem!important;height:2rem!important;border-radius:50%!important;background:#0C1422!important;border:1px solid #1E2D4A!important;cursor:pointer!important;display:flex!important;align-items:center!important;justify-content:center!important}
[data-testid="stSidebarCollapseButton"] button::after{content:'‹';font-size:1.3rem;color:#60A5FA;line-height:1}
[data-testid="collapsedControl"] button::after{content:'›';font-size:1.3rem;color:#60A5FA;line-height:1}
[data-testid="stSidebarCollapseButton"] button svg,[data-testid="collapsedControl"] button svg{display:none!important}
[data-testid="stSidebarCollapseButton"] button span,[data-testid="collapsedControl"] button span{display:none!important}
/* Fix broken Material Icons on file uploader button */
[data-testid="stFileUploader"] button{font-size:0!important;position:relative!important}
[data-testid="stFileUploader"] button::after{content:'⬆ Upload File';font-size:.85rem!important;font-family:'Syne',sans-serif!important;font-weight:700!important;color:#fff!important}
[data-testid="stFileUploader"] button span{display:none!important}
[data-testid="stFileUploader"] button svg{display:none!important}
.block-container{padding:1.8rem 2.2rem 4rem!important;max-width:1380px!important}

/* ── Sidebar ── */
.sb-logo{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;background:linear-gradient(135deg,#60A5FA,#A78BFA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:2px}
.sb-tag{font-family:'DM Mono',monospace;font-size:.62rem;color:#374151;text-transform:uppercase;letter-spacing:.1em;margin-bottom:1.4rem}
.sb-sec{font-family:'DM Mono',monospace;font-size:.62rem;color:#374151;text-transform:uppercase;letter-spacing:.1em;margin:1.2rem 0 .5rem;padding-top:.9rem;border-top:1px solid #151F35}
.sb-pill{display:flex;align-items:center;gap:7px;padding:.55rem .9rem;border-radius:8px;font-family:'DM Sans',sans-serif;font-size:.8rem;margin-bottom:.4rem}
.sb-pill.ok{background:rgba(16,185,129,.07);border:1px solid rgba(16,185,129,.18);color:#6EE7B7}
.sb-pill.err{background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.18);color:#FCA5A5}
.sb-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.sb-dot.ok{background:#10B981;animation:pdot 2s ease-in-out infinite}
.sb-dot.err{background:#EF4444}
@keyframes pdot{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.6)}}

/* ── Hero ── */
.hero{padding:2.8rem 0 1.8rem;position:relative;overflow:hidden}
.hero-ghost{position:absolute;top:-20px;left:-8px;font-family:'Syne',sans-serif;font-size:8rem;font-weight:800;color:rgba(96,165,250,.03);white-space:nowrap;pointer-events:none;user-select:none;letter-spacing:-4px}
.hero-pill{display:inline-flex;align-items:center;gap:6px;background:rgba(96,165,250,.08);border:1px solid rgba(96,165,250,.22);border-radius:100px;padding:4px 13px;font-family:'DM Mono',monospace;font-size:.68rem;color:#60A5FA;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.9rem}
.hero-pill::before{content:'';width:6px;height:6px;border-radius:50%;background:#60A5FA;animation:pdot 2s ease-in-out infinite}
.hero-h1{font-family:'Syne',sans-serif!important;font-size:3.4rem!important;font-weight:800!important;line-height:1.06!important;letter-spacing:-2px!important;margin:0 0 .5rem!important;background:linear-gradient(135deg,#E2E8F0 0%,#60A5FA 55%,#A78BFA 100%);-webkit-background-clip:text!important;-webkit-text-fill-color:transparent!important;background-clip:text!important}
.hero-sub{font-family:'DM Sans',sans-serif;font-size:1rem;color:#94A3B8;letter-spacing:.02em;font-weight:300;max-width:500px;line-height:1.7}
.divider{height:1px;background:linear-gradient(90deg,#60A5FA1A,#A78BFA1A,transparent);margin:1.8rem 0 2rem}

/* ── Tabs ── */
[data-testid="stTabs"] [data-testid="stTab"]{font-family:'Syne',sans-serif!important;font-weight:600!important;font-size:.88rem!important;color:#4B5563!important;border-bottom:2px solid transparent!important;padding:.55rem 1.3rem!important;transition:all .2s!important;border-radius:0!important}
[data-testid="stTabs"] [aria-selected="true"]{color:#60A5FA!important;border-bottom:2px solid #60A5FA!important;background:transparent!important}
[data-testid="stTabs"]{border-bottom:1px solid #151F35!important}

/* ── Cards ── */
.card{background:#0C1422;border:1px solid #151F35;border-radius:14px;padding:1.5rem;margin-bottom:1rem}
.ctop{background:#0C1422;border:1px solid #1E2D4A;border-radius:14px;padding:1.5rem;margin-bottom:1rem;position:relative;overflow:hidden}
.ctop::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#60A5FA,#A78BFA);speak:none;font-size:0;line-height:0}
.clbl{font-family:'DM Mono',monospace;font-size:.63rem;color:#60A5FA;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem}
.ctitle{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#E2E8F0;margin-bottom:.3rem}
.cbody{font-family:'DM Sans',sans-serif;font-size:.88rem;color:#6B7280;line-height:1.7}

/* ── Steps ── */
.steps{display:flex;align-items:center;margin:1.4rem 0 1.8rem}
.snum{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'DM Mono',monospace;font-size:.7rem;flex-shrink:0;transition:all .3s}
.snum.idle{background:#0A0F1A;border:1px solid #151F35;color:#374151}
.snum.active{background:#3B82F6;border:1px solid #3B82F6;color:#fff}
.snum.done{background:#10B981;border:1px solid #10B981;color:#fff}
.slbl{font-family:'DM Sans',sans-serif;font-size:.76rem;color:#374151;margin-left:6px;white-space:nowrap}
.slbl.active{color:#E2E8F0}
.sconn{flex:1;height:1px;background:#151F35;margin:0 8px}

/* ── Inputs ── */
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{background:#0A0F1A!important;border:1px solid #151F35!important;color:#E2E8F0!important;border-radius:10px!important;font-family:'DM Mono',monospace!important;font-size:.85rem!important;transition:border-color .2s!important}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus{border-color:#60A5FA!important;box-shadow:0 0 0 3px rgba(96,165,250,.1)!important}
[data-testid="stTextInput"] label,[data-testid="stTextArea"] label,[data-testid="stFileUploader"] label,[data-testid="stSelectbox"] label{font-family:'DM Sans',sans-serif!important;color:#9CA3AF!important;font-size:.82rem!important;font-weight:500!important}
[data-testid="stSelectbox"]>div>div{background:#0A0F1A!important;border:1px solid #151F35!important;color:#E2E8F0!important;border-radius:10px!important}
[data-testid="stFileUploader"]{background:#0A0F1A!important;border:1px dashed #1E2D4A!important;border-radius:12px!important}
[data-testid="stRadio"] label{color:#9CA3AF!important;font-family:'DM Sans',sans-serif!important}

/* ── Buttons ── */
.stButton>button{font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:.87rem!important;letter-spacing:.02em!important;padding:.65rem 1.8rem!important;border-radius:10px!important;border:none!important;background:linear-gradient(135deg,#3B82F6,#6366F1)!important;color:#fff!important;width:100%!important;transition:all .2s!important}
.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 8px 22px rgba(99,102,241,.3)!important}
.stButton>button:disabled{opacity:.4!important;transform:none!important}

/* ── Alerts ── */
.ainfo{background:rgba(96,165,250,.07);border:1px solid rgba(96,165,250,.18);border-left:3px solid #60A5FA;border-radius:0 9px 9px 0;padding:.8rem 1.1rem;font-family:'DM Sans',sans-serif;font-size:.85rem;color:#93C5FD;margin:.7rem 0}
.awarn{background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.18);border-left:3px solid #FBBF24;border-radius:0 9px 9px 0;padding:.8rem 1.1rem;font-family:'DM Sans',sans-serif;font-size:.85rem;color:#FDE68A;margin:.7rem 0}
.aok{background:rgba(16,185,129,.07);border:1px solid rgba(16,185,129,.18);border-left:3px solid #10B981;border-radius:0 9px 9px 0;padding:.8rem 1.1rem;font-family:'DM Sans',sans-serif;font-size:.85rem;color:#6EE7B7;margin:.7rem 0}
.aerr{background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.18);border-left:3px solid #EF4444;border-radius:0 9px 9px 0;padding:.8rem 1.1rem;font-family:'DM Sans',sans-serif;font-size:.85rem;color:#FCA5A5;margin:.7rem 0}

/* ── Stats ── */
.stats{display:flex;gap:.7rem;flex-wrap:wrap;margin:1rem 0}
.stat{background:rgba(96,165,250,.06);border:1px solid rgba(96,165,250,.14);border-radius:10px;padding:.65rem 1rem;flex:1;min-width:90px;text-align:center}
.stat .v{font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:700;color:#60A5FA}
.stat .l{font-family:'DM Mono',monospace;font-size:.6rem;color:#374151;text-transform:uppercase;letter-spacing:.08em}

/* ── Expanders ── */
[data-testid="stExpander"]{background:#0C1422!important;border:1px solid #151F35!important;border-radius:12px!important;margin-bottom:.7rem!important;margin-top:.8rem!important}
[data-testid="stExpander"] summary{font-family:'Syne',sans-serif!important;font-weight:600!important;color:#E2E8F0!important;padding:.9rem 1.1rem!important;font-size:.95rem!important;letter-spacing:.01em!important;overflow:visible!important}
/* ── Custom collapsible (replaces st.expander for transcript) ── */
details.tx-wrap{background:#0C1422;border:1px solid #151F35;border-radius:12px;margin:.8rem 0 .7rem;overflow:hidden}
details.tx-wrap summary{font-family:'Syne',sans-serif;font-weight:600;color:#E2E8F0;padding:.9rem 1.1rem;font-size:.95rem;letter-spacing:.01em;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem;user-select:none}
details.tx-wrap summary::-webkit-details-marker{display:none}
details.tx-wrap summary::before{content:'▶';font-size:.6rem;color:#60A5FA;transition:transform .2s;flex-shrink:0}
details.tx-wrap[open] summary::before{transform:rotate(90deg)}
details.tx-wrap .tx-inner{padding:0 1.1rem 1.1rem}
/* ── Transcript ── */
.tx-box{background:#070B12;border:1px solid #151F35;border-radius:11px;padding:1.2rem 1.4rem;font-family:'DM Mono',monospace;font-size:.78rem;color:#9CA3AF;line-height:1.8;max-height:260px;overflow-y:auto;white-space:pre-wrap;word-break:break-word}
.tx-box::-webkit-scrollbar{width:3px}
.tx-box::-webkit-scrollbar-track{background:#0A0F1A}
.tx-box::-webkit-scrollbar-thumb{background:#1E2D4A;border-radius:3px}

/* ── Chat ── */
.chat-wrap{display:flex;flex-direction:column;gap:.9rem;max-height:400px;overflow-y:auto;padding:.3rem 0;margin-bottom:.9rem}
.chat-wrap::-webkit-scrollbar{width:3px}
.chat-wrap::-webkit-scrollbar-track{background:transparent}
.chat-wrap::-webkit-scrollbar-thumb{background:#1E2D4A;border-radius:3px}
.mu{align-self:flex-end;background:linear-gradient(135deg,#1D3461,#1B3A5C);border:1px solid #2D4A7A;border-radius:13px 13px 3px 13px;padding:.8rem 1.1rem;max-width:74%;font-family:'DM Sans',sans-serif;font-size:.87rem;color:#E2E8F0;line-height:1.6}
.ma{align-self:flex-start;background:#0C1422;border:1px solid #151F35;border-radius:13px 13px 13px 3px;padding:.8rem 1.1rem;max-width:76%;font-family:'DM Sans',sans-serif;font-size:.87rem;color:#CBD5E1;line-height:1.7}
.mu-lbl{font-family:'DM Mono',monospace;font-size:.6rem;color:#60A5FA;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.25rem;text-align:right}
.ma-lbl{font-family:'DM Mono',monospace;font-size:.6rem;color:#A78BFA;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.25rem}
.chat-empty{height:280px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#0A0F1A;border:1px dashed #151F35;border-radius:13px;color:#1F2937;font-family:'DM Mono',monospace;font-size:.78rem;text-align:center;padding:2rem}

/* ── Section header ── */
.sh{display:flex;align-items:baseline;gap:10px;margin:1.8rem 0 .9rem}
.sh-t{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#E2E8F0}
.sh-b{font-family:'DM Mono',monospace;font-size:.62rem;color:#374151;text-transform:uppercase;letter-spacing:.1em;background:#0C1422;border:1px solid #151F35;border-radius:100px;padding:2px 9px}

/* ── Quick prompt chips ── */
.stButton > button{white-space:normal!important;word-wrap:break-word!important;height:auto!important;min-height:2.8rem!important;line-height:1.4!important}
.stButton[data-testid*="quick"] > button{background:#0C1422!important;border:1px solid #1E2D4A!important;color:#9CA3AF!important;font-size:.78rem!important;font-weight:500!important;font-family:'DM Sans',sans-serif!important;padding:.45rem .9rem!important;text-align:left!important;border-radius:8px!important;white-space:normal!important;word-wrap:break-word!important;height:auto!important;min-height:2.8rem!important;line-height:1.4!important}
.stButton[data-testid*="quick"] > button:hover{border-color:#60A5FA!important;color:#E2E8F0!important;transform:none!important;box-shadow:none!important}

/* ── Progress ── */
[data-testid="stProgress"]>div>div{background:linear-gradient(90deg,#3B82F6,#A78BFA)!important;border-radius:100px!important}
[data-testid="stProgress"]>div{background:#151F35!important;border-radius:100px!important}

/* ── Footer ── */
.ft{margin-top:3.5rem;padding-top:1.2rem;border-top:1px solid #151F35;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem}
.ft-logo{font-family:'Syne',sans-serif;font-weight:800;font-size:.92rem;background:linear-gradient(135deg,#60A5FA,#A78BFA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.ft-meta{font-family:'DM Mono',monospace;font-size:.6rem;color:#374151;letter-spacing:.04em}
.ft-link{font-family:'DM Mono',monospace;font-size:.6rem;color:#60A5FA!important;letter-spacing:.04em;text-decoration:none!important;border-bottom:none!important;transition:color .2s}
.ft-link2{font-family:'DM Mono',monospace;font-size:.6rem;color:#A78BFA!important;letter-spacing:.04em;text-decoration:none!important;border-bottom:none!important;transition:color .2s}
.ft-link:hover{text-decoration:none!important;color:#FBBF24!important;text-shadow:0 0 8px rgba(251,191,36,.4)}
.ft-link2:hover{text-decoration:none!important;color:#FBBF24!important;text-shadow:0 0 8px rgba(251,191,36,.4)}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────────
_defaults = {
    "t1_result": None,
    "t1_rag_chain": None,
    "t1_chat": [],
    "t1_processing": False,
    "t2_live_notes": "",
    "t2_rag_chain": None,
    "t2_chat": [],
    "t2_post_result": None,
    "t2_processing": False,
    "t2_post_processing": False,
    "t2_transcript": "",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Helper: run pipeline steps ─────────────────────────────────────────────────
def run_full_pipeline(source: str, language: str, progress_cb, status_cb):
    from utils.audio_processor import process_input
    from core.transcriber import transcribe_all
    from core.rag_engine import build_rag_chain

    status_cb("🔊 Extracting & chunking audio…")
    progress_cb(12)
    chunks = process_input(source)

    engine = "Sarvam AI" if language == "hinglish" else "Whisper"
    status_cb(f"📝 Transcribing {len(chunks)} chunk(s) with {engine}…")
    progress_cb(45)
    transcript = transcribe_all(chunks, language)

    status_cb("🧠 Building RAG knowledge base…")
    progress_cb(82)
    rag_chain = build_rag_chain(transcript)

    progress_cb(100)
    return {
        "title": "Transcript Ready",
        "transcript": transcript,
        "rag_chain": rag_chain,
    }


def render_chat(history_key: str):
    history = st.session_state[history_key]
    if not history:
        st.markdown("""
        <div class="chat-empty">
            <div style="font-size:2rem;opacity:.2;margin-bottom:.8rem">💬</div>
            <div>No messages yet</div>
            <div style="font-size:.68rem;color:#111827;margin-top:.3rem">Ask anything about the content</div>
        </div>""", unsafe_allow_html=True)
        return
    html = '<div class="chat-wrap">'
    for m in history:
        if m["role"] == "user":
            html += f'<div><div class="mu-lbl">You</div><div class="mu">{m["content"]}</div></div>'
        else:
            html += f'<div><div class="ma-lbl">Nuance AI</div><div class="ma">{m["content"]}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_results(r: dict, chat_key: str, rag_key: str, tab_prefix: str):
    words = len(r["transcript"].split())
    sents = r["transcript"].count(".")

    st.markdown(
        f'<div class="stats">'
        f'<div class="stat"><div class="v">{words:,}</div><div class="l">Words</div></div>'
        f'<div class="stat"><div class="v">{sents}</div><div class="l">Sentences</div></div>'
        f'<div class="stat"><div class="v">~{round(words/130)}m</div><div class="l">Duration</div></div>'
        f'</div>', unsafe_allow_html=True
    )

    st.markdown(
        f'<details class="tx-wrap"><summary>📄 View Transcript</summary>'
        f'<div class="tx-inner"><div class="tx-box">{r["transcript"]}</div></div></details>',
        unsafe_allow_html=True
    )

    st.markdown('<div style="height:.6rem"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sh">'
        '<span class="sh-t">💬 Ask Questions About This Content</span>'
        '<span class="sh-b">Mistral RAG</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="ainfo">💡 Chat is scoped to the current video. '
        'Transcribing a new video will automatically clear this chat.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="clbl" style="margin-bottom:.5rem">Try asking</div>', unsafe_allow_html=True)
    sugg = [
        "What is this video about?",
        "What are the main points discussed?",
        "Summarize the key takeaways",
        "What conclusions were reached?",
    ]
    scols = st.columns(4, gap="small")
    for i, sq in enumerate(sugg):
        with scols[i]:
            if st.button(sq, key=f"{tab_prefix}_sugg_{i}", use_container_width=True):
                if st.session_state[rag_key]:
                    with st.spinner("Thinking…"):
                        from core.rag_engine import ask_question
                        ans = ask_question(st.session_state[rag_key], sq)
                    st.session_state[chat_key].append({"role": "user", "content": sq})
                    st.session_state[chat_key].append({"role": "assistant", "content": ans})
                    st.rerun()

    st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
    render_chat(chat_key)

    q_col, b_col = st.columns([5, 1], gap="small")
    with q_col:
        user_q = st.text_input("Your question",
                               placeholder="Ask anything…",
                               label_visibility="collapsed", key=f"{tab_prefix}_q_input")
    with b_col:
        ask = st.button("Ask →", key=f"{tab_prefix}_ask_btn")

    if ask and user_q.strip():
        if st.session_state[rag_key]:
            with st.spinner("Thinking…"):
                from core.rag_engine import ask_question
                ans = ask_question(st.session_state[rag_key], user_q.strip())
            st.session_state[chat_key].append({"role": "user", "content": user_q.strip()})
            st.session_state[chat_key].append({"role": "assistant", "content": ans})
            st.rerun()

    if st.session_state[chat_key]:
        if st.button("🗑 Clear chat", key=f"{tab_prefix}_clear_chat"):
            st.session_state[chat_key] = []
            st.rerun()


def save_upload(uploaded_file) -> str:
    os.makedirs("downloads", exist_ok=True)
    path = os.path.join("downloads", uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.read())
    return path


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">Nuance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tag">AI Video & Meeting Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-pill">Live</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sec">API Status</div>', unsafe_allow_html=True)
    for label, key in [
        ("Mistral AI", "MISTRAL_API_KEY"),
        ("Groq AI (English STT)", "GROQ_API_KEY"),
        ("Sarvam AI (Hinglish)", "SARVAM_API_KEY"),
    ]:
        ok = bool(get_secret(key))
        cls = "ok" if ok else "err"
        st.markdown(
            f'<div class="sb-pill {cls}"><div class="sb-dot {cls}"></div>{label}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="sb-sec">Config</div>', unsafe_allow_html=True)
    st.selectbox("Whisper Model", ["small"],
                index=0, key="whisper_model",
                disabled=True,
                help="Default: whisper small model")
    st.selectbox("RAG context chunks (k)", [2, 3, 4, 6], index=2, key="rag_k")

    if st.session_state.t1_result:
        st.markdown('<div class="sb-sec">Export Transcript</div>', unsafe_allow_html=True)
        r = st.session_state.t1_result
        words_sb = len(r.get("transcript", "").split())
        st.markdown(
            f'<div class="sb-pill ok"><div class="sb-dot ok"></div>{words_sb:,} words ready</div>',
            unsafe_allow_html=True
        )
        txt = f"NUANCE AI — TRANSCRIPT\n{'='*52}\n\n{r.get('transcript','')}"
        st.download_button("⬇ Download Transcript", data=txt,
                           file_name="nuance_transcript.txt", mime="text/plain",
                           use_container_width=True)

    if st.session_state.t2_post_result:
        st.markdown('<div class="sb-sec">Export Meeting Notes</div>', unsafe_allow_html=True)
        r2 = st.session_state.t2_post_result
        txt2 = (
            f"NUANCE — MEETING INTELLIGENCE NOTES\n{'='*52}\n\n"
            f"TITLE: {r2['title']}\n\nSUMMARY:\n{r2['summary']}\n\n"
            f"ACTION ITEMS:\n{r2['action_items']}\n\nKEY DECISIONS:\n{r2['key_decisions']}\n\n"
            f"OPEN QUESTIONS:\n{r2['open_questions']}\n\nTRANSCRIPT:\n{r2['transcript']}"
        )
        st.download_button("⬇ Download Meeting Notes", data=txt2,
                           file_name="nuance_meeting_notes.txt", mime="text/plain",
                           use_container_width=True)

    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ft-meta" style="text-align:center">Whisper · Mistral AI · LangChain · ChromaDB · RAG</div>',
        unsafe_allow_html=True
    )


# ─── Hero ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-ghost">NUANCE</div>
    <div class="hero-h1">Every word.<br>Every detail. Captured.</div>
    <div class="hero-sub">Built by Bishwajit Pattanaik</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["💬  Transcribe & Ask Questions", "📋  Meeting Notes Generator"])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="ctop">
        <div class="clbl">Transcribe & Ask Questions</div>
        <div class="ctitle">Upload any video/audio → chat with every nuance of it</div>
        <div class="cbody">
            Paste a YouTube URL or upload any audio/video file. Nuance extracts the audio,
            transcribes it with Whisper (or Sarvam AI for Hinglish), and builds a RAG knowledge base —
            so you can ask <b>any question</b> about the content and get precise answers powered by Mistral.
        </div>
    </div>
    """, unsafe_allow_html=True)

    s = 1
    if st.session_state.t1_result: s = 3
    elif st.session_state.t1_processing: s = 2
    def sc(n):
        if n < s: return "done"
        if n == s: return "active"
        return "idle"
    steps_html = '<div class="steps">'
    for i, (num, lbl) in enumerate([("1","Upload / URL"),("2","Transcribe"),("3","Ask Questions")]):
        c = sc(i+1)
        icon = "✓" if c == "done" else num
        steps_html += f'<div style="display:flex;align-items:center"><div class="snum {c}">{icon}</div><span class="slbl {c if c!="idle" else ""}">{lbl}</span></div>'
        if i < 2: steps_html += '<div class="sconn"></div>'
    steps_html += '</div>'
    st.markdown(steps_html, unsafe_allow_html=True)

    col_src, col_lang = st.columns([3, 1], gap="large")
    with col_src:
        src_type = st.radio("Source", ["YouTube / Web URL", "Local File"],
                            horizontal=True, key="t1_src_type")
        if src_type == "YouTube / Web URL":
            yt = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=…",
                               label_visibility="collapsed", key="t1_yt_url")
            source_val = yt.strip() if yt.strip() else None
            st.markdown('<div class="ainfo">ℹ️ Any YouTube, Loom, or direct audio URL</div>', unsafe_allow_html=True)
        else:
            up = st.file_uploader("Upload audio/video file", type=["mp4","mp3","wav","m4a","webm","ogg","mkv","mov"],
                                  label_visibility="collapsed", key="t1_upload")
            source_val = None
            if up:
                source_val = save_upload(up)
                st.markdown(f'<div class="aok">Loaded: <b>{up.name}</b> — {round(up.size/1e6,1)} MB</div>', unsafe_allow_html=True)

    with col_lang:
        lang = st.selectbox("Language", ["english", "hinglish"],
                            key="t1_lang",
                            help="Hinglish uses Sarvam AI STT-Translate API")
        if lang == "hinglish":
            st.markdown('<div class="awarn">Powered by Sarvam AI</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
    run_col, _ = st.columns([1, 2])
    with run_col:
        go = st.button("⚡ Transcribe & Build Q&A", key="t1_go",
                       disabled=st.session_state.t1_processing)

    if go:
        if not source_val:
            st.markdown('<div class="awarn">⚠️ Provide a URL or upload a file first.</div>', unsafe_allow_html=True)
        else:
            st.session_state.t1_processing = True
            st.session_state.t1_result = None
            st.session_state.t1_chat = []
            st.session_state.t1_rag_chain = None
            pb  = st.progress(0, text="Starting…")
            sta = st.empty()
            try:
                result = run_full_pipeline(
                    source_val, lang,
                    lambda pct: pb.progress(pct, text="Working…"),
                    lambda msg: sta.markdown(f'<div class="ainfo">{msg}</div>', unsafe_allow_html=True),
                )
                st.session_state.t1_result    = result
                st.session_state.t1_rag_chain = result["rag_chain"]
                st.session_state.t1_chat      = []
                sta.markdown('<div class="aok">🎉 Done! Scroll down for results.</div>', unsafe_allow_html=True)
            except Exception as e:
                sta.markdown(f'<div class="aerr">❌ Error: {e}</div>', unsafe_allow_html=True)
            finally:
                st.session_state.t1_processing = False
            time.sleep(1)
            st.rerun()

    if st.session_state.t1_result:
        r = st.session_state.t1_result
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        words_p = len(st.session_state.t1_result["transcript"].split())
        st.markdown(
            f'<div class="sh">'
            f'<span class="sh-t">✅ Transcript Ready — {words_p:,} words</span>'
            f'<span class="sh-b">RAG Ready · Ask Anything</span></div>',
            unsafe_allow_html=True
        )
        render_results(r, "t1_chat", "t1_rag_chain", "t1")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="ctop">
        <div class="clbl">Meeting Notes Generator</div>
        <div class="ctitle">Upload your recording → structured notes, zero effort</div>
        <div class="cbody">
            Upload a meeting recording or paste a YouTube/Loom URL.
            Nuance extracts the audio, transcribes it with Whisper, then automatically
            generates a <b>Summary</b>, <b>Meeting Notes</b>, <b>Action Items</b>, and
            <b>Open Questions</b> — capturing every nuance in clean visual cards. No prompting needed.
        </div>
    </div>
    """, unsafe_allow_html=True)

    inp_col, lang_col = st.columns([3, 1], gap="large")

    with inp_col:
        t2_src = st.radio("Input type", ["YouTube / Web URL", "Local File"],
                          horizontal=True, key="t2_src_type")
        if t2_src == "YouTube / Web URL":
            t2_url = st.text_input("Meeting URL",
                                   placeholder="https://www.youtube.com/watch?v=… or Loom/direct URL",
                                   label_visibility="collapsed", key="t2_url")
            t2_source = t2_url.strip() if t2_url.strip() else None
            st.markdown('<div class="ainfo">ℹ️ Paste any YouTube, Loom, or direct audio/video URL</div>',
                        unsafe_allow_html=True)
        else:
            t2_up = st.file_uploader("Meeting recording",
                                     type=["mp4","mp3","wav","m4a","webm","ogg","mkv","mov"],
                                     label_visibility="collapsed", key="t2_upload")
            t2_source = None
            if t2_up:
                t2_source = save_upload(t2_up)
                st.markdown(f'<div class="aok">✅ {t2_up.name} — {round(t2_up.size/1e6,1)} MB</div>',
                            unsafe_allow_html=True)

    with lang_col:
        t2_lang = st.selectbox("Language", ["english","hinglish"], key="t2_lang")
        if t2_lang == "hinglish":
            st.markdown('<div class="awarn">Powered by Sarvam AI</div>', unsafe_allow_html=True)

    run2_col, _ = st.columns([1, 2])
    with run2_col:
        go2 = st.button("📋 Generate Meeting Notes", key="t2_go",
                        disabled=st.session_state.t2_processing)

    if go2:
        if not t2_source:
            st.markdown('<div class="awarn">⚠️ Provide a URL or upload a file first.</div>',
                        unsafe_allow_html=True)
        else:
            st.session_state.t2_processing = True
            st.session_state.t2_post_result = None
            st.session_state.t2_transcript = ""
            st.session_state.t2_chat = []
            pb2  = st.progress(0)
            sta2 = st.empty()
            try:
                from utils.audio_processor import process_input
                from core.transcriber import transcribe_all
                from core.summarizer import summarize, generate_title
                from core.extractor import extract_action_items, extract_key_decisions, extract_questions

                sta2.markdown('<div class="ainfo">🔊 Extracting & chunking audio…</div>', unsafe_allow_html=True)
                pb2.progress(10)
                chunks = process_input(t2_source)

                engine = "Sarvam AI" if t2_lang == "hinglish" else "Whisper"
                sta2.markdown(f'<div class="ainfo">📝 Transcribing {len(chunks)} chunk(s) with {engine}…</div>',
                              unsafe_allow_html=True)
                pb2.progress(30)
                tx2 = transcribe_all(chunks, t2_lang)

                sta2.markdown('<div class="ainfo">🏷️ Generating title…</div>', unsafe_allow_html=True)
                pb2.progress(44)
                title2 = generate_title(tx2)

                sta2.markdown('<div class="ainfo">📋 Summarizing meeting…</div>', unsafe_allow_html=True)
                pb2.progress(56)
                summary2 = summarize(tx2)

                sta2.markdown('<div class="ainfo">✅ Extracting action items…</div>', unsafe_allow_html=True)
                pb2.progress(68)
                ai2 = extract_action_items(tx2)

                sta2.markdown('<div class="ainfo">🔑 Extracting key decisions & notes…</div>', unsafe_allow_html=True)
                pb2.progress(80)
                kd2 = extract_key_decisions(tx2)

                sta2.markdown('<div class="ainfo">❓ Extracting open questions…</div>', unsafe_allow_html=True)
                pb2.progress(92)
                oq2 = extract_questions(tx2)

                pb2.progress(100)
                sta2.markdown('<div class="aok">🎉 Meeting notes ready!</div>', unsafe_allow_html=True)

                st.session_state.t2_post_result = {
                    "title": title2, "transcript": tx2,
                    "summary": summary2, "action_items": ai2,
                    "key_decisions": kd2, "open_questions": oq2,
                }
            except Exception as e:
                sta2.markdown(f'<div class="aerr">❌ Error: {e}</div>', unsafe_allow_html=True)
            finally:
                st.session_state.t2_processing = False
            time.sleep(1)
            st.rerun()

    if st.session_state.t2_post_result:
        r2 = st.session_state.t2_post_result
        tx  = r2["transcript"]
        words = len(tx.split())

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="sh"><span class="sh-t">📌 {r2["title"]}</span></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="stats">'
            f'<div class="stat"><div class="v">{words:,}</div><div class="l">Words</div></div>'
            f'<div class="stat"><div class="v">~{round(words/130)}m</div><div class="l">Est. Duration</div></div>'
            f'<div class="stat"><div class="v">{tx.count(chr(10)+chr(10))+1}</div><div class="l">Paragraphs</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin:1.4rem 0 .7rem">
            <div style="width:3px;height:20px;background:linear-gradient(180deg,#60A5FA,#A78BFA);border-radius:3px"></div>
            <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#E2E8F0">Meeting Summary</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(
            f'''<div style="background:#0C1422;border:1px solid #1E2D4A;border-radius:14px;
                          padding:1.4rem 1.6rem;border-left:3px solid #60A5FA;
                          font-family:DM Sans,sans-serif;font-size:.9rem;
                          color:#CBD5E1;line-height:1.8">{r2["summary"]}</div>''',
            unsafe_allow_html=True
        )

        st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)

        card_r1, card_r2 = st.columns(2, gap="medium")
        with card_r1:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:.7rem">
                <div style="width:3px;height:20px;background:linear-gradient(180deg,#10B981,#059669);border-radius:3px"></div>
                <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#E2E8F0">✅ Action Items</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(
                f'''<div style="background:#0C1422;border:1px solid #1E2D4A;border-radius:14px;
                              padding:1.4rem 1.6rem;border-left:3px solid #10B981;
                              font-family:DM Sans,sans-serif;font-size:.88rem;
                              color:#CBD5E1;line-height:1.9;min-height:180px">{r2["action_items"]}</div>''',
                unsafe_allow_html=True
            )

        with card_r2:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:.7rem">
                <div style="width:3px;height:20px;background:linear-gradient(180deg,#F59E0B,#D97706);border-radius:3px"></div>
                <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#E2E8F0">❓ Open Questions</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(
                f'''<div style="background:#0C1422;border:1px solid #1E2D4A;border-radius:14px;
                              padding:1.4rem 1.6rem;border-left:3px solid #F59E0B;
                              font-family:DM Sans,sans-serif;font-size:.88rem;
                              color:#CBD5E1;line-height:1.9;min-height:180px">{r2["open_questions"]}</div>''',
                unsafe_allow_html=True
            )

        st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:.7rem">
            <div style="width:3px;height:20px;background:linear-gradient(180deg,#A78BFA,#7C3AED);border-radius:3px"></div>
            <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#E2E8F0">🔑 Key Decisions & Meeting Notes</span>
        </div>""", unsafe_allow_html=True)
        st.markdown(
            f'''<div style="background:#0C1422;border:1px solid #1E2D4A;border-radius:14px;
                          padding:1.4rem 1.6rem;border-left:3px solid #A78BFA;
                          font-family:DM Sans,sans-serif;font-size:.88rem;
                          color:#CBD5E1;line-height:1.9">{r2["key_decisions"]}</div>''',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<details class="tx-wrap"><summary>📄 View full Transcript</summary>'
            f'<div class="tx-inner"><div class="tx-box">{tx}</div></div></details>',
            unsafe_allow_html=True
        )


# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ft">
    <div class="ft-meta">Copyright © 2026 Bishwajit Pattanaik</div>
    <div class="ft-meta">
        <a href="https://www.linkedin.com/in/bishwajit-pattanaik-717818320/" target="_blank" class="ft-link">LinkedIn</a>
        &nbsp;·&nbsp;
        <a href="https://github.com/bishwajitpattanaik" target="_blank" class="ft-link2">GitHub</a>
    </div>
    <div class="ft-logo">Nuance AI</div>
</div>
""", unsafe_allow_html=True)