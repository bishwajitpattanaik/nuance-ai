import streamlit as st
import time
import html

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VoxIQ · AI Video Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #08090d !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #08090d; }
::-webkit-scrollbar-thumb { background: #2e7d6b; border-radius: 2px; }

/* ── HERO SECTION ── */
.hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 60px 40px;
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(46,125,107,0.25) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 80% 60%, rgba(20,180,140,0.08) 0%, transparent 50%),
        #08090d;
}

.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(46,125,107,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(46,125,107,0.07) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridMove 20s linear infinite;
    pointer-events: none;
}

@keyframes gridMove {
    0% { transform: translateY(0); }
    100% { transform: translateY(60px); }
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    background: rgba(46,125,107,0.15);
    border: 1px solid rgba(46,125,107,0.4);
    border-radius: 100px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4ecba8;
    margin-bottom: 28px;
    animation: fadeUp 0.8s ease both;
}

.badge .dot {
    width: 6px;
    height: 6px;
    background: #4ecba8;
    border-radius: 50%;
    animation: pulse 2s ease infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(52px, 8vw, 96px);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -0.03em;
    text-align: center;
    color: #f0ece2;
    animation: fadeUp 0.9s 0.1s ease both;
    margin-bottom: 6px;
}

.hero-title span {
    background: linear-gradient(135deg, #4ecba8 0%, #2e7d6b 50%, #1ab88d 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 17px;
    color: #7a8a84;
    text-align: center;
    max-width: 520px;
    line-height: 1.65;
    margin: 20px auto 48px;
    animation: fadeUp 1s 0.2s ease both;
}

/* ── Transcript box ── */
.transcript-box {
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 12.5px;
    color: #6a7a74;
    line-height: 1.75;
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
</style>
""", unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-logo">Vox<span>IQ</span></div>
</div>
""", unsafe_allow_html=True)

# ── State init ────────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processing" not in st.session_state:
    st.session_state.processing = False

# ── Demo helpers ──────────────────────────────────────────────────────────────
def _demo_result(source):
    return {
        "title": "AI in Healthcare",
        "transcript": "This is a demo transcript.",
        "summary": "This is a demo summary.",
        "action_items": "1. Demo action",
        "key_decisions": "1. Demo decision",
        "open_questions": "1. Demo question",
        "rag_chain": None,
    }

def _demo_answer(question, result):
    return "Demo AI response."

# ── Hero ──────────────────────────────────────────────────────────────────────
if not st.session_state.result:

    st.markdown("""
    <div class="hero">
      <div class="badge"><div class="dot"></div>AI-powered · RAG · Real-time NLP</div>
      <div class="hero-title">Turn any video into<br><span>intelligence.</span></div>
      <p class="hero-sub">
        Paste a YouTube link or upload a video.
      </p>
    </div>
    """, unsafe_allow_html=True)

    yt_url = st.text_input("YouTube URL")

    if st.button("Analyze Video"):

        if not yt_url.strip():
            st.warning("Enter URL")
        else:

            prog = st.progress(0)

            for i in range(100):
                prog.progress(i + 1)
                time.sleep(0.01)

            try:
                from main import run_pipeline
                result = run_pipeline(yt_url, "english")
            except Exception:
                result = _demo_result(yt_url)

            st.session_state.result = result
            st.rerun()

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.result:

    r = st.session_state.result

    # FIXED: escaped transcript safely
    transcript = html.escape(r.get("transcript", ""))

    st.title(r.get("title", "Untitled"))

    tab1, tab2 = st.tabs(["Summary", "Transcript"])

    with tab1:
        st.write(r.get("summary", ""))

    with tab2:

        # FIXED: safe transcript rendering
        st.markdown(
            f'<div class="transcript-box">{transcript}</div>',
            unsafe_allow_html=True
        )

    st.subheader("Chat")

    # FIXED: escaped chat rendering
    for msg in st.session_state.chat_history:

        role = msg["role"]
        content = html.escape(msg["content"])

        st.markdown(
            f"""
            <div style="
                padding:12px;
                margin-bottom:10px;
                border-radius:10px;
                background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.05);
            ">
                <b>{role}:</b><br>{content}
            </div>
            """,
            unsafe_allow_html=True
        )

    q = st.text_input("Ask something")

    if st.button("Ask") and q.strip():

        st.session_state.chat_history.append({
            "role": "user",
            "content": q
        })

        answer = _demo_answer(q, r)

        st.session_state.chat_history.append({
            "role": "ai",
            "content": answer
        })

        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
text-align:center;
padding:20px;
font-size:11px;
opacity:0.6;
">
VOXIQ · AI VIDEO INTELLIGENCE
</div>
""", unsafe_allow_html=True)