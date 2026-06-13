"""Document search tool for the Strands Agent.

Provides semantic search over uploaded document chunks stored in ChromaDB.
"""

from strands import tool
from rag.vectordb import documents_collection


@tool
def search_document(query: str) -> str:
    """Search through uploaded documents to find relevant information.

    Use this tool when the user asks questions about content from documents
    they have uploaded (resumes, PDFs, notes, etc.).

    Args:
        query: The search query describing what information to look for in the documents.
    """
    count = documents_collection.count()
    if count == 0:
        return "No documents have been uploaded yet."

    n_results = min(5, count)
    results = documents_collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    if not results["documents"] or not results["documents"][0]:
        return "No relevant document sections found."

    sections = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        source = meta.get("filename", "unknown")
        chunk_idx = meta.get("chunk_index", "?")
        sections.append(f"[Source: {source}, Chunk {chunk_idx}]\n{doc}")

    return "Relevant document sections:\n\n" + "\n\n---\n\n".join(sections)
