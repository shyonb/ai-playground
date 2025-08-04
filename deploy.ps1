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
    
    [string]$AzureFoundryDeploymentName = "gpt-4"
)

Write-Host "🚀 Starting Azure Foundry API Deployment" -ForegroundColor Green
Write-Host "Environment: $EnvironmentName" -ForegroundColor Yellow
Write-Host "Location: $Location" -ForegroundColor Yellow

# Check if user is logged in to Azure
try {
    $context = az account show --query "name" -o tsv 2>$null
    if (!$context) {
        throw "Not logged in"
    }
} catch {
    Write-Host "❌ Not logged in to Azure. Please run 'az login'" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Logged in to Azure as: $context" -ForegroundColor Green

# Check if azd is installed
try {
    azd version | Out-Null
} catch {
    Write-Host "❌ Azure Developer CLI (azd) not found. Please install it first." -ForegroundColor Red
    Write-Host "Install from: https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd" -ForegroundColor Yellow
    exit 1
}

# Set environment variables for azd
$env:AZURE_ENV_NAME = $EnvironmentName
$env:AZURE_LOCATION = $Location
$env:AZURE_FOUNDRY_ENDPOINT = $AzureFoundryEndpoint
$env:AZURE_FOUNDRY_API_KEY = $AzureFoundryApiKey
$env:AZURE_FOUNDRY_DEPLOYMENT_NAME = $AzureFoundryDeploymentName

Write-Host "🔧 Setting up azd environment..." -ForegroundColor Blue

# Initialize azd environment if it doesn't exist
try {
    azd env new $EnvironmentName --location $Location 2>$null
} catch {
    Write-Host "Environment may already exist, continuing..." -ForegroundColor Yellow
}

# Set environment variables
azd env set AZURE_FOUNDRY_ENDPOINT $AzureFoundryEndpoint
azd env set AZURE_FOUNDRY_API_KEY $AzureFoundryApiKey
azd env set AZURE_FOUNDRY_DEPLOYMENT_NAME $AzureFoundryDeploymentName

Write-Host "🏗️ Deploying infrastructure and application..." -ForegroundColor Blue

# Deploy to Azure
azd up --no-prompt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
    
    Write-Host "📋 Deployment Outputs:" -ForegroundColor Yellow
    azd env get-values | ForEach-Object { 
        if ($_ -match "=") {
            Write-Host "  $_" -ForegroundColor Cyan 
        }
    }
    
    Write-Host "`n🌐 Access your API:" -ForegroundColor Green
    Write-Host "  - Documentation: Check the FRONT_DOOR_ENDPOINT_URL/docs" -ForegroundColor Cyan
    Write-Host "  - Health Check: Check the API_BASE_URL/health" -ForegroundColor Cyan
    
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Check the azd logs for more details." -ForegroundColor Yellow
    exit 1
}
