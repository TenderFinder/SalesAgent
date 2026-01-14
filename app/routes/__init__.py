"""
Routes package for FastAPI application.
"""

# Import routers from route modules
from app.routes.health import router as health_router
from app.routes.matching import router as matching_router
from app.routes.tenders import router as tenders_router

__all__ = ["health_router", "matching_router", "tenders_router"]
