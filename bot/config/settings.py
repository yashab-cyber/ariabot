"""
Aria Configuration Module.
Loads environment variables using Pydantic Settings.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Discord Config
    DISCORD_TOKEN: str = Field(default="mock_token_for_testing")
    DISCORD_CLIENT_ID: str = Field(default="0")
    DISCORD_CLIENT_SECRET: str = Field(default="")
    DISCORD_GUILD_ID: Optional[int] = Field(default=None)

    # AI Assistant Config
    DEFAULT_AI_PROVIDER: str = Field(default="openai")
    DEFAULT_AI_MODEL: str = Field(default="gpt-4o-mini")
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    GROQ_API_KEY: Optional[str] = Field(default=None)
    OPENROUTER_API_KEY: Optional[str] = Field(default=None)
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    LMSTUDIO_BASE_URL: str = Field(default="http://localhost:1234/v1")

    # Database & Cache Config
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///aria.db")
    REDIS_URL: Optional[str] = Field(default=None)

    # Dashboard Settings
    DASHBOARD_PORT: int = Field(default=8000)
    DASHBOARD_HOST: str = Field(default="0.0.0.0")
    SECRET_KEY: str = Field(default="aria-secret-key-change-in-production-123456")
    REDIRECT_URI: str = Field(default="http://localhost:8000/auth/callback")

    # General Bot Settings
    BOT_PREFIX: str = Field(default="!")
    OWNER_IDS: List[int] = Field(default_factory=list)
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")


settings = Settings()
