"""
FastAPI Backend for Azure Foundry Model Integration
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from functools import lru_cache
import os
import logging
from typing import Optional, List
from datetime import datetime
from openai import AzureOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app instance
app = FastAPI(
    title="Azure Foundry API",
    description="Backend API for Azure Foundry Model Integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "gpt-4.1"
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    model: str
    timestamp: datetime
    tokens_used: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

class ModelInfo(BaseModel):
    name: str
    description: str
    endpoint: str
    status: str

# Configuration
class Config:
    AZURE_FOUNDRY_ENDPOINT = os.getenv("AZURE_FOUNDRY_ENDPOINT", "")
    AZURE_FOUNDRY_API_KEY = os.getenv("AZURE_FOUNDRY_API_KEY", "")
    AZURE_FOUNDRY_DEPLOYMENT_NAME = os.getenv("AZURE_FOUNDRY_DEPLOYMENT_NAME", "gpt-4.1")
    API_VERSION = os.getenv("AZURE_FOUNDRY_API_VERSION", "2025-01-01-preview")

config = Config()

# Azure OpenAI client dependency with proper caching and error handling
@lru_cache()
def get_azure_openai_client() -> AzureOpenAI:
    """
    Get Azure OpenAI client with LRU caching
    This approach:
    - Caches the client but allows for invalidation
    - Recreates client if configuration changes
    - Better error handling and recovery
    """
    if not config.AZURE_FOUNDRY_ENDPOINT or not config.AZURE_FOUNDRY_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Azure Foundry configuration is missing. Please check AZURE_FOUNDRY_ENDPOINT and AZURE_FOUNDRY_API_KEY."
        )
    
    try:
        return AzureOpenAI(
            azure_endpoint=config.AZURE_FOUNDRY_ENDPOINT,
            api_key=config.AZURE_FOUNDRY_API_KEY,
            api_version=config.API_VERSION,
        )
    except Exception as e:
        logger.error(f"Failed to create Azure OpenAI client: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize Azure OpenAI client: {str(e)}"
        )

# Function to clear cache if needed (for configuration changes)
def clear_azure_client_cache():
    """Clear the cached Azure OpenAI client"""
    get_azure_openai_client.cache_clear()

# Dependency for API key validation
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token - implement your auth logic here"""
    # For now, we'll do basic validation
    # In production, implement proper JWT or API key validation
    if not credentials.credentials:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return credentials.credentials

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Azure Foundry API is running", "docs": "/docs"}

# Chat completion endpoint
@app.post("/api/v1/chat/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    token: str = Depends(verify_token),
    client: AzureOpenAI = Depends(get_azure_openai_client)
):
    """
    Chat completion using Azure Foundry model
    """
    try:
        # Prepare the chat messages in the correct format
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user", 
                "content": request.message
            }
        ]
        
        # Generate the completion
        completion = client.chat.completions.create(
            model=config.AZURE_FOUNDRY_DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        
        # Extract response
        ai_response = completion.choices[0].message.content
        tokens_used = completion.usage.total_tokens if completion.usage else None
        
        return ChatResponse(
            response=ai_response,
            model=request.model or config.AZURE_FOUNDRY_DEPLOYMENT_NAME,
            timestamp=datetime.now(),
            tokens_used=tokens_used
        )
        
    except Exception as e:
        logger.error(f"Error calling Azure Foundry: {str(e)}")
        # Clear cache in case of client issues
        clear_azure_client_cache()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Generate text endpoint
@app.post("/api/v1/generate")
async def generate_text(
    request: ChatRequest,
    token: str = Depends(verify_token),
    client: AzureOpenAI = Depends(get_azure_openai_client)
):
    """
    Text generation endpoint - optimized for single-turn text generation tasks
    Future: Add business logic for content filtering, custom prompts, etc.
    """
    try:
        # Prepare messages for text generation (simpler system prompt)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant focused on generating high-quality text content."
            },
            {
                "role": "user", 
                "content": request.message
            }
        ]
        
        # Generate the completion
        completion = client.chat.completions.create(
            model=config.AZURE_FOUNDRY_DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )
        
        
        
        # Extract response
        generated_text = completion.choices[0].message.content
        tokens_used = completion.usage.total_tokens if completion.usage else None
        
        # Return with generate-specific response format
        return {
            "generated_text": generated_text,
            "model": request.model or config.AZURE_FOUNDRY_DEPLOYMENT_NAME,
            "timestamp": datetime.now(),
            "tokens_used": tokens_used,
            "generation_type": "text_completion"
        }
        
    except Exception as e:
        logger.error(f"Error in text generation: {str(e)}")
        # Clear cache in case of client issues
        clear_azure_client_cache()
        raise HTTPException(status_code=500, detail=f"Text generation error: {str(e)}")

# List available models
@app.get("/api/v1/models", response_model=List[ModelInfo])
async def list_models():
    """
    List available models
    """
    # For now, return a static list
    # In production, you might query Azure Foundry for available models
    models = [
        ModelInfo(
            name="gpt-4.1",
            description="gpt-4.1 model for advanced text generation",
            endpoint=f"{config.AZURE_FOUNDRY_ENDPOINT}/openai/deployments/{config.AZURE_FOUNDRY_DEPLOYMENT_NAME}",
            status="active"
        ),
        ModelInfo(
            name="gpt-35-turbo",
            description="GPT-3.5 Turbo for faster responses",
            endpoint=f"{config.AZURE_FOUNDRY_ENDPOINT}/openai/deployments/gpt-35-turbo",
            status="active"
        )
    ]
    return models

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
