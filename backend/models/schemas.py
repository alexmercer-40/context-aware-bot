"""Pydantic request/response schemas for the FastAPI endpoints."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat message."""

    message: str = Field(..., example="What do you know about me?", description="The user's message to the chatbot")


class ChatResponse(BaseModel):
    """Non-streaming chat response."""

    response: str = Field(..., description="The assistant's complete reply")


class UploadResponse(BaseModel):
    """Response after a document has been ingested."""

    status: str = Field(..., example="ok")
    filename: str = Field(..., example="resume.pdf", description="Name of the uploaded file")
    chunks: int = Field(..., example=12, description="Number of text chunks created from the document")
