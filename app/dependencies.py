"""
FastAPI Dependencies
"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import lru_cache
import logging
from openai import AzureOpenAI
from .config import get_settings

logger = logging.getLogger(__name__)
security = HTTPBearer()


@lru_cache()
def get_azure_openai_client() -> AzureOpenAI:
    """
    Get Azure OpenAI client with LRU caching
    This approach:
    - Caches the client but allows for invalidation
    - Recreates client if configuration changes
    - Better error handling and recovery
    """
    settings = get_settings()
    
    if not settings.AZURE_FOUNDRY_ENDPOINT or not settings.AZURE_FOUNDRY_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="Azure Foundry configuration is missing. Please check AZURE_FOUNDRY_ENDPOINT and AZURE_FOUNDRY_API_KEY."
        )
    
    try:
        return AzureOpenAI(
            azure_endpoint=settings.AZURE_FOUNDRY_ENDPOINT,
            api_key=settings.AZURE_FOUNDRY_API_KEY,
            api_version=settings.AZURE_FOUNDRY_API_VERSION,
        )
    except Exception as e:
        logger.error(f"Failed to create Azure OpenAI client: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize Azure OpenAI client: {str(e)}"
        )


def clear_azure_client_cache():
    """Clear the cached Azure OpenAI client"""
    get_azure_openai_client.cache_clear()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token - implement your auth logic here"""
    # For now, we'll do basic validation
    # In production, implement proper JWT or API key validation
    if not credentials.credentials:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return credentials.credentials
