"""
API Models and Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ModelType(str, Enum):
    GPT_4 = "gpt-4.1"
    GPT_35_TURBO = "gpt-35-turbo"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"

class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: ChatRole
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user message")
    model: Optional[ModelType] = Field(ModelType.GPT_4, description="The model to use")
    max_tokens: Optional[int] = Field(1000, ge=1, le=4000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: Optional[float] = Field(1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    presence_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Presence penalty")
    stop: Optional[List[str]] = Field(None, description="Stop sequences")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The generated response")
    model: str = Field(..., description="The model used")
    timestamp: datetime = Field(..., description="Response timestamp")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    finish_reason: Optional[str] = Field(None, description="Reason for completion")

class CompletionRequest(BaseModel):
    prompt: str = Field(..., description="The prompt text")
    model: Optional[ModelType] = Field(ModelType.GPT_4, description="The model to use")
    max_tokens: Optional[int] = Field(1000, ge=1, le=4000, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: Optional[float] = Field(1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Frequency penalty")
    presence_penalty: Optional[float] = Field(0.0, ge=-2.0, le=2.0, description="Presence penalty")
    stop: Optional[List[str]] = Field(None, description="Stop sequences")

class CompletionResponse(BaseModel):
    text: str = Field(..., description="The generated text")
    model: str = Field(..., description="The model used")
    timestamp: datetime = Field(..., description="Response timestamp")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    finish_reason: Optional[str] = Field(None, description="Reason for completion")

class EmbeddingRequest(BaseModel):
    input_text: str = Field(..., description="Text to embed")
    model: Optional[str] = Field("text-embedding-ada-002", description="Embedding model")

class EmbeddingResponse(BaseModel):
    embedding: List[float] = Field(..., description="The embedding vector")
    model: str = Field(..., description="The model used")
    timestamp: datetime = Field(..., description="Response timestamp")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
    uptime: Optional[str] = Field(None, description="Service uptime")

class ModelInfo(BaseModel):
    name: str = Field(..., description="Model name")
    description: str = Field(..., description="Model description")
    endpoint: str = Field(..., description="Model endpoint")
    status: str = Field(..., description="Model status")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens supported")
    capabilities: Optional[List[str]] = Field(None, description="Model capabilities")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(..., description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

class UsageStats(BaseModel):
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")
    total_tokens: int = Field(..., description="Total tokens processed")
    average_response_time: float = Field(..., description="Average response time in seconds")

class APIKeyRequest(BaseModel):
    name: str = Field(..., description="API key name")
    permissions: Optional[List[str]] = Field(None, description="API key permissions")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")

class APIKeyResponse(BaseModel):
    key_id: str = Field(..., description="API key ID")
    name: str = Field(..., description="API key name")
    key: str = Field(..., description="The actual API key")
    created_at: datetime = Field(..., description="Creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    permissions: List[str] = Field(..., description="API key permissions")
