#!/usr/bin/env python3
"""
SalesAgent - Start API Server

Starts the FastAPI server for the SalesAgent matching system.

Usage:
    python run_api.py
    
Or directly:
    uvicorn app.main:app --reload
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting SalesAgent API Server...")
    print("📡 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
