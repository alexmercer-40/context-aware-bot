"""ChromaDB vector database initialization.

Creates a persistent ChromaDB client and two collections:
  - chat_memory:  stores user facts, preferences, and personal details
  - documents:    stores RAG document chunks from uploaded files
"""

import chromadb
from config import CHROMADB_PATH, MEMORY_COLLECTION, DOCUMENTS_COLLECTION

# ── Persistent client — data survives server restarts ─────────────────────────
client = chromadb.PersistentClient(path=CHROMADB_PATH)

# ── Collections ───────────────────────────────────────────────────────────────
memory_collection = client.get_or_create_collection(
    name=MEMORY_COLLECTION,
    metadata={"hnsw:space": "cosine"},
)

documents_collection = client.get_or_create_collection(
    name=DOCUMENTS_COLLECTION,
    metadata={"hnsw:space": "cosine"},
)
