"""
Match repository for storing and retrieving match results.

Handles persistence of tender-product matches to MongoDB and JSON files.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection

from app.models import Match
from app.repositories.base import BaseRepository
from app.config import get_settings
from app.utils import get_logger

logger = get_logger(__name__)


class MatchRepository(BaseRepository[Match]):
    """
    Repository for match result storage and retrieval.
    
    Handles:
    - Storing matches in MongoDB
    - Exporting matches to JSON files
    - Querying match history
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
            Collection: MongoDB collection for matches
        """
        if self._collection is None:
            client = MongoClient(self.settings.mongo_uri)
            db = client[self.settings.mongo_db_name]
            self._collection = db[self.settings.mongo_collection_matches]
        return self._collection
    
    def find_all(self) -> List[Match]:
        """
        Retrieve all matches from MongoDB.
        
        Returns:
            List[Match]: All stored matches
        """
        logger.debug("Fetching all matches from database")
        
        try:
            documents = list(self.collection.find().sort("created_at", -1))
            matches = [Match(**doc) for doc in documents]
            logger.info(f"Retrieved {len(matches)} matches from database")
            return matches
        except Exception as e:
            logger.error(f"Error fetching matches from database: {e}")
            return []
    
    def find_by_id(self, entity_id: str) -> Optional[Match]:
        """
        Find match by tender ID.
        
        Args:
            entity_id: Tender ID
        
        Returns:
            Optional[Match]: Match if found
        """
        logger.debug(f"Finding match by tender ID: {entity_id}")
        
        try:
            doc = self.collection.find_one({"tender_id": entity_id})
            if doc:
                return Match(**doc)
            return None
        except Exception as e:
            logger.error(f"Error finding match {entity_id}: {e}")
            return None
    
    def save(self, entity: Match) -> Match:
        """
        Save a single match to MongoDB.
        
        Args:
            entity: Match to save
        
        Returns:
            Match: Saved match
        """
        logger.debug(f"Saving match: {entity.tender_id} -> {entity.matched_product}")
        
        try:
            match_dict = entity.model_dump()
            match_dict.pop('_id', None)
            
            # Upsert based on tender_id and matched_product
            self.collection.update_one(
                {
                    "tender_id": entity.tender_id,
                    "matched_product": entity.matched_product
                },
                {"$set": match_dict},
                upsert=True
            )
            
            logger.info(f"Successfully saved match: {entity.tender_id}")
            return entity
            
        except Exception as e:
            logger.error(f"Error saving match: {e}")
            raise
    
    def save_many(self, entities: List[Match]) -> List[Match]:
        """
        Save multiple matches to MongoDB.
        
        Args:
            entities: List of matches to save
        
        Returns:
            List[Match]: Saved matches
        """
        logger.info(f"Saving {len(entities)} matches to database")
        
        if not entities:
            return []
        
        try:
            match_dicts = [m.model_dump() for m in entities]
            
            for md in match_dicts:
                md.pop('_id', None)
            
            from pymongo import UpdateOne
            operations = [
                UpdateOne(
                    {
                        "tender_id": md["tender_id"],
                        "matched_product": md["matched_product"]
                    },
                    {"$set": md},
                    upsert=True
                )
                for md in match_dicts
            ]
            
            result = self.collection.bulk_write(operations)
            logger.info(f"Bulk write complete: {result.upserted_count} inserted, "
                       f"{result.modified_count} modified")
            
            return entities
            
        except Exception as e:
            logger.error(f"Error saving matches in bulk: {e}")
            raise
    
    def delete(self, entity_id: str) -> bool:
        """
        Delete match by tender ID.
        
        Args:
            entity_id: Tender ID
        
        Returns:
            bool: True if deleted
        """
        logger.debug(f"Deleting match: {entity_id}")
        
        try:
            result = self.collection.delete_one({"tender_id": entity_id})
            deleted = result.deleted_count > 0
            
            if deleted:
                logger.info(f"Deleted match: {entity_id}")
            else:
                logger.warning(f"Match not found for deletion: {entity_id}")
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting match {entity_id}: {e}")
            return False
    
    def count(self) -> int:
        """
        Count total matches in database.
        
        Returns:
            int: Total match count
        """
        try:
            count = self.collection.count_documents({})
            logger.debug(f"Total matches in database: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting matches: {e}")
            return 0
    
    def find_by_product(self, product_name: str) -> List[Match]:
        """
        Find matches for a specific product.
        
        Args:
            product_name: Product name
        
        Returns:
            List[Match]: Matches for the product
        """
        logger.debug(f"Finding matches for product: {product_name}")
        
        try:
            documents = list(self.collection.find(
                {"matched_product": product_name}
            ).sort("score", -1))
            
            matches = [Match(**doc) for doc in documents]
            logger.info(f"Found {len(matches)} matches for product '{product_name}'")
            return matches
        except Exception as e:
            logger.error(f"Error finding matches by product: {e}")
            return []
    
    def find_by_score_range(self, min_score: float, max_score: float = 100.0) -> List[Match]:
        """
        Find matches within score range.
        
        Args:
            min_score: Minimum score
            max_score: Maximum score
        
        Returns:
            List[Match]: Matches within range
        """
        logger.debug(f"Finding matches with score between {min_score} and {max_score}")
        
        try:
            documents = list(self.collection.find({
                "score": {"$gte": min_score, "$lte": max_score}
            }).sort("score", -1))
            
            matches = [Match(**doc) for doc in documents]
            logger.info(f"Found {len(matches)} matches in score range")
            return matches
        except Exception as e:
            logger.error(f"Error finding matches by score range: {e}")
            return []
    
    def export_to_json(self, file_path: Optional[str] = None, matches: Optional[List[Match]] = None) -> str:
        """
        Export matches to JSON file.
        
        Args:
            file_path: Output file path (optional)
            matches: Specific matches to export (optional, defaults to all)
        
        Returns:
            str: Path to exported file
        """
        if matches is None:
            matches = self.find_all()
        
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"{self.settings.output_dir}/matched_tenders_{timestamp}.json"
        
        logger.info(f"Exporting {len(matches)} matches to {file_path}")
        
        try:
            output_file = Path(file_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dicts for JSON serialization
            match_dicts = [m.model_dump(mode='json') for m in matches]
            
            with open(output_file, 'w') as f:
                json.dump(match_dicts, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Successfully exported matches to {file_path}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error exporting matches to JSON: {e}")
            raise
