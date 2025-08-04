"""
Configuration and Settings
"""
import os
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv

class Settings:
    """Application settings"""
    
    def __init__(self):
        # Load environment variables when creating settings instance
        load_dotenv()
        
        # Azure Foundry Configuration
        self.AZURE_FOUNDRY_ENDPOINT: str = os.getenv("AZURE_FOUNDRY_ENDPOINT", "")
        self.AZURE_FOUNDRY_API_KEY: str = os.getenv("AZURE_FOUNDRY_API_KEY", "")
        self.AZURE_FOUNDRY_DEPLOYMENT_NAME: str = os.getenv("AZURE_FOUNDRY_DEPLOYMENT_NAME", "gpt-4.1")
        self.AZURE_FOUNDRY_API_VERSION: str = os.getenv("AZURE_FOUNDRY_API_VERSION", "2025-01-01-preview")
        
        # Application Configuration
        self.APP_NAME: str = "Azure Foundry API"
        self.APP_VERSION: str = "1.0.0"
        self.API_V1_STR: str = "/api/v1"
        self.PORT: int = int(os.getenv("PORT", "8000"))
        self.HOST: str = os.getenv("HOST", "0.0.0.0")
        
        # Security
        self.API_KEY_HEADER: str = os.getenv("API_KEY_HEADER", "X-API-Key")
        self.JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
        
        # CORS
        self.ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://yourdomain.com").split(",")
        self.ALLOWED_METHODS: list = os.getenv("ALLOWED_METHODS", "GET,POST,PUT,DELETE").split(",")
        self.ALLOWED_HEADERS: list = os.getenv("ALLOWED_HEADERS", "*").split(",")
        
        # Rate Limiting
        self.RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hour
        
        # Logging
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Environment
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.DEBUG: bool = self.ENVIRONMENT.lower() == "development"
        
        # Azure Application Insights
        self.APPLICATIONINSIGHTS_CONNECTION_STRING: Optional[str] = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
        
        # Health Check
        self.HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
        
        # Request Timeout
        self.REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
        
        # Default Model Parameters
        self.DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "1000"))
        self.DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
        self.DEFAULT_TOP_P: float = float(os.getenv("DEFAULT_TOP_P", "1.0"))
    
    def validate_required_settings(self) -> list:
        """Validate that required settings are present"""
        errors = []
        
        if not self.AZURE_FOUNDRY_ENDPOINT:
            errors.append("AZURE_FOUNDRY_ENDPOINT is required")
        
        if not self.AZURE_FOUNDRY_API_KEY:
            errors.append("AZURE_FOUNDRY_API_KEY is required")
        
        if not self.AZURE_FOUNDRY_DEPLOYMENT_NAME:
            errors.append("AZURE_FOUNDRY_DEPLOYMENT_NAME is required")
        
        return errors

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
