# Nuance AI

> Every word. Every detail. Captured.

An end-to-end AI pipeline for video and meeting intelligence — transcribes any audio/video using Groq Whisper API, builds a RAG knowledge base with ChromaDB + Mistral AI, and auto-generates structured meeting notes (Summary, Action Items, Key Decisions, Open Questions) in a production-ready Streamlit web app.

🌐 **Live Demo:** [nuance-ai-bishwajitpattanaik.streamlit.app](https://nuance-ai-bishwajitpattanaik.streamlit.app)

---

## 💻 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web app framework |
| Groq Whisper API (`whisper-large-v3-turbo`) | Speech-to-text (English) |
| Sarvam AI (`saaras:v2.5`) | Speech-to-text (Hinglish) |
| Mistral AI (`mistral-small-latest`) | LLM for summarization, extraction, Q&A |
| LangChain (LCEL) | LLM orchestration & RAG pipeline |
| ChromaDB | Local vector store |
| HuggingFace `all-MiniLM-L6-v2` | Sentence embeddings |
| pydub + ffmpeg | Audio conversion & chunking |

**Cloud Services**

| Service | Purpose |
|---|---|
| Streamlit Cloud | App deployment & hosting |
| GitHub | Source control & CI/CD trigger |
| Groq Cloud | Whisper transcription API |
| Mistral AI Cloud | LLM inference |
| Sarvam AI | Hinglish STT-translate API |

---

## ✨ Features

**💬 Transcribe & Ask Questions Tab**
- Upload any audio/video file (mp3, mp4, wav, m4a, webm, ogg, mkv, mov)
- Transcribes with Groq Whisper API (English) or Sarvam AI (Hinglish)
- Builds a RAG knowledge base from the transcript
- Chat interface to ask any question about the content
- Quick-prompt suggestion chips
- Word count, sentence count, estimated duration stats
- Collapsible transcript viewer
- Download transcript as `.txt`

**📋 Meeting Notes Generator Tab**
- Upload a meeting recording
- Auto-generates: Summary, Action Items, Key Decisions, Open Questions
- Clean visual cards with color-coded sections
- Estimated duration and paragraph count stats
- Collapsible full transcript view
- Download complete meeting notes as `.txt`

**🔒 YouTube URL Support**
- Works fully in local development via `yt-dlp`
- Disabled on the hosted deployment — see the **⚠️ Why YouTube URL Does Not Work on the Hosted Deployment** section below

---

## 🤖 AI Pipeline

```
Audio/Video File (or YouTube URL — local only)
        │
        ▼
┌───────────────────────┐
│   Audio Processing    │
│   pydub + ffmpeg      │
│   → mono 16kHz WAV    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│   Audio Chunking      │
│   10-min chunks       │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────────────┐
│   Speech-to-Text              │
│   English → Groq Whisper API  │
│   Hinglish → Sarvam AI        │
└──────────┬────────────────────┘
           │
           ▼
┌───────────────────────┐
│   Full Transcript     │
└──────────┬────────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌─────────┐  ┌──────────────────────┐
│Mistral  │  │  ChromaDB            │
│(Summary,│  │  Vector Store        │
│Actions, │  │  (sentence-          │
│Decisions│  │   transformers       │
│Questions│  │   embeddings)        │
│Title)   │  │        │             │
└─────────┘  │   Mistral AI         │
             │   RAG Q&A Chat       │
             └──────────────────────┘
```

---

## 📁 Project Structure

```
nuance-ai/
│
├── app.py                        # Streamlit UI — main entry point
├── main.py                       # CLI entry point (local use)
├── requirements.txt              # Deployment dependencies
├── packages.txt                  # System packages (ffmpeg, nodejs)
├── .env                          # API keys — never commit this
│
├── core/
│   ├── transcriber.py            # Groq + Sarvam transcription routing
│   ├── summarizer.py             # LangChain summarization chain
│   ├── extractor.py              # Action items, decisions, questions
│   ├── rag_engine.py             # RAG pipeline (retrieval + generation)
│   └── vector_store.py           # ChromaDB vector store management
│
└── utils/
    └── audio_processor.py        # Audio conversion + chunking
```

> **PreDeploy versions** of `transcriber.py` and `audio_processor.py` are preserved as `transcriberPreDeploy.py` and `audio_processorPreDeploy.py` — these use local Whisper and `yt-dlp` for full local functionality.

---

## ⚙️ Setup & Installation

**1. Clone the repository**

```bash
git clone https://github.com/bishwajitpattanaik/nuance-ai.git
cd nuance-ai
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Install ffmpeg**

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Windows — https://ffmpeg.org/download.html
```

**5. Set up API keys**

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

| Key | Get it from | Cost |
|---|---|---|
| `MISTRAL_API_KEY` | [console.mistral.ai](https://console.mistral.ai) | Free tier |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) | Free — no credit card |
| `SARVAM_API_KEY` | [dashboard.sarvam.ai](https://dashboard.sarvam.ai) | Free tier — Hinglish only |

**6. Run the app**

```bash
streamlit run app.py
```

> App runs on `http://localhost:8501`

---

## 🎬 YouTube URL Support

Nuance supports YouTube URL ingestion via `yt-dlp` in local development.

**How it works locally:**

```
YouTube URL → yt-dlp downloads audio → pydub converts to WAV → chunked → Groq transcription → RAG pipeline
```

To enable YouTube support locally, install the pre-deploy requirements:

```bash
pip install -r requirementsPreDeploy.txt
```

Then paste any YouTube URL in the app and click **Transcribe**.

---

## ⚠️ Why YouTube URL Does Not Work on the Hosted Deployment

**This is a known cloud infrastructure limitation — not a bug in the code.**

YouTube URL ingestion works perfectly in local development. On the hosted Streamlit Cloud deployment, it is disabled for the following reasons:

**1. YouTube actively blocks cloud server IPs**

YouTube detects and blocks HTTP requests from well-known cloud provider IP ranges — AWS, GCP, and Azure. Streamlit Cloud runs on these providers, so any `yt-dlp` download attempt is rejected with a `403` or `429` error regardless of how the request is structured.

**2. yt-dlp requires constant maintenance at scale**

YouTube frequently changes its internal API, signature algorithms, and bot-detection mechanisms. `yt-dlp` releases patches to keep up, but on a hosted deployment this means the feature can break silently overnight — an unsustainable maintenance overhead.

**3. Streamlit Cloud network restrictions**

Streamlit Cloud imposes additional network-level restrictions that further limit outbound requests to YouTube's CDN endpoints.

**What to do instead:** Upload your audio or video file directly. All formats work perfectly on the hosted deployment: `mp3, mp4, wav, m4a, webm, ogg, mkv, mov`

---

## 🔄 Local vs Deployment — What Changes

### Dependencies

| Package | Local | Deployed | Reason |
|---|---|---|---|
| `yt-dlp` | ✅ | ❌ | YouTube blocked on cloud IPs |
| `openai-whisper` | ✅ | ❌ | Too heavy for cloud; runs locally |
| `torch>=2.9.0` | ✅ | ❌ | Required by local Whisper only |
| `ffmpeg-python` | ✅ | ❌ | Not needed without yt-dlp |
| `groq>=0.9.0` | ❌ | ✅ | Replaces local Whisper on cloud |
| `torchvision` | ✅ pinned | ✅ unpinned | Still needed by sentence-transformers |

### Transcription Engine

| Environment | Engine |
|---|---|
| Local | OpenAI Whisper — runs on your machine via `torch` |
| Deployed | Groq Whisper API — `whisper-large-v3-turbo` via API call |

### Audio Source

| Environment | YouTube URL | Local File |
|---|---|---|
| Local | ✅ via `yt-dlp` | ✅ |
| Deployed | ❌ Disabled | ✅ |

---

## 🚀 Deployment (Streamlit Cloud)

**1.** Push your repo to GitHub

**2.** Go to [share.streamlit.io](https://share.streamlit.io) → connect repo → set main file as `app.py`

**3.** Add secrets under **App Settings → Secrets:**

```toml
MISTRAL_API_KEY = "your_mistral_api_key"
GROQ_API_KEY = "your_groq_api_key"
SARVAM_API_KEY = "your_sarvam_api_key"
```

**4.** Deploy — Streamlit installs `requirements.txt` and `packages.txt` automatically.

> Every push to `main` triggers an automatic redeploy.

---

## 📦 API Free Tiers

| API | Free Limit |
|---|---|
| Groq Whisper | 7 hours of audio/day — no credit card |
| Mistral AI | Free tier available |
| Sarvam AI | Free tier available |

---

## 👤 Author

Built by **Bishwajit Pattanaik**

- 💼 LinkedIn: [linkedin.com/in/bishwajit-pattanaik-717818320](https://www.linkedin.com/in/bishwajit-pattanaik-717818320/)
- 🔗 GitHub: [github.com/bishwajitpattanaik](https://github.com/bishwajitpattanaik)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
