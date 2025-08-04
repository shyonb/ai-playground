"""
Configuration and Settings
"""
import os
from functools import lru_cache
from typing import Optional

class Settings:
    """Application settings"""
    
    # Azure Foundry Configuration
    AZURE_FOUNDRY_ENDPOINT: str = os.getenv("AZURE_FOUNDRY_ENDPOINT", "")
    AZURE_FOUNDRY_API_KEY: str = os.getenv("AZURE_FOUNDRY_API_KEY", "")
    AZURE_FOUNDRY_DEPLOYMENT_NAME: str = os.getenv("AZURE_FOUNDRY_DEPLOYMENT_NAME", "gpt-4")
    AZURE_FOUNDRY_API_VERSION: str = os.getenv("AZURE_FOUNDRY_API_VERSION", "2024-02-15-preview")
    
    # Application Configuration
    APP_NAME: str = "Azure Foundry API"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Security
    API_KEY_HEADER: str = os.getenv("API_KEY_HEADER", "X-API-Key")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://yourdomain.com").split(",")
    ALLOWED_METHODS: list = os.getenv("ALLOWED_METHODS", "GET,POST,PUT,DELETE").split(",")
    ALLOWED_HEADERS: list = os.getenv("ALLOWED_HEADERS", "*").split(",")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hour
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT.lower() == "development"
    
    # Azure Application Insights
    APPLICATIONINSIGHTS_CONNECTION_STRING: Optional[str] = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    
    # Health Check
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
    
    # Request Timeout
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    # Default Model Parameters
    DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "1000"))
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    DEFAULT_TOP_P: float = float(os.getenv("DEFAULT_TOP_P", "1.0"))
    
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
