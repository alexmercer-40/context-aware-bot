"""Document ingestion pipeline.

Extracts text from PDF and plain-text files, chunks the text, and stores the
chunks in the ChromaDB documents collection for RAG retrieval.
"""

import uuid
from pypdf import PdfReader
from rag.vectordb import documents_collection


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text content from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for embedding.

    Args:
        text: The full text to split.
        chunk_size: Maximum characters per chunk.
        overlap: Number of overlapping characters between consecutive chunks.

    Returns:
        A list of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks


def ingest_document(file_path: str, filename: str) -> int:
    """Ingest a document into the vector database.

    Args:
        file_path: Absolute path to the temporary file on disk.
        filename: Original filename (used for metadata).

    Returns:
        Number of chunks stored.
    """
    # Extract text based on file type
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    # Chunk the extracted text
    chunks = chunk_text(text)

    if not chunks:
        return 0

    # Store in ChromaDB
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"filename": filename, "chunk_index": i} for i in range(len(chunks))]

    documents_collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids,
    )

    return len(chunks)
