"""
Matching service for orchestrating tender-product matching workflows.

Coordinates between repositories and agents to perform matching operations.
"""

from typing import List, Optional, Dict, Any
from app.models import Tender, Product, Match
from app.repositories import TenderRepository, ProductRepository, MatchRepository
from app.agents import RuleBasedMatchingAgent, LLMMatchingAgent
from app.utils import get_logger

logger = get_logger(__name__)


class MatchingService:
    """
    Service for orchestrating matching operations.
    
    Coordinates:
    - Loading tenders and products
    - Running matching agents
    - Storing match results
    """
    
    def __init__(
        self,
        tender_repo: Optional[TenderRepository] = None,
        product_repo: Optional[ProductRepository] = None,
        match_repo: Optional[MatchRepository] = None,
        rule_agent: Optional[RuleBasedMatchingAgent] = None,
        llm_agent: Optional[LLMMatchingAgent] = None
    ):
        """
        Initialize matching service.
        
        Args:
            tender_repo: Tender repository (optional)
            product_repo: Product repository (optional)
            match_repo: Match repository (optional)
            rule_agent: Rule-based agent (optional)
            llm_agent: LLM agent (optional)
        """
        self.tender_repo = tender_repo or TenderRepository()
        self.product_repo = product_repo or ProductRepository()
        self.match_repo = match_repo or MatchRepository()
        self.rule_agent = rule_agent or RuleBasedMatchingAgent()
        self.llm_agent = llm_agent or LLMMatchingAgent()
        
        logger.info("Initialized MatchingService")
    
    def execute_matching(
        self,
        use_ai: bool = False,
        min_score: float = 1.0,
        save_results: bool = True,
        export_json: bool = True
    ) -> List[Match]:
        """
        Execute complete matching workflow.
        
        Args:
            use_ai: Use LLM agent instead of rule-based
            min_score: Minimum match score threshold
            save_results: Save results to database
            export_json: Export results to JSON file
        
        Returns:
            List[Match]: Found matches
        """
        logger.info(f"Starting matching workflow (use_ai={use_ai}, min_score={min_score})")
        
        # Load data
        tenders = self._load_tenders()
        products = self._load_products()
        
        if not tenders:
            logger.warning("No tenders available for matching")
            return []
        
        if not products:
            logger.warning("No products available for matching")
            return []
        
        # Execute matching
        agent = self.llm_agent if use_ai else self.rule_agent
        logger.info(f"Using agent: {agent.name}")
        
        matches = agent.analyze(tenders, products, min_score=min_score)
        
        logger.info(f"Matching complete: {len(matches)} matches found")
        
        # Save results
        if save_results and matches:
            self.match_repo.save_many(matches)
            logger.info("Matches saved to database")
        
        # Export to JSON
        if export_json and matches:
            file_path = self.match_repo.export_to_json(matches=matches)
            logger.info(f"Matches exported to {file_path}")
        
        return matches
    
    def _load_tenders(self) -> List[Tender]:
        """Load tenders based on configuration."""
        from app.config import get_settings
        import json
        
        settings = get_settings()
        logger.debug(f"Loading tenders (source: {settings.tender_data_source})")
        
        if settings.tender_data_source == "file":
            # Load from local JSON file
            try:
                logger.info(f"Loading tenders from file: {settings.tenders_file}")
                with open(settings.tenders_file, 'r') as f:
                    data = json.load(f)
                tenders = [Tender(**t) for t in data.get('services', [])]
                logger.info(f"Loaded {len(tenders)} tenders from file")
                return tenders
            except FileNotFoundError:
                logger.error(f"Tenders file not found: {settings.tenders_file}")
                return []
            except Exception as e:
                logger.error(f"Error loading tenders from file: {e}")
                return []
        else:
            # Load from MongoDB
            logger.info("Loading tenders from MongoDB")
            tenders = self.tender_repo.find_all()
            
            if not tenders:
                logger.info("No tenders in database, fetching from API")
                try:
                    tender_collection = self.tender_repo.fetch_from_api()
                    tenders = tender_collection.services
                    
                    # Save to database
                    if tenders:
                        self.tender_repo.save_many(tenders)
                except Exception as e:
                    logger.error(f"Failed to fetch tenders from API: {e}")
                    return []
            
            logger.info(f"Loaded {len(tenders)} tenders from MongoDB")
            return tenders
    
    def _load_products(self) -> List[Product]:
        """Load products based on configuration."""
        from app.config import get_settings
        
        settings = get_settings()
        logger.debug(f"Loading products (source: {settings.product_data_source})")
        
        if settings.product_data_source == "file":
            # Product repo always loads from file by default
            try:
                products = self.product_repo.find_all()
                logger.info(f"Loaded {len(products)} products from file")
                return products
            except Exception as e:
                logger.error(f"Failed to load products: {e}")
                return []
        else:
            # Load from MongoDB (if you implement this in future)
            try:
                products = self.product_repo.find_all()
                logger.info(f"Loaded {len(products)} products")
                return products
            except Exception as e:
                logger.error(f"Failed to load products: {e}")
                return []
    
    def get_match_statistics(self) -> Dict[str, Any]:
        """
        Get matching statistics.
        
        Returns:
            Dict: Statistics about matches
        """
        total_matches = self.match_repo.count()
        
        if total_matches == 0:
            return {
                "total_matches": 0,
                "by_product": {},
                "score_distribution": {}
            }
        
        all_matches = self.match_repo.find_all()
        
        # Group by product
        by_product = {}
        for match in all_matches:
            product = match.matched_product
            by_product[product] = by_product.get(product, 0) + 1
        
        # Score distribution
        score_ranges = {
            "0-25": 0,
            "26-50": 0,
            "51-75": 0,
            "76-100": 0
        }
        
        for match in all_matches:
            score = match.score
            if score <= 25:
                score_ranges["0-25"] += 1
            elif score <= 50:
                score_ranges["26-50"] += 1
            elif score <= 75:
                score_ranges["51-75"] += 1
            else:
                score_ranges["76-100"] += 1
        
        return {
            "total_matches": total_matches,
            "by_product": by_product,
            "score_distribution": score_ranges
        }
