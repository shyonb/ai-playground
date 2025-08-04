"""
Test client for Azure Foundry API
"""
import asyncio
import httpx
import json
from datetime import datetime

class TestClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = "test-key"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def test_health(self):
        """Test health endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            print(f"Health Check - Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
    
    async def test_chat_completion(self):
        """Test chat completion endpoint"""
        payload = {
            "message": "Hello, how are you today?",
            "model": "gpt-4",
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/chat/completions",
                json=payload,
                headers=self.headers,
                timeout=30.0
            )
            print(f"Chat Completion - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error: {response.text}")
            return response.status_code == 200
    
    async def test_generate_text(self):
        """Test text generation endpoint"""
        payload = {
            "message": "Write a short poem about artificial intelligence",
            "model": "gpt-4",
            "max_tokens": 200,
            "temperature": 0.8
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/generate",
                json=payload,
                headers=self.headers,
                timeout=30.0
            )
            print(f"Text Generation - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error: {response.text}")
            return response.status_code == 200
    
    async def test_list_models(self):
        """Test list models endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/v1/models")
            print(f"List Models - Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error: {response.text}")
            return response.status_code == 200
    
    async def run_all_tests(self):
        """Run all tests"""
        print("=== Azure Foundry API Test Suite ===")
        print(f"Testing against: {self.base_url}")
        print(f"Timestamp: {datetime.now()}")
        print("-" * 50)
        
        tests = [
            ("Health Check", self.test_health),
            ("List Models", self.test_list_models),
            ("Chat Completion", self.test_chat_completion),
            ("Text Generation", self.test_generate_text)
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n🧪 Running {test_name}...")
            try:
                success = await test_func()
                results[test_name] = "✅ PASSED" if success else "❌ FAILED"
            except Exception as e:
                print(f"Error: {str(e)}")
                results[test_name] = "❌ ERROR"
            print("-" * 30)
        
        print("\n=== Test Results ===")
        for test_name, result in results.items():
            print(f"{test_name}: {result}")
        
        passed = sum(1 for r in results.values() if "PASSED" in r)
        total = len(results)
        print(f"\nSummary: {passed}/{total} tests passed")

async def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Azure Foundry API")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--key", default="test-key", help="API key")
    
    args = parser.parse_args()
    
    client = TestClient(base_url=args.url, api_key=args.key)
    await client.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
