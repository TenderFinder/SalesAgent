"""
FastAPI application factory.

Creates and configures the FastAPI application with all routes.
"""


from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv

from app.routes import health_router, matching_router, tenders_router

# Load environment variables from app/.env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="SalesAgent API",
        description="Government Tender Matching System",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Include routers
    app.include_router(health_router)
    app.include_router(matching_router)
    app.include_router(tenders_router)
    
    return app


# Create app instance
app = create_app()
