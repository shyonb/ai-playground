"""
Quick test of the restructured API
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    headers = {"Authorization": "Bearer test-token", "Content-Type": "application/json"}
    
    # Test health
    print("Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"Health Status: {response.status_code}")
    print(f"Health Response: {response.json()}")
    print()
    
    # Test models
    print("Testing models endpoint...")
    response = requests.get(f"{base_url}/api/v1/models", headers=headers)
    print(f"Models Status: {response.status_code}")
    print(f"Models Response: {response.json()}")
    print()
    
    # Test chat
    print("Testing chat endpoint...")
    chat_data = {
        "messages": [
            {"role": "user", "content": "Hello, are you working? Please respond briefly."}
        ],
        "max_tokens": 50
    }
    response = requests.post(f"{base_url}/api/v1/chat/completions", headers=headers, json=chat_data)
    print(f"Chat Status: {response.status_code}")
    
    if response.status_code == 200:
        chat_response = response.json()
        print(f"Chat Response: {chat_response['choices'][0]['message']['content']}")
        print(f"Model: {chat_response['model']}")
        print(f"Usage: {chat_response['usage']}")
    else:
        print(f"Chat Error: {response.text}")
    print()
    
    # Test generate
    print("Testing generate endpoint...")
    generate_data = {
        "prompt": "Write a short greeting.",
        "max_tokens": 30
    }
    response = requests.post(f"{base_url}/api/v1/generate", headers=headers, json=generate_data)
    print(f"Generate Status: {response.status_code}")
    
    if response.status_code == 200:
        generate_response = response.json()
        print(f"Generated Text: {generate_response['generated_text']}")
        print(f"Model: {generate_response['model']}")
        print(f"Tokens: {generate_response['tokens_used']}")
    else:
        print(f"Generate Error: {response.text}")

if __name__ == "__main__":
    test_api()
