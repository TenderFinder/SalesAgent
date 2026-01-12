"""
Main CLI Entry Point

Fetches tenders from GeM API and stores in MongoDB.
This is a thin wrapper that imports from app.cli

Usage:
    python main.py
"""

from app.cli import main

if __name__ == "__main__":
    main()
