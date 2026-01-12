"""
Simple configuration management without external dependencies.
"""

import os


class Settings:
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME = "SalesAgent"
    APP_VERSION = "2.0.0"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", None)
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def log_level(self):
        return self.LOG_LEVEL
    
    @property
    def log_file(self):
        return self.LOG_FILE
    
    @property
    def log_format(self):
        return self.LOG_FORMAT
    
    # GeM API
    GEM_API_URL = os.getenv(
        "GEM_API_URL",
        "https://mkp.gem.gov.in/cms/others/api/services/list.json?search%5Bstatus_in%5D%5B%5D=active&_ln=en"
    )
    
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "gem_database")
    MONGO_COLLECTION_TENDERS = "tenders"
    MONGO_COLLECTION_MATCHES = "matches"
    
    # LLM
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
    
    # Matching
    MIN_MATCH_SCORE = float(os.getenv("MIN_MATCH_SCORE", "1.0"))
    
    # Data Source Configuration
    # Options: "file" or "mongodb"
    TENDER_DATA_SOURCE = os.getenv("TENDER_DATA_SOURCE", "file")  # "file" or "mongodb"
    PRODUCT_DATA_SOURCE = os.getenv("PRODUCT_DATA_SOURCE", "file")  # "file" or "mongodb"
    
    # Paths
    DATA_DIR = "data"
    PRODUCTS_FILE = os.getenv("PRODUCTS_FILE", "data/products/our_products.json")
    TENDERS_FILE = os.getenv("TENDERS_FILE", "data/tenders/available_tenders.json")
    OUTPUT_DIR = "data/outputs"
    
    @property
    def products_file(self):
        return self.PRODUCTS_FILE
    
    @property
    def output_dir(self):
        return self.OUTPUT_DIR
    
    @property
    def min_match_score(self):
        return self.MIN_MATCH_SCORE
    
    @property
    def mongo_uri(self):
        return self.MONGO_URI
    
    @property
    def mongo_db_name(self):
        return self.MONGO_DB_NAME
    
    @property
    def mongo_collection_tenders(self):
        return self.MONGO_COLLECTION_TENDERS
    
    @property
    def mongo_collection_matches(self):
        return self.MONGO_COLLECTION_MATCHES
    
    @property
    def gem_api_url(self):
        return self.GEM_API_URL
    
    @property
    def tender_data_source(self):
        return self.TENDER_DATA_SOURCE
    
    @property
    def product_data_source(self):
        return self.PRODUCT_DATA_SOURCE
    
    @property
    def tenders_file(self):
        return self.TENDERS_FILE


# Singleton instance
_settings = Settings()


def get_settings():
    """Get settings instance."""
    return _settings


def get_llm_config():
    """Get LLM configuration."""
    settings = get_settings()
    return {
        "model": settings.OLLAMA_MODEL,
        "timeout": 120
    }

