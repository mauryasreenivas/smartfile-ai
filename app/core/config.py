from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "SmartFile AI"
    app_env: Literal["development", "testing", "production"] = "development"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    max_upload_size_mb: int = Field(default=25, ge=1, le=500)


@lru_cache
def get_settings() -> Settings:
    return Settings()
