# Local Development Setup Guide

## Prerequisites
- Python 3.11 or higher
- Git
- PowerShell (Windows)

## Step-by-Step Setup

### 1. Clone and Navigate to Project
```powershell
cd "c:\Users\albabaza\Desktop\New role\shyon-playground\ai_connect_playground\azure-foundry-api\ai-playground"
```

### 2. Create Python Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**Troubleshooting**: If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies
```powershell
# Make sure venv is activated (you should see "(venv)" in your prompt)
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```powershell
@"
AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint.openai.azure.com
AZURE_FOUNDRY_API_KEY=your-api-key-here
AZURE_FOUNDRY_DEPLOYMENT_NAME=gpt-4.1
AZURE_FOUNDRY_API_VERSION=2025-01-01-preview
"@ | Out-File -FilePath .env -Encoding utf8
```

**Replace the placeholder values with your actual Azure Foundry credentials.**

### 5. Start the Development Server
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Start the server
python run_dev.py
```

The server will start at `http://localhost:8000`

### 6. Test the API

#### Option 1: Use the Test Client
```powershell
# In a new PowerShell window, activate venv
.\venv\Scripts\Activate.ps1

# Run tests (use any string as the API key)
python test_client.py --url http://localhost:8000 --key my-test-key
```

#### Option 2: Use the Swagger UI
Open your browser and go to: `http://localhost:8000/docs`

#### Option 3: Use curl
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST "http://localhost:8000/api/v1/chat/completions" -H "Authorization: Bearer test-key" -H "Content-Type: application/json" -d '{\"message\": \"Hello!\", \"model\": \"gpt-4.1\", \"max_tokens\": 50}'
```

## API Key Information

**For Local Testing**: The current authentication implementation accepts ANY Bearer token. You can use any string as your API key:
- `test-key`
- `development-token` 
- `my-api-key`
- `any-string-works`

The authentication only checks that a Bearer token is present, not its specific value.

## Common Issues

### Virtual Environment Not Activating
```powershell
# Check if venv folder exists
ls venv

# Try activating with full path
C:\path\to\your\project\venv\Scripts\Activate.ps1
```

### Missing Azure Foundry Credentials
If you see configuration errors when starting the server:
1. Check that your `.env` file exists and has the correct values
2. Make sure you have valid Azure Foundry endpoint and API key
3. Verify your deployment name matches your Azure setup

### Port Already in Use
If port 8000 is busy:
```powershell
# Use a different port
python -c "from main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

## Deactivating Virtual Environment
When you're done:
```powershell
deactivate
```

## Next Steps
- Visit `http://localhost:8000/docs` for interactive API documentation
- Run the test suite to verify everything works
- Check the logs for any configuration issues
- Review the API endpoints and test with your own data
