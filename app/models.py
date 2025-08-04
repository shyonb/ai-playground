"""
Pydantic models for the Azure Foundry API
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    """A single chat message"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Request model for chat completion"""
    messages: List[ChatMessage]
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    """Response model for chat completion"""
    id: str
    object: str
    created: int
    model: str
    choices: List[dict]
    usage: dict


class GenerateRequest(BaseModel):
    """Request model for text generation"""
    prompt: str
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str
    azure_endpoint: Optional[str] = None


class ModelInfo(BaseModel):
    """Model information"""
    id: str
    object: str
    owned_by: str
