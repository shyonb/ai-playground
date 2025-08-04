# Deployment Scripts

## PowerShell Deployment Script

```powershell
# deploy.ps1 - PowerShell deployment script for Azure Foundry API

param(
    [Parameter(Mandatory=$true)]
    [string]$EnvironmentName,
    
    [Parameter(Mandatory=$true)]
    [string]$Location,
    
    [Parameter(Mandatory=$true)]
    [string]$AzureFoundryEndpoint,
    
    [Parameter(Mandatory=$true)]
    [string]$AzureFoundryApiKey,
    
    [string]$AzureFoundryDeploymentName = "gpt-4.1"
)

Write-Host "🚀 Starting Azure Foundry API Deployment" -ForegroundColor Green
Write-Host "Environment: $EnvironmentName" -ForegroundColor Yellow
Write-Host "Location: $Location" -ForegroundColor Yellow

# Check if user is logged in to Azure
$context = az account show --query "name" -o tsv 2>$null
if (!$context) {
    Write-Host "❌ Not logged in to Azure. Please run 'az login'" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Logged in to Azure as: $context" -ForegroundColor Green

# Set environment variables for azd
$env:AZURE_ENV_NAME = $EnvironmentName
$env:AZURE_LOCATION = $Location
$env:AZURE_FOUNDRY_ENDPOINT = $AzureFoundryEndpoint
$env:AZURE_FOUNDRY_API_KEY = $AzureFoundryApiKey
$env:AZURE_FOUNDRY_DEPLOYMENT_NAME = $AzureFoundryDeploymentName

Write-Host "🔧 Setting up azd environment..." -ForegroundColor Blue

# Initialize azd environment
azd env new $EnvironmentName --location $Location

# Set environment variables
azd env set AZURE_FOUNDRY_ENDPOINT $AzureFoundryEndpoint
azd env set AZURE_FOUNDRY_API_KEY $AzureFoundryApiKey
azd env set AZURE_FOUNDRY_DEPLOYMENT_NAME $AzureFoundryDeploymentName

Write-Host "🏗️ Deploying infrastructure and application..." -ForegroundColor Blue

# Deploy to Azure
azd up --no-prompt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
    
    # Get outputs
    $outputs = azd env get-values
    Write-Host "📋 Deployment Outputs:" -ForegroundColor Yellow
    $outputs | ForEach-Object { Write-Host "  $_" -ForegroundColor Cyan }
    
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}
```

## Bash Deployment Script

```bash
#!/bin/bash
# deploy.sh - Bash deployment script for Azure Foundry API

set -e

# Function to print colored output
print_status() {
    echo -e "\033[1;32m$1\033[0m"
}

print_info() {
    echo -e "\033[1;34m$1\033[0m"
}

print_warning() {
    echo -e "\033[1;33m$1\033[0m"
}

print_error() {
    echo -e "\033[1;31m$1\033[0m"
}

# Check parameters
if [ $# -lt 4 ]; then
    print_error "Usage: $0 <environment-name> <location> <foundry-endpoint> <foundry-api-key> [deployment-name]"
    exit 1
fi

ENVIRONMENT_NAME=$1
LOCATION=$2
AZURE_FOUNDRY_ENDPOINT=$3
AZURE_FOUNDRY_API_KEY=$4
AZURE_FOUNDRY_DEPLOYMENT_NAME=${5:-"gpt-4.1"}

print_status "🚀 Starting Azure Foundry API Deployment"
print_warning "Environment: $ENVIRONMENT_NAME"
print_warning "Location: $LOCATION"

# Check if user is logged in to Azure
if ! az account show &> /dev/null; then
    print_error "❌ Not logged in to Azure. Please run 'az login'"
    exit 1
fi

ACCOUNT_NAME=$(az account show --query "name" -o tsv)
print_status "✅ Logged in to Azure as: $ACCOUNT_NAME"

# Set environment variables
export AZURE_ENV_NAME=$ENVIRONMENT_NAME
export AZURE_LOCATION=$LOCATION
export AZURE_FOUNDRY_ENDPOINT=$AZURE_FOUNDRY_ENDPOINT
export AZURE_FOUNDRY_API_KEY=$AZURE_FOUNDRY_API_KEY
export AZURE_FOUNDRY_DEPLOYMENT_NAME=$AZURE_FOUNDRY_DEPLOYMENT_NAME

print_info "🔧 Setting up azd environment..."

# Initialize azd environment
azd env new $ENVIRONMENT_NAME --location $LOCATION

# Set environment variables
azd env set AZURE_FOUNDRY_ENDPOINT $AZURE_FOUNDRY_ENDPOINT
azd env set AZURE_FOUNDRY_API_KEY $AZURE_FOUNDRY_API_KEY
azd env set AZURE_FOUNDRY_DEPLOYMENT_NAME $AZURE_FOUNDRY_DEPLOYMENT_NAME

print_info "🏗️ Deploying infrastructure and application..."

# Deploy to Azure
azd up --no-prompt

if [ $? -eq 0 ]; then
    print_status "✅ Deployment completed successfully!"
    
    # Get outputs
    print_warning "📋 Deployment Outputs:"
    azd env get-values | while read line; do
        echo -e "\033[1;36m  $line\033[0m"
    done
    
else
    print_error "❌ Deployment failed!"
    exit 1
fi
```

## Manual Deployment Steps

### 1. Prerequisites
- Azure CLI installed and logged in
- Azure Developer CLI (azd) installed
- Docker installed (for local testing)
- Access to Azure Foundry service

### 2. Quick Deploy

```bash
# Clone or create the project
cd azure-foundry-api

# Copy environment template
cp .env.template .env

# Edit .env with your values
# AZURE_FOUNDRY_ENDPOINT=https://your-foundry-endpoint.openai.azure.com
# AZURE_FOUNDRY_API_KEY=your-api-key-here

# Deploy using azd
azd up
```

### 3. Step-by-Step Deployment

```bash
# 1. Login to Azure
az login

# 2. Initialize azd environment
azd env new my-foundry-api --location eastus

# 3. Set required environment variables
azd env set AZURE_FOUNDRY_ENDPOINT "https://your-foundry-endpoint.openai.azure.com"
azd env set AZURE_FOUNDRY_API_KEY "your-api-key-here"
azd env set AZURE_FOUNDRY_DEPLOYMENT_NAME "gpt-4.1"

# 4. Deploy infrastructure and application
azd up

# 5. Get deployment outputs
azd env get-values
```

### 4. Verify Deployment

```bash
# Test health endpoint
curl https://your-frontdoor-endpoint.azurefd.net/health

# Test API endpoint
curl -X POST "https://your-frontdoor-endpoint.azurefd.net/api/v1/chat/completions" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, world!",
    "model": "gpt-4.1",
    "max_tokens": 100
  }'
```

### 5. Troubleshooting

```bash
# Check deployment status
azd env show

# View container app logs
az containerapp logs show --name <container-app-name> --resource-group <resource-group-name>

# Check API Management
az apim api show --resource-group <resource-group-name> --service-name <apim-name> --api-id foundry-api

# Test Front Door
az afd endpoint show --resource-group <resource-group-name> --profile-name <frontdoor-name> --endpoint-name foundry-api-endpoint
```

### 6. Cleanup

```bash
# Delete all resources
azd down --force --purge
```
