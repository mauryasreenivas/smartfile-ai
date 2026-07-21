from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import get_settings

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    application: str
    version: str
    environment: str
    timestamp_utc: datetime


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        timestamp_utc=datetime.now(UTC),
    )
