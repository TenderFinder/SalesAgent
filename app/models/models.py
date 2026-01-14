"""
Data models for SalesAgent.

Pydantic models for tenders, products, matches, and related data structures.
"""

from typing import List, Optional
from pydantic import BaseModel


class Tender(BaseModel):
    """Tender model - matches GeM API structure."""
    id: str
    display_name: str
    description: str = ""
    search_tags: List[str] = []
    market_url: str
    status: str = "active"
    service_type: Optional[str] = None
    sla: Optional[str] = None


class Product(BaseModel):
    """Product model - matches our_products.json structure."""
    name: str
    keywords: List[str]
    category: str
    description: Optional[str] = None


class Match(BaseModel):
    """Match result model."""
    tender_id: str
    tender_name: str
    matched_product: str
    score: float
    reasons: List[str] = []
    market_url: str
    match_type: str = "rule-based"  # or "ai"


class ProductCatalog(BaseModel):
    """Product catalog container."""
    company_name: str
    offerings: List[Product]


class TenderCollection(BaseModel):
    """Tender collection from API."""
    total_count: int = 0
    source: str = "GeM"
    services: List[Tender] = []


class LLMMatchResult(BaseModel):
    """LLM-specific match result."""
    tender_id: str
    tender_title: str
    matched_product: str
    matching_score: int
    customization_possibility: str = ""
    reasoning: str = ""
    
    def to_match(self, market_url: str = "") -> Match:
        """Convert to standard Match model."""
        return Match(
            tender_id=self.tender_id,
            tender_name=self.tender_title,
            matched_product=self.matched_product,
            score=float(self.matching_score),
            reasons=[self.reasoning] if self.reasoning else [],
            market_url=market_url,
            match_type="ai"
        )
