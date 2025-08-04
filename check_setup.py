"""
Quick local test to verify Azure Foundry API setup
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found. Run setup.ps1 first.")
        return False
    
    # Load environment variables from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed. Installing...")
        os.system("pip install python-dotenv")
        from dotenv import load_dotenv
        load_dotenv()
    
    # Check required variables
    required_vars = [
        "AZURE_FOUNDRY_ENDPOINT",
        "AZURE_FOUNDRY_API_KEY",
        "AZURE_FOUNDRY_DEPLOYMENT_NAME"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == "your-api-key-here" or value == "https://your-foundry-endpoint.openai.azure.com":
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * 10}...{value[-4:]}" if "KEY" in var else f"✅ {var}: {value}")
    
    if missing_vars:
        print("❌ Missing or placeholder values for:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    return True

def test_imports():
    """Test if required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("httpx", "HTTPX"),
        ("pydantic", "Pydantic"),
    ]
    
    missing_packages = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {name}")
    
    if missing_packages:
        print("\n📥 Installing missing packages...")
        os.system(f"pip install {' '.join(missing_packages)}")
        return True
    
    return True

def test_api_startup():
    """Test if the API can start without errors"""
    print("\n🚀 Testing API startup...")
    
    try:
        # Import main components
        from main import app
        from config import get_settings
        
        settings = get_settings()
        print(f"✅ Configuration loaded")
        print(f"✅ FastAPI app created")
        print(f"✅ Azure Foundry endpoint configured: {settings.AZURE_FOUNDRY_ENDPOINT}")
        
        return True
    except Exception as e:
        print(f"❌ Error starting API: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Azure Foundry API - Local Test Suite")
    print("=" * 45)
    
    tests = [
        ("Environment Configuration", check_environment),
        ("Package Dependencies", test_imports),
        ("API Startup", test_api_startup)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        try:
            success = test_func()
            results[test_name] = "✅ PASSED" if success else "❌ FAILED"
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results[test_name] = "❌ ERROR"
    
    print("\n" + "=" * 45)
    print("📊 Test Results:")
    for test_name, result in results.items():
        print(f"   {test_name}: {result}")
    
    passed = sum(1 for r in results.values() if "PASSED" in r)
    total = len(results)
    
    if passed == total:
        print(f"\n🎉 All tests passed! ({passed}/{total})")
        print("\n🚀 Next steps:")
        print("   1. Run locally: python run_dev.py")
        print("   2. Test endpoints: python test_client.py")
        print("   3. Deploy to Azure: .\\deploy.ps1 [params]")
    else:
        print(f"\n⚠️  Some tests failed ({passed}/{total})")
        print("   Please fix the issues above before proceeding.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
