"""
Terminal Chat Client for testing the Azure Foundry API
"""
import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Constants
API_BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{API_BASE_URL}/api/v1/chat/completions"
GENERATE_ENDPOINT = f"{API_BASE_URL}/api/v1/generate"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
MODELS_ENDPOINT = f"{API_BASE_URL}/api/v1/models"

# Token for authentication (any string works for testing)
AUTH_TOKEN = "test-token-12345"

class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class ChatClient:
    def __init__(self):
        self.session = None
        self.chat_history = []
        self.mode = "chat"  # or "generate"
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def print_colored(self, text: str, color: str = Colors.END):
        """Print colored text to terminal"""
        print(f"{color}{text}{Colors.END}")
    
    def print_header(self):
        """Print the application header"""
        self.print_colored("=" * 60, Colors.BLUE)
        self.print_colored("🤖 Azure Foundry API Terminal Chat Client", Colors.BOLD)
        self.print_colored("=" * 60, Colors.BLUE)
        self.print_colored("Commands:", Colors.YELLOW)
        self.print_colored("  /help    - Show this help", Colors.GREEN)
        self.print_colored("  /health  - Check API health", Colors.GREEN)
        self.print_colored("  /models  - List available models", Colors.GREEN)
        self.print_colored("  /mode    - Switch between 'chat' and 'generate' modes", Colors.GREEN)
        self.print_colored("  /history - Show chat history", Colors.GREEN)
        self.print_colored("  /clear   - Clear chat history", Colors.GREEN)
        self.print_colored("  /quit    - Exit the client", Colors.GREEN)
        self.print_colored("=" * 60, Colors.BLUE)
        self.print_colored(f"Current mode: {self.mode}", Colors.YELLOW)
        print()
    
    async def check_health(self):
        """Check API health"""
        try:
            async with self.session.get(HEALTH_ENDPOINT) as response:
                if response.status == 200:
                    data = await response.json()
                    self.print_colored("✅ API Health Check:", Colors.GREEN) 
                    self.print_colored(f"   Status: {data.get('status', 'unknown')}", Colors.GREEN)
                    self.print_colored(f"   Message: {data.get('message', 'N/A')}", Colors.GREEN)
                    if data.get('azure_endpoint'):
                        self.print_colored(f"   Azure Endpoint: {data['azure_endpoint']}", Colors.GREEN)
                else:
                    self.print_colored(f"❌ Health check failed: {response.status}", Colors.RED)
        except Exception as e:
            self.print_colored(f"❌ Health check error: {str(e)}", Colors.RED)
    
    async def list_models(self):
        """List available models"""
        try:
            headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
            async with self.session.get(MODELS_ENDPOINT, headers=headers) as response:
                if response.status == 200:
                    models = await response.json()
                    self.print_colored("📋 Available Models:", Colors.GREEN)
                    for model in models:
                        self.print_colored(f"   • {model.get('id', 'unknown')} ({model.get('object', 'model')})", Colors.GREEN)
                else:
                    self.print_colored(f"❌ Failed to list models: {response.status}", Colors.RED)
        except Exception as e:
            self.print_colored(f"❌ Error listing models: {str(e)}", Colors.RED)
    
    async def send_chat_message(self, user_message: str) -> Dict[Any, Any]:
        """Send a chat message to the API"""
        # Add user message to history
        self.chat_history.append({"role": "user", "content": user_message})
        
        # Prepare request payload
        payload = {
            "messages": self.chat_history,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.post(CHAT_ENDPOINT, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract assistant response
                    assistant_message = data['choices'][0]['message']['content']
                    
                    # Add assistant response to history
                    self.chat_history.append({"role": "assistant", "content": assistant_message})
                    
                    return {
                        "success": True,
                        "message": assistant_message,
                        "model": data.get('model', 'unknown'),
                        "usage": data.get('usage', {})
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}: {error_text}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    async def send_generate_request(self, prompt: str) -> Dict[Any, Any]:
        """Send a text generation request to the API"""
        payload = {
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.post(GENERATE_ENDPOINT, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "generated_text": data.get('generated_text', ''),
                        "model": data.get('model', 'unknown'),
                        "tokens_used": data.get('tokens_used', 0)
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}: {error_text}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def show_history(self):
        """Show chat history"""
        if not self.chat_history:
            self.print_colored("📝 No chat history yet.", Colors.YELLOW)
            return
        
        self.print_colored("📝 Chat History:", Colors.BLUE)
        for i, message in enumerate(self.chat_history, 1):
            role_color = Colors.GREEN if message['role'] == 'user' else Colors.BLUE
            self.print_colored(f"{i}. [{message['role'].upper()}]: {message['content'][:100]}{'...' if len(message['content']) > 100 else ''}", role_color)
        print()
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history.clear()
        self.print_colored("🗑️ Chat history cleared.", Colors.YELLOW)
    
    def switch_mode(self):
        """Switch between chat and generate modes"""
        self.mode = "generate" if self.mode == "chat" else "chat"
        self.print_colored(f"🔄 Switched to {self.mode} mode", Colors.YELLOW)
        if self.mode == "generate":
            self.print_colored("   Generate mode: Single-turn text generation", Colors.YELLOW)
        else:
            self.print_colored("   Chat mode: Multi-turn conversation with history", Colors.YELLOW)
    
    async def run(self):
        """Main chat loop"""
        self.print_header()
        await self.check_health()
        print()
        
        while True:
            try:
                # Get user input
                mode_indicator = "🤖" if self.mode == "chat" else "📝"
                prompt = f"{mode_indicator} [{self.mode.upper()}] You: "
                user_input = input(Colors.GREEN + prompt + Colors.END).strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    command = user_input[1:].lower()
                    
                    if command == 'quit' or command == 'exit':
                        self.print_colored("👋 Goodbye!", Colors.YELLOW)
                        break
                    elif command == 'help':
                        self.print_header()
                    elif command == 'health':
                        await self.check_health()
                    elif command == 'models':
                        await self.list_models()
                    elif command == 'history':
                        self.show_history()
                    elif command == 'clear':
                        self.clear_history()
                    elif command == 'mode':
                        self.switch_mode()
                    else:
                        self.print_colored(f"❌ Unknown command: {command}. Type /help for available commands.", Colors.RED)
                    continue
                
                # Send request based on mode
                self.print_colored("🔄 Sending request...", Colors.YELLOW)
                
                if self.mode == "chat":
                    result = await self.send_chat_message(user_input)
                    
                    if result["success"]:
                        self.print_colored("🤖 Assistant:", Colors.BLUE)
                        print(result["message"])
                        
                        # Show usage info
                        usage = result.get("usage", {})
                        if usage:
                            self.print_colored(f"   [Model: {result.get('model', 'unknown')}, Tokens: {usage.get('total_tokens', 'unknown')}]", Colors.YELLOW)
                    else:
                        self.print_colored(f"❌ Error: {result['error']}", Colors.RED)
                
                else:  # generate mode
                    result = await self.send_generate_request(user_input)
                    
                    if result["success"]:
                        self.print_colored("📝 Generated Text:", Colors.BLUE)
                        print(result["generated_text"])
                        
                        # Show usage info
                        self.print_colored(f"   [Model: {result.get('model', 'unknown')}, Tokens: {result.get('tokens_used', 'unknown')}]", Colors.YELLOW)
                    else:
                        self.print_colored(f"❌ Error: {result['error']}", Colors.RED)
                
                print()  # Add spacing
                
            except KeyboardInterrupt:
                self.print_colored("\n👋 Goodbye!", Colors.YELLOW)
                break
            except Exception as e:
                self.print_colored(f"❌ Unexpected error: {str(e)}", Colors.RED)

async def main():
    """Main entry point"""
    async with ChatClient() as client:
        await client.run()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
