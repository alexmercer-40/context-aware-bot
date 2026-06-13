"""Pydantic request/response schemas for the FastAPI endpoints."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Incoming chat message from the frontend."""

    message: str


class ChatResponse(BaseModel):
    """Non-streaming chat response."""

    response: str


class UploadResponse(BaseModel):
    """Response after a document has been ingested."""

    status: str
    filename: str
    chunks: int
