# Context-Aware Chatbot

A full-stack chatbot with **long-term memory**, **RAG document Q&A**, **tool calling**, and **real-time SSE streaming**.

- **Backend:** FastAPI + [Strands Agents](https://github.com/strands-agents) + Google Gemini + ChromaDB
- **Frontend:** React + Vite + TailwindCSS

The agent remembers facts you share (name, skills, preferences) across the conversation by saving them to a vector store, and can answer questions about PDFs/text files you upload.

---

## Architecture

```
React (Vite, :5173)  ──/api proxy──▶  FastAPI (:8000)
                                          │
                          ┌───────────────┼───────────────┐
                          ▼               ▼               ▼
                    Strands Agent   ChromaDB         pypdf
                    + Gemini        (memory +        (ingestion)
                    (tool calling)   documents)
```

**Agent tools:** `save_memory`, `search_memory`, `delete_memory`, `search_document`.
Streaming uses Strands' native `stream_async`, surfaced to the browser as Server-Sent Events (`tool`, `token`, `done`, `error`).

---

## Prerequisites

> ⚠️ Neither Python nor Node.js was found on this machine. Install both before running:

- **Python 3.10+** — https://www.python.org/downloads/ (check "Add Python to PATH" during install)
- **Node.js 18+** — https://nodejs.org/ (includes `npm`)
- **A free Gemini API key** — https://aistudio.google.com/apikey

Verify after installing (open a new terminal):

```powershell
python --version
node --version
npm --version
```

---

## Backend setup

```powershell
cd backend

# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # PowerShell
# venv\Scripts\activate.bat      # cmd.exe

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key
copy .env.example .env
# then edit .env and set GEMINI_API_KEY=...

# 4. Run the API
uvicorn app:app --reload --port 8000
```

Check it: open http://localhost:8000/health → `{"status":"ok"}`.
Interactive API docs: http://localhost:8000/docs

### Endpoints

| Endpoint        | Method | Description                                |
|-----------------|--------|--------------------------------------------|
| `/health`       | GET    | Liveness probe                             |
| `/chat`         | POST   | Non-streaming chat (`{"message": "..."}`)  |
| `/chat/stream`  | POST   | SSE streaming chat (tokens + tool events)  |
| `/upload`       | POST   | Upload a PDF/text file for RAG ingestion   |
| `/memories`     | GET    | List all stored long-term memories         |

---

## Frontend setup

In a **second terminal**:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

The Vite dev server proxies `/api/*` to `http://localhost:8000`, so both must be running.

---

## Try it

1. **Memory** — Say *"My name is Shubham and I know React and Kotlin."*
   Watch the **Searching/Saving memory** indicator and see the fact appear in the
   left sidebar.
2. Ask *"What do you know about me?"* — the agent searches memory and answers.
3. **RAG** — Click the 📎 paperclip, drop in a PDF, then ask a question about it.
4. **Streaming** — Responses stream token-by-token; hit the ⏹ stop button to abort.

---

## Project structure

```
backend/
  app.py              FastAPI app + endpoints
  agent.py            Strands Agent + Gemini + streaming
  config.py           Env vars, constants, system prompt
  tools/              save/search/delete_memory, search_document
  rag/                vectordb (ChromaDB), ingest (chunking)
  models/schemas.py   Pydantic request/response models
  requirements.txt
  .env.example

frontend/
  src/
    App.jsx
    components/        ChatWindow, MessageBubble, InputBar,
                       Sidebar, FileUpload, ToolIndicator
    hooks/useChat.js   SSE streaming state machine
    api/chatApi.js     upload + memories clients
  package.json, vite.config.js, tailwind.config.js, ...
```

---

## Notes & next steps

- ChromaDB persists to `backend/db/` (git-ignored) and uses the built-in
  `all-MiniLM-L6-v2` embedding model — no extra setup.
- The architecture review (`architecture_review.md`) outlines stretch goals:
  reranking, background ingestion, a supervisor multi-agent pattern, rate
  limiting via Redis, structured user profiles in PostgreSQL, and Dockerization.
```
