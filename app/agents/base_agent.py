"""
Base agent interface for AI components.

Defines the contract that all agents must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models import Tender, Product, Match


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    
    Agents are autonomous components that perform specific AI tasks
    such as matching, scoring, or analysis.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize agent with configuration.
        
        Args:
            config: Agent-specific configuration
        """
        self.config = config or {}
        self.name = self.__class__.__name__
    
    @abstractmethod
    def analyze(
        self,
        tenders: List[Tender],
        products: List[Product],
        **kwargs
    ) -> List[Match]:
        """
        Analyze tenders against products to find matches.
        
        Args:
            tenders: List of tenders to analyze
            products: List of products to match against
            **kwargs: Additional parameters
        
        Returns:
            List[Match]: List of matches found
        """
        pass
    
    def preprocess_tenders(self, tenders: List[Tender]) -> List[Tender]:
        """
        Preprocess tenders before analysis (optional override).
        
        Args:
            tenders: Raw tenders
        
        Returns:
            List[Tender]: Processed tenders
        """
        return tenders
    
    def preprocess_products(self, products: List[Product]) -> List[Product]:
        """
        Preprocess products before analysis (optional override).
        
        Args:
            products: Raw products
        
        Returns:
            List[Product]: Processed products
        """
        return products
    
    def postprocess_matches(self, matches: List[Match]) -> List[Match]:
        """
        Postprocess matches after analysis (optional override).
        
        Args:
            matches: Raw matches
        
        Returns:
            List[Match]: Processed matches
        """
        return matches
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities and metadata.
        
        Returns:
            Dict: Agent capabilities
        """
        return {
            "name": self.name,
            "type": self.__class__.__bases__[0].__name__,
            "config": self.config
        }
