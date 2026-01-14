#!/usr/bin/env python3
"""
Start the SalesAgent FastAPI server.

Usage:
    python start_api.py
    
Or:
    uvicorn api:app --reload --host 0.0.0.0 --port 8000
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting SalesAgent API Server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    print("🔍 Interactive API: http://localhost:8000/redoc")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
