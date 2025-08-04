# setup.ps1 - Initial setup script for Azure Foundry API

param(
    [string]$AzureFoundryEndpoint,
    [string]$AzureFoundryApiKey,
    [string]$AzureFoundryDeploymentName = "gpt-4.1"
)

Write-Host "🔧 Azure Foundry API - Initial Setup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists. Creating backup..." -ForegroundColor Yellow
    Copy-Item ".env" ".env.backup"
}

# Copy template to .env
if (Test-Path ".env.template") {
    Copy-Item ".env.template" ".env"
    Write-Host "✅ Created .env file from template" -ForegroundColor Green
} else {
    Write-Host "❌ .env.template not found!" -ForegroundColor Red
    exit 1
}

# If parameters provided, update .env file
if ($AzureFoundryEndpoint -and $AzureFoundryApiKey) {
    Write-Host "🔧 Updating .env with provided values..." -ForegroundColor Blue
    
    $envContent = Get-Content ".env"
    $envContent = $envContent -replace "AZURE_FOUNDRY_ENDPOINT=.*", "AZURE_FOUNDRY_ENDPOINT=$AzureFoundryEndpoint"
    $envContent = $envContent -replace "AZURE_FOUNDRY_API_KEY=.*", "AZURE_FOUNDRY_API_KEY=$AzureFoundryApiKey"
    $envContent = $envContent -replace "AZURE_FOUNDRY_DEPLOYMENT_NAME=.*", "AZURE_FOUNDRY_DEPLOYMENT_NAME=$AzureFoundryDeploymentName"
    
    $envContent | Set-Content ".env"
    Write-Host "✅ Updated .env with your Azure Foundry details" -ForegroundColor Green
} else {
    Write-Host "⚠️  Please edit .env file with your Azure Foundry details:" -ForegroundColor Yellow
    Write-Host "   - AZURE_FOUNDRY_ENDPOINT" -ForegroundColor Cyan
    Write-Host "   - AZURE_FOUNDRY_API_KEY" -ForegroundColor Cyan
    Write-Host "   - AZURE_FOUNDRY_DEPLOYMENT_NAME" -ForegroundColor Cyan
}

# Check if Python is available
Write-Host "`n🐍 Checking Python installation..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11 or later." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
}

# Check if Azure CLI is available
Write-Host "`n☁️  Checking Azure CLI..." -ForegroundColor Blue
try {
    $azVersion = az --version | Select-String "azure-cli" | Select-Object -First 1
    Write-Host "✅ Azure CLI found: $azVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found. Please install it." -ForegroundColor Red
    Write-Host "   Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
}

# Check if Azure Developer CLI is available
Write-Host "`n🚀 Checking Azure Developer CLI..." -ForegroundColor Blue
try {
    $azdVersion = azd version 2>&1
    Write-Host "✅ Azure Developer CLI found: $azdVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure Developer CLI not found. Please install it." -ForegroundColor Red
    Write-Host "   Download from: https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd" -ForegroundColor Yellow
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Green
Write-Host "=============" -ForegroundColor Green
Write-Host "1. Edit .env file with your Azure Foundry details (if not already done)" -ForegroundColor Cyan
Write-Host "2. Test locally: python run_dev.py" -ForegroundColor Cyan
Write-Host "3. Deploy to Azure: .\deploy.ps1 -EnvironmentName 'my-api' -Location 'eastus' -AzureFoundryEndpoint 'your-endpoint' -AzureFoundryApiKey 'your-key'" -ForegroundColor Cyan

Write-Host "`n🔗 Useful Commands:" -ForegroundColor Yellow
Write-Host "==================" -ForegroundColor Yellow
Write-Host "Local development:  python run_dev.py" -ForegroundColor White
Write-Host "Test API:          python test_client.py" -ForegroundColor White
Write-Host "Deploy to Azure:   .\deploy.ps1 [params]" -ForegroundColor White
Write-Host "View docs:         http://localhost:8000/docs (when running locally)" -ForegroundColor White

Write-Host "`n✨ Setup complete! You're ready to build with Azure Foundry!" -ForegroundColor Green
