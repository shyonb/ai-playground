# 🚀 GitHub Repository Setup Guide

## Option 1: Create Repository on GitHub (Recommended)

### Step 1: Create Repository on GitHub
1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon in top right → "New repository"
3. Repository name: `ai-playground`
4. Description: `Azure Foundry API with FastAPI, API Management, and Front Door`
5. Keep it **Public** (or Private if you prefer)
6. **Don't** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

### Step 2: Get Your Repository URL
After creating, GitHub will show you the repository URL. It will look like:
```
https://github.com/YOUR_USERNAME/ai-playground.git
```

### Step 3: Update Remote and Push
```powershell
# Remove the current remote (if any)
git remote remove origin

# Add your correct repository URL
git remote add origin https://github.com/YOUR_USERNAME/ai-playground.git

# Push to GitHub
git push -u origin main
```

## Option 2: Use GitHub CLI (If you have it installed)

```powershell
# Create repository directly from command line
gh repo create ai-playground --public --description "Azure Foundry API with FastAPI, API Management, and Front Door"

# Push the code
git push -u origin main
```

## Option 3: Manual Repository Setup

If you already created the repository, just update the remote:

```powershell
# Check current remote
git remote -v

# Update the remote URL with YOUR username
git remote set-url origin https://github.com/YOUR_USERNAME/ai-playground.git

# Push to GitHub
git push -u origin main
```

## 📝 What's Already Prepared

Your repository is ready with:
- ✅ All files committed locally
- ✅ Branch renamed to `main`
- ✅ Comprehensive `.gitignore`
- ✅ Professional README.md
- ✅ Complete documentation

## 🎯 After Pushing to GitHub

Your repository will contain:

```
ai-playground/
├── 📚 Documentation
│   ├── README.md           # Main project documentation
│   ├── QUICK_START.md      # 3-step setup guide
│   └── DEPLOYMENT.md       # Detailed deployment instructions
├── 🐍 Python Backend
│   ├── main.py             # FastAPI application
│   ├── models.py           # Pydantic models
│   ├── config.py           # Configuration
│   ├── azure_foundry_client.py # Azure integration
│   └── test_client.py      # Testing suite
├── 🏗️ Infrastructure
│   └── infra/
│       ├── main.bicep      # Main Bicep template
│       ├── resources.bicep # Resource definitions
│       └── main.parameters.json # Parameters
├── 🐳 Deployment
│   ├── Dockerfile          # Container definition
│   ├── azure.yaml         # Azure Developer CLI
│   ├── deploy.ps1         # Deployment script
│   └── requirements.txt    # Dependencies
└── 🔧 Configuration
    ├── .env.template      # Environment template
    ├── .gitignore         # Git ignore rules
    └── setup.ps1          # Setup script
```

## 🌟 Professional Repository Features

Your repo will showcase:
- 🏗️ **Enterprise Architecture**: Front Door → API Management → Container Apps
- 🐍 **Modern Python**: FastAPI with async/await patterns
- ☁️ **Infrastructure as Code**: Complete Bicep templates
- 🐳 **Containerization**: Production-ready Dockerfile
- 📊 **Monitoring**: Application Insights integration
- 🔐 **Security**: Authentication, CORS, managed identities
- 📖 **Documentation**: Comprehensive guides and API docs
- 🧪 **Testing**: Complete test suite included
- 🚀 **One-Click Deploy**: PowerShell and azd deployment

## 🎯 Next Steps After GitHub Push

1. **Enable GitHub Actions** (optional):
   - Set up CI/CD pipeline
   - Auto-deploy on commits

2. **Add Repository Secrets** (for CI/CD):
   - `AZURE_FOUNDRY_ENDPOINT`
   - `AZURE_FOUNDRY_API_KEY`
   - Azure service principal credentials

3. **Create Issues/Projects**:
   - Track enhancements
   - Plan new features

4. **Share and Collaborate**:
   - Invite team members
   - Set up branch protection rules

## 🔧 Troubleshooting

### If push fails with authentication:
```powershell
# Configure Git credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Use personal access token for HTTPS
# Go to GitHub Settings → Developer settings → Personal access tokens
```

### If repository already exists with content:
```powershell
# Pull first to merge
git pull origin main --allow-unrelated-histories

# Then push
git push -u origin main
```

## 📞 Ready to Push?

1. Create your repository on GitHub
2. Get the correct URL
3. Update the remote
4. Push your code!

Your Azure Foundry API will be live on GitHub! 🎉
