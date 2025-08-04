"""
Test client for Azure Foundry integration
"""
import asyncio
import json
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.dependencies import get_azure_openai_client

async def test_azure_client():
    """Test the Azure OpenAI client connection"""
    print("Testing Azure Foundry client connection...")
    
    try:
        # Get settings
        settings = get_settings()
        print(f"Endpoint: {settings.AZURE_FOUNDRY_ENDPOINT}")
        print(f"Model: {settings.AZURE_FOUNDRY_MODEL}")
        print(f"API Version: {settings.AZURE_FOUNDRY_API_VERSION}")
        
        # Get client
        client = get_azure_openai_client()
        print("✅ Client created successfully")
        
        # Test a simple completion
        print("\nTesting chat completion...")
        completion = client.chat.completions.create(
            model=settings.AZURE_FOUNDRY_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello and confirm you're working."}
            ],
            max_tokens=100
        )
        
        response = completion.choices[0].message.content
        print(f"✅ Response: {response}")
        print(f"✅ Model: {completion.model}")
        print(f"✅ Tokens used: {completion.usage.total_tokens if completion.usage else 'unknown'}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    result = asyncio.run(test_azure_client())
    sys.exit(0 if result else 1)
