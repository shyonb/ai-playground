# Scripts Directory

This directory contains utility scripts for testing and interacting with the Azure Foundry API project.

## Available Scripts

### 🤖 `chat_terminal.py` - Interactive Chat Terminal
Interactive async terminal client for testing the API with a user-friendly interface.

**Features:**
- Multi-turn chat conversations with history
- Single-turn text generation mode
- Real-time API health monitoring
- Model listing and selection
- Colored terminal output
- Command system for easy navigation

**Usage:**
```bash
python scripts/chat_terminal.py
```

**Commands:**
- `/help` - Show available commands
- `/health` - Check API health status
- `/models` - List available models
- `/mode` - Switch between chat and generate modes
- `/history` - Show conversation history
- `/clear` - Clear conversation history
- `/quit` - Exit the terminal

### 🧪 `test_api.py` - Comprehensive API Tests
Comprehensive test suite for all API endpoints with detailed reporting.

**Features:**
- Tests all API endpoints
- Detailed success/failure reporting
- Performance timing
- Error handling validation
- Configurable test parameters

**Usage:**
```bash
# Test local API
python scripts/test_api.py

# Test deployed API
python scripts/test_api.py --url https://your-api-url.com
```

### 🔌 `test_azure_client.py` - Azure Connection Tests
Test script specifically for validating Azure OpenAI client connection and configuration.

**Features:**
- Direct Azure OpenAI client testing
- Configuration validation
- Connection troubleshooting
- Model availability checking

**Usage:**
```bash
python scripts/test_azure_client.py
```

### 📜 `test_client.py` - Legacy Test Client
Original test client maintained for compatibility and simple testing scenarios.

**Features:**
- Basic API endpoint testing
- Simple HTTP request/response validation
- Command-line parameter support

**Usage:**
```bash
python scripts/test_client.py --key any-test-key-works
```

## Quick Testing Workflow

1. **Start the API server:**
   ```bash
   python run_dev.py
   ```

2. **Test with interactive terminal (recommended):**
   ```bash
   python scripts/chat_terminal.py
   ```

3. **Run comprehensive tests:**
   ```bash
   python scripts/test_api.py
   ```

4. **Validate Azure connection:**
   ```bash
   python scripts/test_azure_client.py
   ```

## Dependencies

All scripts use the project's main dependencies from `requirements.txt`. The chat terminal additionally uses:
- `aiohttp` - For async HTTP requests
- `asyncio` - For async operations

## Environment Setup

Ensure your virtual environment is activated and dependencies are installed:

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies (if not already done)
pip install -r requirements.txt
```

## Authentication

All scripts support the development authentication system where any Bearer token works for local testing. For production testing, use valid API keys.
