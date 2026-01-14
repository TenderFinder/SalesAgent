"""
Rule-based matching agent using keyword scoring.

Implements traditional keyword-based matching algorithm.
"""

from typing import List, Dict, Any, Optional
from app.models import Tender, Product, Match
from app.agents.base_agent import BaseAgent
from app.agents.scoring import score_match
from app.utils import get_logger

logger = get_logger(__name__)


class RuleBasedMatchingAgent(BaseAgent):
    """
    Rule-based agent for tender-product matching.
    
    Uses keyword matching and scoring algorithms to find matches
    between tenders and products.
    
    Configuration:
        min_score: Minimum score threshold for matches (default: 1.0)
        max_matches_per_tender: Maximum matches to return per tender
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize rule-based matching agent.
        
        Args:
            config: Agent configuration
        """
        super().__init__(config)
        self.min_score = self.config.get('min_score', 1.0)
        self.max_matches_per_tender = self.config.get('max_matches_per_tender', None)
        
        logger.info(f"Initialized {self.name} with min_score={self.min_score}")
    
    def analyze(
        self,
        tenders: List[Tender],
        products: List[Product],
        **kwargs
    ) -> List[Match]:
        """
        Analyze tenders against products using rule-based matching.
        
        Args:
            tenders: List of tenders to analyze
            products: List of products to match against
            **kwargs: Additional parameters (min_score override)
        
        Returns:
            List[Match]: List of matches found
        """
        min_score = kwargs.get('min_score', self.min_score)
        
        logger.info(f"Starting rule-based analysis: {len(tenders)} tenders, "
                   f"{len(products)} products, min_score={min_score}")
        
        matches = []
        
        for tender in tenders:
            tender_matches = self._match_tender(tender, products, min_score)
            matches.extend(tender_matches)
        
        logger.info(f"Rule-based analysis complete: found {len(matches)} matches")
        
        return self.postprocess_matches(matches)
    
    def _match_tender(
        self,
        tender: Tender,
        products: List[Product],
        min_score: float
    ) -> List[Match]:
        """
        Match a single tender against all products.
        
        Args:
            tender: Tender to match
            products: Products to match against
            min_score: Minimum score threshold
        
        Returns:
            List[Match]: Matches for this tender
        """
        tender_matches = []
        
        for product in products:
            # Convert models to dicts for scorer
            tender_dict = {
                'id': tender.id,
                'display_name': tender.display_name,
                'description': tender.description,
                'search_tags': tender.search_tags,
                'market_url': tender.market_url
            }
            
            product_dict = {
                'name': product.name,
                'keywords': product.keywords,
                'category': product.category
            }
            
            # Calculate score
            score, reasons = score_match(product_dict, tender_dict)
            
            if score >= min_score:
                match = Match(
                    tender_id=tender.id,
                    tender_name=tender.display_name,
                    matched_product=product.name,
                    score=round(score, 2),
                    reasons=reasons,
                    market_url=tender.market_url,
                    confidence=min(score / 10.0, 1.0),  # Normalize to 0-1
                    match_type="rule-based"
                )
                tender_matches.append(match)
        
        # Sort by score (highest first)
        tender_matches.sort(key=lambda m: m.score, reverse=True)
        
        # Limit matches if configured
        if self.max_matches_per_tender:
            tender_matches = tender_matches[:self.max_matches_per_tender]
        
        return tender_matches
    
    def postprocess_matches(self, matches: List[Match]) -> List[Match]:
        """
        Postprocess matches (sort by score, remove duplicates).
        
        Args:
            matches: Raw matches
        
        Returns:
            List[Match]: Processed matches
        """
        # Remove duplicates (same tender + product combination)
        seen = set()
        unique_matches = []
        
        for match in matches:
            key = (match.tender_id, match.matched_product)
            if key not in seen:
                seen.add(key)
                unique_matches.append(match)
        
        # Sort by score
        unique_matches.sort(key=lambda m: m.score, reverse=True)
        
        logger.debug(f"Postprocessing: {len(matches)} -> {len(unique_matches)} unique matches")
        
        return unique_matches
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities.
        
        Returns:
            Dict: Agent capabilities
        """
        capabilities = super().get_capabilities()
        capabilities.update({
            "matching_type": "rule-based",
            "scoring_method": "keyword",
            "min_score": self.min_score,
            "supports_batch": True,
            "supports_streaming": False
        })
        return capabilities
