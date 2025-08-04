# Azure Foundry API

A comprehensive FastAPI backend that integrates with Azure Foundry models, featuring API Management and Azure Front Door layers.

## Features

- 🚀 **FastAPI Backend** - High-performance async Python web API
- 🤖 **Azure Foundry Integration** - Direct integration with Azure Foundry models
- 🛡️ **API Management** - Azure APIM for API governance and security
- 🌐 **Azure Front Door** - Global CDN and routing layer
- 🐳 **Containerized** - Docker support with multi-stage builds
- 📊 **Monitoring** - Application Insights integration
- 🔐 **Security** - JWT authentication and CORS support
- 📖 **Auto Documentation** - OpenAPI/Swagger docs

## Architecture

```
[Client] → [Azure Front Door] → [API Management] → [Container App] → [Azure Foundry]
```

## Quick Start

### Prerequisites

- Python 3.11+
- Azure CLI
- Docker (optional)
- Azure subscription with Foundry access

### 1. Environment Setup

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Create .env file with your Azure Foundry details
@"
AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint.openai.azure.com
AZURE_FOUNDRY_API_KEY=your-api-key-here
AZURE_FOUNDRY_DEPLOYMENT_NAME=gpt-4.1
AZURE_FOUNDRY_API_VERSION=2025-01-01-preview
"@ | Out-File -FilePath .env -Encoding utf8
```

### 2. Local Development

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run development server
python run_dev.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test the API

The easiest way to test the API is using the interactive chat terminal:

```powershell
# Run interactive chat terminal (recommended)
python scripts/chat_terminal.py

# Or run comprehensive API tests
python scripts/test_api.py --key any-test-key-works

# Or test individual endpoints with curl
curl -X POST "http://localhost:8000/api/v1/chat/completions" -H "Authorization: Bearer any-test-key-works" -H "Content-Type: application/json" -d '{\"message\": \"Hello, how are you?\", \"model\": \"gpt-4.1\", \"max_tokens\": 100}'
```

**Authentication Note**: The current implementation accepts ANY Bearer token for testing purposes. You can use any string as your API key (e.g., "test-key", "my-api-key", "development-token").

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

### Chat & Completion

- `POST /api/v1/chat/completions` - Chat completion using Azure Foundry
- `POST /api/v1/generate` - Simple text generation
- `GET /api/v1/models` - List available models

### Example Request

```json
{
  "message": "Explain quantum computing in simple terms",
  "model": "gpt-4.1",
  "max_tokens": 500,
  "temperature": 0.7
}
```

### Example Response

```json
{
  "response": "Quantum computing is a revolutionary approach to computation...",
  "model": "gpt-4.1",
  "timestamp": "2024-01-15T10:30:00Z",
  "tokens_used": 156
}
```

## Azure Deployment

### Using Azure Developer CLI (azd)

```bash
# Initialize Azure resources
azd init

# Set environment variables
azd env set AZURE_FOUNDRY_ENDPOINT "https://your-endpoint.openai.azure.com"
azd env set AZURE_FOUNDRY_API_KEY "your-api-key"

# Deploy to Azure
azd up
```

### Manual Deployment

1. **Build and push container**:
   ```bash
   # Build image
   docker build -t foundry-api .
   
   # Tag and push to ACR
   docker tag foundry-api your-registry.azurecr.io/foundry-api:latest
   docker push your-registry.azurecr.io/foundry-api:latest
   ```

2. **Deploy infrastructure**:
   ```bash
   # Deploy Bicep templates
   az deployment sub create \
     --location eastus \
     --template-file infra/main.bicep \
     --parameters infra/main.parameters.json
   ```

## Infrastructure Components

### Azure Resources Created

- **Container App** - Hosts the FastAPI application
- **Container Registry** - Stores Docker images
- **API Management** - API gateway and management
- **Front Door** - Global CDN and routing
- **Log Analytics** - Centralized logging
- **Application Insights** - Application monitoring
- **Managed Identity** - Secure Azure resource access

### Architecture Diagram

```
Internet
    ↓
Azure Front Door (Global)
    ↓
API Management (Regional)
    ↓
Container App (Scalable)
    ↓
Azure Foundry (AI Models)
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_FOUNDRY_ENDPOINT` | Azure Foundry endpoint URL | Yes |
| `AZURE_FOUNDRY_API_KEY` | API key for Azure Foundry | Yes |
| `AZURE_FOUNDRY_DEPLOYMENT_NAME` | Model deployment name | Yes |
| `AZURE_FOUNDRY_API_VERSION` | API version | No |
| `PORT` | Application port | No |
| `LOG_LEVEL` | Logging level | No |

### Security Configuration

- **Authentication**: Bearer token authentication
- **CORS**: Configurable origins and methods
- **Rate Limiting**: Request throttling (future enhancement)
- **API Keys**: Managed through API Management

## Monitoring & Observability

### Application Insights

The application integrates with Azure Application Insights for:

- Request/response tracking
- Performance monitoring
- Error logging
- Custom metrics

### Health Checks

- **Liveness**: `/health` endpoint
- **Readiness**: Application startup checks
- **Dependencies**: Azure Foundry connectivity

### Logging

Structured logging with:
- Request IDs for tracing
- Performance metrics
- Error details
- Security events

## Development

### Project Structure

```
azure-foundry-api/
├── main.py                 # FastAPI application entry point
├── run_dev.py             # Development server launcher
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── azure.yaml           # Azure Developer CLI config
├── .env                 # Environment variables (local)
├── app/                 # Core application code
│   ├── __init__.py      # Package initialization
│   ├── config.py        # Configuration management
│   ├── models.py        # Pydantic models
│   └── dependencies.py  # FastAPI dependencies
├── scripts/             # Utility scripts
│   ├── README.md        # Scripts documentation
│   ├── chat_terminal.py # Interactive API testing client
│   ├── test_api.py      # Comprehensive API tests
│   ├── test_azure_client.py # Azure client connection tests
│   └── test_client.py   # Legacy test client
├── tests/               # Test framework
│   └── __init__.py      # Test package initialization
├── docs/                # Documentation
│   ├── DEPLOYMENT.md    # Deployment guide
│   ├── GITHUB_SETUP.md  # GitHub integration guide
│   ├── QUICK_START.md   # Quick start guide
│   └── RESTRUCTURE_SUMMARY.md # Project restructuring notes
└── infra/               # Infrastructure as Code
    ├── main.bicep       # Main Bicep template
    ├── resources.bicep  # Resource definitions
    └── main.parameters.json # Parameters
```

### Testing

```bash
# Run comprehensive API tests
python scripts/test_api.py

# Run interactive chat terminal (recommended for testing)
python scripts/chat_terminal.py

# Test Azure client connection
python scripts/test_azure_client.py

# Test specific endpoint with legacy client
python scripts/test_client.py --key any-test-key-works

# Test deployed API
python scripts/test_api.py --url https://your-frontdoor.azurefd.net
```

### Interactive Testing

The project includes an interactive chat terminal for easy API testing:

```bash
# Start the interactive terminal client
python scripts/chat_terminal.py
```

**Available Commands:**
- `/help` - Show available commands
- `/health` - Check API health status
- `/models` - List available models
- `/mode` - Switch between chat and generate modes
- `/history` - Show conversation history
- `/clear` - Clear conversation history
- `/quit` - Exit the terminal

**Testing Modes:**
- **Chat Mode**: Multi-turn conversations with context history
- **Generate Mode**: Single-turn text generation requests

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Azure Foundry Authentication**:
   - Verify API key and endpoint
   - Check deployment name
   - Ensure proper permissions

2. **Container App Issues**:
   - Check container logs
   - Verify environment variables
   - Review resource limits

3. **API Management**:
   - Verify backend URL
   - Check subscription keys
   - Review CORS settings

### Getting Help

- Check Azure portal for resource status
- Review Application Insights logs
- Use health check endpoints
- Contact support team

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v1.0.0
- Initial release
- Azure Foundry integration
- API Management setup
- Front Door configuration
- Container App deployment
