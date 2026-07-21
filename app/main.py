from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import structlog
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    logger = structlog.get_logger()
    logger.info(
        "application_started",
        app_name=settings.app_name,
        environment=settings.app_env,
        version=settings.app_version,
    )
    yield
    logger.info("application_stopped")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-powered financial file ingestion, schema mapping, "
        "validation and transformation platform."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["General"])
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health",
    }
