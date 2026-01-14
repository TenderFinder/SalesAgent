"""
Product repository for managing company product catalog.

Handles loading and managing product offerings from JSON files and database.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from app.models import Product, ProductCatalog
from app.repositories.base import BaseRepository
from app.config import get_settings
from app.utils import get_logger

logger = get_logger(__name__)


class ProductRepository(BaseRepository[Product]):
    """
    Repository for product catalog management.
    
    Handles:
    - Loading products from JSON file
    - In-memory product storage
    - Product CRUD operations
    """
    
    def __init__(self, products_file: Optional[str] = None):
        """
        Initialize repository.
        
        Args:
            products_file: Path to products JSON file (optional)
        """
        self.settings = get_settings()
        self.products_file = products_file or self.settings.products_file
        self._catalog: Optional[ProductCatalog] = None
        self._products: List[Product] = []
    
    def load_from_file(self) -> ProductCatalog:
        """
        Load product catalog from JSON file.
        
        Returns:
            ProductCatalog: Loaded product catalog
        
        Raises:
            FileNotFoundError: If products file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        logger.info(f"Loading products from file: {self.products_file}")
        
        file_path = Path(self.products_file)
        if not file_path.exists():
            logger.error(f"Products file not found: {self.products_file}")
            raise FileNotFoundError(f"Products file not found: {self.products_file}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            catalog = ProductCatalog(**data)
            self._catalog = catalog
            self._products = catalog.offerings
            
            logger.info(f"Loaded {len(self._products)} products from catalog")
            return catalog
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in products file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            raise
    
    def find_all(self) -> List[Product]:
        """
        Get all products.
        
        Returns:
            List[Product]: All products in catalog
        """
        if not self._products:
            self.load_from_file()
        
        logger.debug(f"Returning {len(self._products)} products")
        return self._products
    
    def find_by_id(self, entity_id: str) -> Optional[Product]:
        """
        Find product by name (using name as ID).
        
        Args:
            entity_id: Product name
        
        Returns:
            Optional[Product]: Product if found
        """
        if not self._products:
            self.load_from_file()
        
        for product in self._products:
            if product.name == entity_id:
                logger.debug(f"Found product: {entity_id}")
                return product
        
        logger.debug(f"Product not found: {entity_id}")
        return None
    
    def find_by_category(self, category: str) -> List[Product]:
        """
        Find products by category.
        
        Args:
            category: Product category
        
        Returns:
            List[Product]: Products in category
        """
        if not self._products:
            self.load_from_file()
        
        products = [p for p in self._products if p.category.lower() == category.lower()]
        logger.debug(f"Found {len(products)} products in category '{category}'")
        return products
    
    def save(self, entity: Product) -> Product:
        """
        Add or update a product in memory.
        
        Args:
            entity: Product to save
        
        Returns:
            Product: Saved product
        """
        if not self._products:
            self.load_from_file()
        
        # Check if product exists
        existing_idx = None
        for idx, p in enumerate(self._products):
            if p.name == entity.name:
                existing_idx = idx
                break
        
        if existing_idx is not None:
            self._products[existing_idx] = entity
            logger.info(f"Updated product: {entity.name}")
        else:
            self._products.append(entity)
            logger.info(f"Added new product: {entity.name}")
        
        return entity
    
    def save_many(self, entities: List[Product]) -> List[Product]:
        """
        Save multiple products.
        
        Args:
            entities: Products to save
        
        Returns:
            List[Product]: Saved products
        """
        for entity in entities:
            self.save(entity)
        
        logger.info(f"Saved {len(entities)} products")
        return entities
    
    def delete(self, entity_id: str) -> bool:
        """
        Delete product by name.
        
        Args:
            entity_id: Product name
        
        Returns:
            bool: True if deleted
        """
        if not self._products:
            self.load_from_file()
        
        initial_count = len(self._products)
        self._products = [p for p in self._products if p.name != entity_id]
        
        deleted = len(self._products) < initial_count
        if deleted:
            logger.info(f"Deleted product: {entity_id}")
        else:
            logger.warning(f"Product not found for deletion: {entity_id}")
        
        return deleted
    
    def count(self) -> int:
        """
        Count total products.
        
        Returns:
            int: Product count
        """
        if not self._products:
            self.load_from_file()
        
        return len(self._products)
    
    def save_to_file(self, file_path: Optional[str] = None) -> None:
        """
        Save current product catalog to JSON file.
        
        Args:
            file_path: Output file path (optional)
        """
        output_path = file_path or self.products_file
        
        if not self._catalog:
            logger.warning("No catalog loaded, creating new one")
            self._catalog = ProductCatalog(
                company_name="Company",
                offerings=self._products
            )
        else:
            self._catalog.offerings = self._products
        
        logger.info(f"Saving {len(self._products)} products to {output_path}")
        
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(
                    self._catalog.model_dump(),
                    f,
                    indent=2,
                    ensure_ascii=False
                )
            
            logger.info(f"Successfully saved products to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving products to file: {e}")
            raise
