"""
Health and status routes.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class StatusResponse(BaseModel):
    """API status response."""
    status: str
    version: str
    service: str


@router.get("/", response_model=StatusResponse)
async def root():
    """Root endpoint - API status."""
    return StatusResponse(
        status="running",
        version="2.0.0",
        service="SalesAgent Matching API"
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "salesagent"}
