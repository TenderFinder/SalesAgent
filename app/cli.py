"""
CLI commands for SalesAgent.

Command-line interface for various operations.
"""

from app.config import get_settings
from app.repositories.tender_repository import TenderRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


def fetch_tenders():
    """Fetch tenders from GeM API and store in MongoDB."""
    print("🚀 Starting GEM API → MongoDB pipeline")
    logger.info("Starting tender fetch pipeline")
    
    settings = get_settings()
    tender_repo = TenderRepository()
    
    try:
        # Fetch from API
        tender_collection = tender_repo.fetch_from_api()
        tenders = tender_collection.services
        
        if tenders:
            # Save to MongoDB
            tender_repo.save_many(tenders)
            print(f"✅ Successfully stored {len(tenders)} tenders in MongoDB")
            logger.info(f"Stored {len(tenders)} tenders")
        else:
            print("⚠️  No data to store")
            logger.warning("No tenders fetched from API")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise


def main():
    """Main CLI entry point."""
    fetch_tenders()
