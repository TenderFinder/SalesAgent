"""
Base repository interface for data access layer.

Defines the contract that all repositories must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar, Dict, Any

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository providing common CRUD operations.
    
    Type Parameters:
        T: The model type this repository manages
    """
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Retrieve all entities.
        
        Returns:
            List[T]: List of all entities
        """
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """
        Find entity by ID.
        
        Args:
            entity_id: Unique identifier
        
        Returns:
            Optional[T]: Entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save a single entity.
        
        Args:
            entity: Entity to save
        
        Returns:
            T: Saved entity
        """
        pass
    
    @abstractmethod
    def save_many(self, entities: List[T]) -> List[T]:
        """
        Save multiple entities.
        
        Args:
            entities: List of entities to save
        
        Returns:
            List[T]: Saved entities
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete entity by ID.
        
        Args:
            entity_id: ID of entity to delete
        
        Returns:
            bool: True if deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """
        Count total entities.
        
        Returns:
            int: Total count
        """
        pass
    
    def find_by_criteria(self, criteria: Dict[str, Any]) -> List[T]:
        """
        Find entities matching criteria.
        
        Args:
            criteria: Search criteria
        
        Returns:
            List[T]: Matching entities
        """
        # Default implementation - can be overridden
        return []
