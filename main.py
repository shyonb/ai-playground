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
import httpx
from datetime import datetime

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
    model: Optional[str] = "gpt-4"
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
    AZURE_FOUNDRY_DEPLOYMENT_NAME = os.getenv("AZURE_FOUNDRY_DEPLOYMENT_NAME", "gpt-4")
    API_VERSION = os.getenv("AZURE_FOUNDRY_API_VERSION", "2024-02-15-preview")

config = Config()

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
        # Prepare the request to Azure Foundry
        headers = {
            "Content-Type": "application/json",
            "api-key": config.AZURE_FOUNDRY_API_KEY
        }
        
        payload = {
            "messages": [
                {"role": "user", "content": request.message}
            ],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "model": request.model
        }
        
        # Construct the full endpoint URL
        url = f"{config.AZURE_FOUNDRY_ENDPOINT}/openai/deployments/{config.AZURE_FOUNDRY_DEPLOYMENT_NAME}/chat/completions?api-version={config.API_VERSION}"
        
        # Make request to Azure Foundry
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Azure Foundry API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Azure Foundry API error: {response.status_code}"
                )
            
            result = response.json()
            
            # Extract response
            ai_response = result["choices"][0]["message"]["content"]
            tokens_used = result.get("usage", {}).get("total_tokens")
            
            return ChatResponse(
                response=ai_response,
                model=request.model,
                timestamp=datetime.now(),
                tokens_used=tokens_used
            )
            
    except httpx.TimeoutException:
        logger.error("Timeout calling Azure Foundry API")
        raise HTTPException(status_code=504, detail="Request timeout")
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
            name="gpt-4",
            description="GPT-4 model for advanced text generation",
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
