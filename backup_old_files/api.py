"""
FastAPI Application Entry Point

This is a thin wrapper that imports the app from app.main
Run with: uvicorn api:app --reload
"""

from app.main import app

__all__ = ["app"]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
