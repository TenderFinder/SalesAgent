"""
Tender Matching Agent

Rule-based matching using the new agent architecture.
Maintains compatibility with original matcher.py interface.
"""

import json
from typing import List, Dict
from app.agents.rule_based_agent import RuleBasedMatchingAgent
from app.repositories.product_repository import ProductRepository
from app.models import Tender, Product


class TenderMatchingAgent:
    """
    Tender matching agent - compatible with original interface.
    
    Now uses the new architecture internally.
    """
    
    def __init__(self, product_file: str, tender_file: str):
        """
        Initialize matcher with product and tender files.
        
        Args:
            product_file: Path to products JSON
            tender_file: Path to tenders JSON
        """
        # Load products
        with open(product_file) as pf:
            product_data = json.load(pf)
            self.offerings = [Product(**p) for p in product_data["offerings"]]
        
        # Load tenders
        with open(tender_file) as tf:
            tender_data = json.load(tf)
            self.tenders = [Tender(**t) for t in tender_data["services"]]
        
        # Initialize agent
        self.agent = RuleBasedMatchingAgent()
    
    def find_matches(self, min_score: float = 1.0) -> List[Dict]:
        """
        Find matches between tenders and products.
        
        Args:
            min_score: Minimum score threshold
        
        Returns:
            List of match dictionaries
        """
        # Use the new agent
        matches = self.agent.analyze(
            tenders=self.tenders,
            products=self.offerings,
            min_score=min_score
        )
        
        # Convert to dict format for compatibility
        results = []
        for match in matches:
            results.append({
                "tender_id": match.tender_id,
                "tender_name": match.tender_name,
                "matched_offering": match.matched_product,
                "score": round(match.score, 2),
                "reason": match.reasons,
                "market_url": match.market_url
            })
        
        return results
