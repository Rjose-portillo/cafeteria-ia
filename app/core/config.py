"""
Configuration module using pydantic-settings.
Loads environment variables from .env file and provides type-safe settings.
"""
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic-settings for validation and type coercion.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Keys
    GEMINI_API_KEY: str
    
    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str
    
    # AI Model Configuration
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # Environment
    ENV: Literal["local", "prod"] = "local"
    
    # Application Settings
    APP_NAME: str = "Justicia y Café"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    # Business Rules
    CANCEL_TIME_LIMIT_MINUTES: int = 5
    DEFAULT_PREP_BUFFER_MINUTES: int = 5
    DEFAULT_COST_PERCENTAGE: float = 0.30
    
    # Chat Settings
    CHAT_HISTORY_LIMIT: int = 10
    MESSAGE_BUFFER_SECONDS: float = 2.0


@lru_cache()
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Global settings instance for easy import
settings = get_settings()