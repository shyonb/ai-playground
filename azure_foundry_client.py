"""
Azure Foundry Client - Utility class for interacting with Azure Foundry
"""
import os
import httpx
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AzureFoundryClient:
    """Client for Azure Foundry API"""
    
    def __init__(
        self,
        endpoint: str = None,
        api_key: str = None,
        deployment_name: str = None,
        api_version: str = "2024-02-15-preview"
    ):
        self.endpoint = endpoint or os.getenv("AZURE_FOUNDRY_ENDPOINT", "")
        self.api_key = api_key or os.getenv("AZURE_FOUNDRY_API_KEY", "")
        self.deployment_name = deployment_name or os.getenv("AZURE_FOUNDRY_DEPLOYMENT_NAME", "gpt-4.1")
        self.api_version = api_version
        
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure Foundry endpoint and API key are required")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
    
    def _get_url(self, endpoint_path: str) -> str:
        """Construct full URL for API endpoint"""
        base_url = f"{self.endpoint}/openai/deployments/{self.deployment_name}"
        return f"{base_url}/{endpoint_path}?api-version={self.api_version}"
    
    async def chat_completion(
        self,
        messages: list,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate chat completion
        """
        payload = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        
        if stop:
            payload["stop"] = stop
        
        url = self._get_url("chat/completions")
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Azure Foundry API error: {response.status_code} - {response.text}")
                raise Exception(f"Azure Foundry API error: {response.status_code}")
            
            return response.json()
    
    async def completions(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate text completion
        """
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        
        if stop:
            payload["stop"] = stop
        
        url = self._get_url("completions")
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Azure Foundry API error: {response.status_code} - {response.text}")
                raise Exception(f"Azure Foundry API error: {response.status_code}")
            
            return response.json()
    
    async def embeddings(
        self,
        input_text: str,
        model: str = "text-embedding-ada-002"
    ) -> Dict[str, Any]:
        """
        Generate embeddings
        """
        payload = {
            "input": input_text,
            "model": model
        }
        
        url = self._get_url("embeddings")
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Azure Foundry API error: {response.status_code} - {response.text}")
                raise Exception(f"Azure Foundry API error: {response.status_code}")
            
            return response.json()
