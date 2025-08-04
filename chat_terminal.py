#!/usr/bin/env python3
"""
Interactive Terminal Chat Client for Azure Foundry API
"""
import asyncio
import httpx
import json
import sys
from datetime import datetime
import argparse
from typing import Optional

class TerminalChatClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = "test-key"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.session_history = []
    
    def print_banner(self):
        """Print welcome banner"""
        print("=" * 60)
        print("🤖 Azure Foundry API Terminal Chat Client")
        print("=" * 60)
        print(f"Connected to: {self.base_url}")
        print("Commands:")
        print("  /help     - Show this help")
        print("  /history  - Show chat history")
        print("  /clear    - Clear chat history")
        print("  /models   - List available models")
        print("  /health   - Check API health")
        print("  /generate - Use text generation endpoint")
        print("  /chat     - Use chat completion endpoint (default)")
        print("  /quit     - Exit the chat")
        print("=" * 60)
        print("Type your message and press Enter to chat!")
        print()
    
    async def check_health(self):
        """Check API health"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ API Status: {data['status']}")
                    print(f"📅 Timestamp: {data['timestamp']}")
                    print(f"🔢 Version: {data['version']}")
                else:
                    print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking health: {str(e)}")
    
    async def list_models(self):
        """List available models"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/v1/models")
                if response.status_code == 200:
                    models = response.json()
                    print("📋 Available Models:")
                    for model in models:
                        print(f"  • {model['name']}: {model['description']} ({model['status']})")
                else:
                    print(f"❌ Failed to list models: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing models: {str(e)}")
    
    async def chat_completion(self, message: str, model: str = "gpt-4.1", max_tokens: int = 1000, temperature: float = 0.7):
        """Send chat completion request"""
        payload = {
            "message": message,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/chat/completions",
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["response"]
                    tokens = data.get("tokens_used", "unknown")
                    
                    # Add to session history
                    self.session_history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "user": message,
                        "assistant": ai_response,
                        "tokens": tokens,
                        "endpoint": "chat"
                    })
                    
                    print(f"🤖 Assistant: {ai_response}")
                    print(f"📊 Tokens used: {tokens}")
                    return True
                else:
                    print(f"❌ Chat failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    async def text_generation(self, message: str, model: str = "gpt-4.1", max_tokens: int = 1000, temperature: float = 0.8):
        """Send text generation request"""
        payload = {
            "message": message,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/generate",
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    generated_text = data["generated_text"]
                    tokens = data.get("tokens_used", "unknown")
                    
                    # Add to session history
                    self.session_history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "user": message,
                        "assistant": generated_text,
                        "tokens": tokens,
                        "endpoint": "generate"
                    })
                    
                    print(f"📝 Generated: {generated_text}")
                    print(f"📊 Tokens used: {tokens}")
                    return True
                else:
                    print(f"❌ Generation failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def show_history(self):
        """Show chat session history"""
        if not self.session_history:
            print("📝 No chat history yet.")
            return
        
        print("📚 Chat History:")
        print("-" * 50)
        for i, entry in enumerate(self.session_history, 1):
            print(f"{i}. [{entry['timestamp']}] ({entry['endpoint']})")
            print(f"   👤 You: {entry['user']}")
            print(f"   🤖 AI: {entry['assistant'][:100]}{'...' if len(entry['assistant']) > 100 else ''}")
            print(f"   📊 Tokens: {entry['tokens']}")
            print()
    
    def clear_history(self):
        """Clear chat history"""
        self.session_history.clear()
        print("🗑️ Chat history cleared.")
    
    def show_help(self):
        """Show help message"""
        print("\n📖 Available Commands:")
        print("  /help     - Show this help")
        print("  /history  - Show chat history")
        print("  /clear    - Clear chat history")
        print("  /models   - List available models")
        print("  /health   - Check API health")
        print("  /generate <message> - Use text generation endpoint")
        print("  /chat <message>     - Use chat completion endpoint")
        print("  /quit     - Exit the chat")
        print("\n💡 Tips:")
        print("  - Just type your message for chat completion")
        print("  - Use /generate for creative text generation")
        print("  - Check /models to see what's available")
        print()
    
    async def run_interactive(self):
        """Run interactive chat session"""
        self.print_banner()
        
        # Check if API is running
        print("🔍 Checking API connection...")
        await self.check_health()
        print()
        
        mode = "chat"  # Default mode
        
        while True:
            try:
                # Get user input
                prompt = f"[{mode}] 💬 You: "
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    command_parts = user_input.split(' ', 1)
                    command = command_parts[0].lower()
                    args = command_parts[1] if len(command_parts) > 1 else ""
                    
                    if command == '/quit' or command == '/exit':
                        print("👋 Goodbye!")
                        break
                    elif command == '/help':
                        self.show_help()
                    elif command == '/history':
                        self.show_history()
                    elif command == '/clear':
                        self.clear_history()
                    elif command == '/models':
                        await self.list_models()
                    elif command == '/health':
                        await self.check_health()
                    elif command == '/generate':
                        if args:
                            mode = "generate"
                            await self.text_generation(args)
                        else:
                            mode = "generate"
                            print("🔄 Switched to text generation mode. Type your prompt:")
                    elif command == '/chat':
                        if args:
                            mode = "chat"
                            await self.chat_completion(args)
                        else:
                            mode = "chat"
                            print("🔄 Switched to chat mode. Type your message:")
                    else:
                        print(f"❓ Unknown command: {command}")
                        print("Type /help for available commands.")
                else:
                    # Regular message - use current mode
                    if mode == "generate":
                        await self.text_generation(user_input)
                    else:
                        await self.chat_completion(user_input)
                
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Terminal Chat Client for Azure Foundry API")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--key", default="test-key", help="API key")
    parser.add_argument("--message", help="Send single message and exit")
    parser.add_argument("--generate", action="store_true", help="Use text generation endpoint")
    
    args = parser.parse_args()
    
    client = TerminalChatClient(base_url=args.url, api_key=args.key)
    
    # If single message provided, send it and exit
    if args.message:
        if args.generate:
            await client.text_generation(args.message)
        else:
            await client.chat_completion(args.message)
        return
    
    # Otherwise, run interactive session
    await client.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())
