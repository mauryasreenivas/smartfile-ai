from functools import lru_cache
from pathlib import Path
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
    app_version: str = "0.2.0"
    api_v1_prefix: str = "/api/v1"

    max_upload_size_mb: int = Field(default=25, ge=1, le=500)
    preview_rows: int = Field(default=10, ge=1, le=100)

    upload_directory: Path = Path("uploads")

    allowed_extensions: set[str] = {
        ".csv",
        ".xlsx",
    }

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
