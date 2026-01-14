"""
Configuration module for SalesAgent.

This module manages application configuration using environment variables
for sensitive data like database credentials.

Environment Variables:
    MONGO_URI: MongoDB connection string (required for production)
    DB_NAME: Database name (default: "gem_database")
    COLLECTION_NAME: Collection name (default: "services")
"""

import os

# GeM API endpoint for fetching government tenders
API_URL = "https://mkp.gem.gov.in/cms/others/api/services/list.json?search%5Bstatus_in%5D%5B%5D=active&_ln=en"

# MongoDB Configuration
# IMPORTANT: Set MONGO_URI as an environment variable in production
# Example: export MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net/"
MONGO_URI = os.getenv(
    "MONGO_URI", 
    "mongodb://localhost:27017/"  # Default for local development only
)

DB_NAME = os.getenv("DB_NAME", "gem_database")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "services")

# Validate configuration
if MONGO_URI == "mongodb://localhost:27017/":
    print("⚠️  WARNING: Using default local MongoDB URI. Set MONGO_URI environment variable for production!")