"""
FastAPI Backend for Azure Foundry Model Integration
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
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

# Initialize Azure OpenAI client
def get_azure_openai_client():
    """Get Azure OpenAI client"""
    return AzureOpenAI(
        azure_endpoint=config.AZURE_FOUNDRY_ENDPOINT,
        api_key=config.AZURE_FOUNDRY_API_KEY,
        api_version=config.API_VERSION,
    )

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
    token: str = Depends(verify_token)
):
    """
    Chat completion using Azure Foundry model
    """
    try:
        # Get Azure OpenAI client
        client = get_azure_openai_client()
        
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
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Generate text endpoint
@app.post("/api/v1/generate")
async def generate_text(
    request: ChatRequest,
    token: str = Depends(verify_token)
):
    """
    Text generation endpoint - simple wrapper around chat completion
    """
    try:
        # Use the chat completion endpoint internally
        response = await chat_completion(request, token)
        return {
            "generated_text": response.response,
            "model": response.model,
            "timestamp": response.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
