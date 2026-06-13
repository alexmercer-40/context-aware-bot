"""FastAPI application — endpoints for chat, streaming, file upload, and memories."""

import asyncio
import logging
import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse, ServerSentEvent

from models.schemas import ChatRequest, ChatResponse, UploadResponse
from agent import create_agent, stream_agent
from rag.ingest import ingest_document
from rag.vectordb import memory_collection, documents_collection

log = logging.getLogger("app")

app = FastAPI(
    title="Context-Aware Chatbot API",
    description=(
        "A GenAI-powered chatbot with **long-term memory** and **RAG** (Retrieval-Augmented Generation). "
        "Built with FastAPI, Strands Agent, Google Gemini, and ChromaDB.\n\n"
        "### Features\n"
        "- **Chat** — streaming & non-streaming responses via Gemini LLM\n"
        "- **Memory** — automatically remembers user facts across conversations\n"
        "- **RAG** — upload PDFs/text files and ask questions about them\n"
        "- **Tool Calling** — agent autonomously decides when to save/search memory or documents"
    ),
    version="1.0.0",
    contact={"name": "Rachit Raj Singh", "url": "https://github.com/alexmercer-40/context-aware-bot"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health():
    """Check if the API is running and which model is configured."""
    from config import MODEL_ID, GEMINI_API_KEY
    key_preview = GEMINI_API_KEY[:8] + "..." if len(GEMINI_API_KEY) > 8 else "(not set)"
    return {"status": "ok", "model": MODEL_ID, "key_prefix": key_preview}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(req: ChatRequest):
    """Send a message and receive the complete response (non-streaming).

    The agent may internally call tools (save_memory, search_memory, search_document)
    before returning the final answer."""
    try:
        agent = create_agent()
        result = agent(req.message)
        if hasattr(result, "message"):
            msg = result.message
            if isinstance(msg, dict) and "content" in msg:
                parts = msg["content"]
                text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
            else:
                text = str(msg)
        else:
            text = str(result)
        return ChatResponse(response=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream", tags=["Chat"])
async def chat_stream(req: ChatRequest):
    """Stream a chat response via Server-Sent Events (SSE).

    **Event types:**
    - `token` — a text chunk of the assistant's reply
    - `tool` — name of a tool the agent is currently invoking
    - `done` — final complete response text
    - `error` — error message if something went wrong"""

    async def event_generator():
        agent = create_agent()
        log.info("Created fresh agent for stream request")
        async for event in stream_agent(agent, req.message):
            yield ServerSentEvent(data=event["data"], event=event["event"])

    return EventSourceResponse(event_generator())


@app.post("/upload", response_model=UploadResponse, tags=["Documents"])
async def upload(file: UploadFile = File(...)):
    """Upload a PDF, TXT, or Markdown file for RAG ingestion.

    The file is chunked, embedded, and stored in ChromaDB. Once uploaded,
    the chatbot can answer questions about its content via the `search_document` tool."""
    allowed = (".pdf", ".txt", ".md")
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(allowed)}",
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        chunks = ingest_document(tmp_path, file.filename)
        return UploadResponse(status="ok", filename=file.filename, chunks=chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.get("/memories", tags=["Memory"])
async def get_memories():
    """Retrieve all long-term memories stored about the user.

    Memories are auto-saved by the agent when users share personal info
    (name, skills, preferences, goals)."""
    count = memory_collection.count()
    if count == 0:
        return {"memories": []}

    all_data = memory_collection.get(
        limit=count,
        include=["documents", "metadatas"],
    )

    memories = []
    for doc, meta, mid in zip(
        all_data["documents"],
        all_data["metadatas"],
        all_data["ids"],
    ):
        memories.append({
            "id": mid,
            "category": meta.get("category", "general"),
            "text": doc,
        })

    return {"memories": memories}


@app.get("/documents", tags=["Documents"])
async def get_documents():
    """List all uploaded documents with their chunk counts."""
    count = documents_collection.count()
    if count == 0:
        return {"documents": []}

    all_data = documents_collection.get(
        limit=count,
        include=["metadatas"],
    )

    file_chunks = {}
    for meta in all_data["metadatas"]:
        fname = meta.get("filename", "unknown")
        file_chunks[fname] = file_chunks.get(fname, 0) + 1

    documents = [
        {"filename": fname, "chunks": cnt}
        for fname, cnt in file_chunks.items()
    ]

    return {"documents": documents}
