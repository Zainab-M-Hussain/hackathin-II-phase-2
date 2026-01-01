"""
Application configuration and settings.

Loads from environment variables with sensible defaults.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Example .env:
        DATABASE_URL=postgresql+psycopg2://user:password@localhost/todo_db
        SERVER_HOST=0.0.0.0
        SERVER_PORT=8000
        ENVIRONMENT=development
        DEBUG=true
    """

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/todo_db"
    )
    DATABASE_POOL_SIZE: int = 20
    DATABASE_POOL_RECYCLE: int = 3600
    DATABASE_ECHO: bool = False

    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # API
    API_TITLE: str = "Phase II Todo API"
    API_DESCRIPTION: str = "REST API for todo application with persistent storage"
    API_VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:8000",  # FastAPI dev server (Swagger UI)
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    CORS_HEADERS: list[str] = ["*"]

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "json"  # json or text

    # Rate Limiting (Phase III preparation)
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    @validator("DATABASE_URL")
    def database_url_required(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v

    @validator("SERVER_PORT")
    def port_valid(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("SERVER_PORT must be between 1 and 65535")
        return v

    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
