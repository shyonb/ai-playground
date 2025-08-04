#!/usr/bin/env python3
"""
Development server script
"""
import uvicorn
import os
from dotenv import load_dotenv
from config import get_settings

def main():
    """Run the development server"""
    # Load environment variables from .env file
    load_dotenv()
    
    settings = get_settings()
    
    # Validate required settings
    errors = settings.validate_required_settings()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease check your .env file or environment variables.")
        return
    
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Azure Foundry Endpoint: {settings.AZURE_FOUNDRY_ENDPOINT}")
    print(f"Azure Foundry Deployment: {settings.AZURE_FOUNDRY_DEPLOYMENT_NAME}")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )

if __name__ == "__main__":
    main()
