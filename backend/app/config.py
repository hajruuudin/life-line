"""Configuration settings for the LifeLine backend application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str
    
    # Google OAuth
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    # N8N
    n8n_url: str
    n8n_api_key: str
    n8n_webhook_auth_key: str
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # Server
    backend_port: int = 8080
    frontend_url: str = "http://localhost:4200"
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = 'ignore'


# Global settings instance
settings = Settings()

