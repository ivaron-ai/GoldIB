"""FastAPI application and routes."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.logging_config import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Ralph",
    description="Trading Infrastructure API",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    logger.info("health_check_called")
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "ralph"}
    )


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {"message": "Welcome to Ralph API", "version": "0.1.0"}
