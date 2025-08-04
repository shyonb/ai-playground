#!/usr/bin/env python3
"""
Simple test script to verify Azure OpenAI client setup
"""
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_azure_openai_client():
    """Test the Azure OpenAI client setup"""
    
    # Get environment variables
    endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT")
    api_key = os.getenv("AZURE_FOUNDRY_API_KEY")
    deployment = os.getenv("AZURE_FOUNDRY_DEPLOYMENT_NAME", "gpt-4.1")
    api_version = os.getenv("AZURE_FOUNDRY_API_VERSION", "2025-01-01-preview")
    
    print("Testing Azure OpenAI Client Setup")
    print("-" * 40)
    print(f"Endpoint: {endpoint}")
    print(f"Deployment: {deployment}")
    print(f"API Version: {api_version}")
    print(f"API Key: {'*' * 10 if api_key else 'NOT SET'}")
    print("-" * 40)
    
    if not endpoint or not api_key:
        print("❌ Missing required environment variables!")
        print("Please check your .env file and ensure:")
        print("- AZURE_FOUNDRY_ENDPOINT is set")
        print("- AZURE_FOUNDRY_API_KEY is set")
        return False
    
    try:
        # Initialize client
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        
        # Test simple completion
        print("🧪 Testing chat completion...")
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello and confirm you're working!"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        response = completion.choices[0].message.content
        tokens_used = completion.usage.total_tokens if completion.usage else "unknown"
        
        print("✅ SUCCESS!")
        print(f"Response: {response}")
        print(f"Tokens used: {tokens_used}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_azure_openai_client()
    exit(0 if success else 1)
