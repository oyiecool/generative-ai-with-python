# src/aikit/settings.py
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables and .env."""

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="AIKIT_", extra="ignore"
    )

    provider: Literal["anthropic", "openai", "ollama"] = "anthropic"
    chat_model: str = Field(..., description="Main model for generation")
    fast_model: str | None = Field(None, description="Cheaper model for simple tasks")
    embed_model: str | None = None
    max_output_tokens: int = Field(1024, ge=1, le=64_000)
    temperature: float = Field(0.2, ge=0.0, le=2.0)
    request_timeout_s: float = 60.0
    log_prompts: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
