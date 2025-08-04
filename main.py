"""
FastAPI Backend for Azure Foundry Model Integration
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, cast, Any
from datetime import datetime
import logging
import os
from openai import AzureOpenAI

from app.models import (
    ChatRequest, ChatResponse, GenerateRequest, 
    HealthResponse, ModelInfo, ChatMessage
)
from app.config import get_settings
from app.dependencies import get_azure_openai_client, verify_token, clear_azure_client_cache

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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        message="Azure Foundry API is running",
        azure_endpoint=settings.AZURE_FOUNDRY_ENDPOINT
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
        settings = get_settings()
        
        # Convert our ChatMessage objects to the format expected by Azure OpenAI
        messages = cast(Any, [
            {"role": message.role, "content": message.content}
            for message in request.messages
        ])
        
        # Generate the completion
        completion = client.chat.completions.create(
            model=settings.AZURE_FOUNDRY_MODEL,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False  # Force non-streaming for now
        )
        
        # Convert Azure OpenAI response to our format
        choices = []
        for choice in completion.choices:
            choices.append({
                "index": choice.index,
                "message": {
                    "role": choice.message.role,
                    "content": choice.message.content
                },
                "finish_reason": choice.finish_reason
            })
        
        return ChatResponse(
            id=completion.id,
            object=completion.object,
            created=completion.created,
            model=completion.model,
            choices=choices,
            usage={
                "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
                "total_tokens": completion.usage.total_tokens if completion.usage else 0
            }
        )
        
    except Exception as e:
        logger.error(f"Error calling Azure Foundry: {str(e)}")
        # Clear cache in case of client issues
        clear_azure_client_cache()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Generate text endpoint
@app.post("/api/v1/generate")
async def generate_text(
    request: GenerateRequest,
    token: str = Depends(verify_token),
    client: AzureOpenAI = Depends(get_azure_openai_client)
):
    """
    Text generation endpoint - optimized for single-turn text generation tasks
    """
    try:
        settings = get_settings()
        
        # Prepare messages for text generation
        messages = cast(Any, [
            {
                "role": "system",
                "content": "You are a helpful AI assistant focused on generating high-quality text content."
            },
            {
                "role": "user", 
                "content": request.prompt
            }
        ])
        
        # Generate the completion
        completion = client.chat.completions.create(
            model=settings.AZURE_FOUNDRY_MODEL,
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
            "model": request.model or settings.AZURE_FOUNDRY_MODEL,
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
    settings = get_settings()
    
    # For now, return a static list
    # In production, you might query Azure Foundry for available models
    models = [
        ModelInfo(
            id="gpt-4o",
            object="model",
            owned_by="azure-foundry"
        ),
        ModelInfo(
            id="gpt-35-turbo",
            object="model",
            owned_by="azure-foundry"
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
