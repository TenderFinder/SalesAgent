"""
Tender repository for GeM API integration and MongoDB storage.

Handles fetching tenders from external API and persisting to database.
"""

import requests
from typing import List, Optional, Dict, Any
from pymongo import MongoClient
from pymongo.collection import Collection

from app.models import Tender, TenderCollection
from app.repositories.base import BaseRepository
from app.config import get_settings
from app.utils import get_logger

logger = get_logger(__name__)


class TenderRepository(BaseRepository[Tender]):
    """
    Repository for tender data access.
    
    Handles:
    - Fetching tenders from GeM API
    - Storing tenders in MongoDB
    - Retrieving tenders from MongoDB
    """
    
    def __init__(self):
        """Initialize repository with configuration."""
        self.settings = get_settings()
        self._collection: Optional[Collection] = None
    
    @property
    def collection(self) -> Collection:
        """
        Get MongoDB collection (lazy initialization).
        
        Returns:
            Collection: MongoDB collection for tenders
        """
        if self._collection is None:
            client = MongoClient(self.settings.mongo_uri)
            db = client[self.settings.mongo_db_name]
            self._collection = db[self.settings.mongo_collection_tenders]
        return self._collection
    
    def fetch_from_api(self) -> TenderCollection:
        """
        Fetch tenders from GeM API.
        
        Returns:
            TenderCollection: Collection of tenders from API
        
        Raises:
            requests.RequestException: If API request fails
        """
        logger.info(f"Fetching tenders from API: {self.settings.gem_api_url}")
        
        try:
            response = requests.get(
                self.settings.gem_api_url,
                timeout=self.settings.api_timeout
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched {len(data.get('services', []))} tenders")
            
            # Convert to TenderCollection model
            tender_collection = TenderCollection(**data)
            return tender_collection
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch tenders from API: {e}")
            raise
    
    def find_all(self) -> List[Tender]:
        """
        Retrieve all tenders from MongoDB.
        
        Returns:
            List[Tender]: All stored tenders
        """
        logger.debug("Fetching all tenders from database")
        
        try:
            documents = list(self.collection.find())
            tenders = [Tender(**doc) for doc in documents]
            logger.info(f"Retrieved {len(tenders)} tenders from database")
            return tenders
        except Exception as e:
            logger.error(f"Error fetching tenders from database: {e}")
            return []
    
    def find_by_id(self, entity_id: str) -> Optional[Tender]:
        """
        Find tender by ID.
        
        Args:
            entity_id: Tender ID
        
        Returns:
            Optional[Tender]: Tender if found
        """
        logger.debug(f"Finding tender by ID: {entity_id}")
        
        try:
            doc = self.collection.find_one({"id": entity_id})
            if doc:
                return Tender(**doc)
            return None
        except Exception as e:
            logger.error(f"Error finding tender {entity_id}: {e}")
            return None
    
    def save(self, entity: Tender) -> Tender:
        """
        Save a single tender to MongoDB.
        
        Args:
            entity: Tender to save
        
        Returns:
            Tender: Saved tender
        """
        logger.debug(f"Saving tender: {entity.id}")
        
        try:
            # Convert to dict and remove MongoDB _id if present
            tender_dict = entity.model_dump()
            tender_dict.pop('_id', None)
            
            # Upsert (update if exists, insert if not)
            self.collection.update_one(
                {"id": entity.id},
                {"$set": tender_dict},
                upsert=True
            )
            
            logger.info(f"Successfully saved tender: {entity.id}")
            return entity
            
        except Exception as e:
            logger.error(f"Error saving tender {entity.id}: {e}")
            raise
    
    def save_many(self, entities: List[Tender]) -> List[Tender]:
        """
        Save multiple tenders to MongoDB.
        
        Args:
            entities: List of tenders to save
        
        Returns:
            List[Tender]: Saved tenders
        """
        logger.info(f"Saving {len(entities)} tenders to database")
        
        if not entities:
            return []
        
        try:
            # Convert to dicts
            tender_dicts = [t.model_dump() for t in entities]
            
            # Remove _id fields
            for td in tender_dicts:
                td.pop('_id', None)
            
            # Bulk upsert
            from pymongo import UpdateOne
            operations = [
                UpdateOne(
                    {"id": td["id"]},
                    {"$set": td},
                    upsert=True
                )
                for td in tender_dicts
            ]
            
            result = self.collection.bulk_write(operations)
            logger.info(f"Bulk write complete: {result.upserted_count} inserted, "
                       f"{result.modified_count} modified")
            
            return entities
            
        except Exception as e:
            logger.error(f"Error saving tenders in bulk: {e}")
            raise
    
    def delete(self, entity_id: str) -> bool:
        """
        Delete tender by ID.
        
        Args:
            entity_id: Tender ID to delete
        
        Returns:
            bool: True if deleted
        """
        logger.debug(f"Deleting tender: {entity_id}")
        
        try:
            result = self.collection.delete_one({"id": entity_id})
            deleted = result.deleted_count > 0
            
            if deleted:
                logger.info(f"Deleted tender: {entity_id}")
            else:
                logger.warning(f"Tender not found for deletion: {entity_id}")
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting tender {entity_id}: {e}")
            return False
    
    def count(self) -> int:
        """
        Count total tenders in database.
        
        Returns:
            int: Total tender count
        """
        try:
            count = self.collection.count_documents({})
            logger.debug(f"Total tenders in database: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting tenders: {e}")
            return 0
    
    def find_by_status(self, status: str = "active") -> List[Tender]:
        """
        Find tenders by status.
        
        Args:
            status: Tender status to filter by
        
        Returns:
            List[Tender]: Matching tenders
        """
        logger.debug(f"Finding tenders with status: {status}")
        
        try:
            documents = list(self.collection.find({"status": status}))
            tenders = [Tender(**doc) for doc in documents]
            logger.info(f"Found {len(tenders)} tenders with status '{status}'")
            return tenders
        except Exception as e:
            logger.error(f"Error finding tenders by status: {e}")
            return []
