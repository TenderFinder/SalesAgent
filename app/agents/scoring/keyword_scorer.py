"""
Scoring module for tender-to-product matching.

This module provides functionality to calculate match scores between
company offerings and government tenders based on keyword matching
and semantic similarity.
"""


def score_match(offering, tender):
    """
    Calculate match score between an offering and a tender.
    
    This function evaluates how well a company's product/service offering
    matches a government tender by analyzing keyword overlap in tags and
    descriptions.
    
    Scoring Logic:
    - Exact keyword match in tender tags: +2.0 points
    - Keyword found in tender description/title: +1.0 point
    - Case-insensitive matching
    
    Args:
        offering (dict): Product/service offering with structure:
            {
                "name": str,
                "keywords": list[str],
                "category": str
            }
        tender (dict): Tender information with structure:
            {
                "id": str,
                "display_name": str,
                "description": str,
                "search_tags": list[str],
                ...
            }
    
    Returns:
        tuple: (score: float, reasons: list[str])
            - score: Numerical match score (higher is better)
            - reasons: List of human-readable match explanations
    
    Example:
        >>> offering = {
        ...     "name": "3D Printing Service",
        ...     "keywords": ["3d printing", "additive manufacturing"],
        ...     "category": "manufacturing"
        ... }
        >>> tender = {
        ...     "display_name": "3D Printing Service",
        ...     "search_tags": ["3D Printing", "Rapid Prototyping"],
        ...     "description": "Additive manufacturing services needed"
        ... }
        >>> score, reasons = score_match(offering, tender)
        >>> print(f"Score: {score}")
        Score: 4.0
        >>> print(reasons)
        ["Keyword '3d printing' found in tender tags", 
         "Keyword 'additive manufacturing' found in tender description"]
    """
    score = 0.0
    reasons = []
    
    # Extract and normalize keywords from offering
    keywords = [k.lower().strip() for k in offering.get('keywords', [])]
    
    # Extract and normalize tags from tender
    tags = [t.lower().strip() for t in tender.get('search_tags', [])]
    
    # Create searchable tender text (title + description)
    tender_title = tender.get('display_name', '').lower()
    tender_desc = tender.get('description', '').lower()
    tender_text = f"{tender_title} {tender_desc}"
    
    # Check each keyword for matches
    for keyword in keywords:
        if not keyword:  # Skip empty keywords
            continue
            
        # Check for exact match in tags (highest priority)
        if keyword in tags:
            score += 2.0
            reasons.append(f"Keyword '{keyword}' found in tender tags")
        
        # Check for keyword in tender text (lower priority)
        elif keyword in tender_text:
            score += 1.0
            reasons.append(f"Keyword '{keyword}' found in tender description")
    
    # Bonus: Category match (if both have category field)
    offering_category = offering.get('category', '').lower().strip()
    tender_type = tender.get('service_type', '').lower().strip()
    
    if offering_category and tender_type and offering_category in tender_type:
        score += 0.5
        reasons.append(f"Category match: '{offering_category}'")
    
    return score, reasons


def score_matches_batch(offerings, tenders, min_score=1.0):
    """
    Score multiple offerings against multiple tenders in batch.
    
    This is a convenience function for bulk matching operations.
    
    Args:
        offerings (list[dict]): List of product/service offerings
        tenders (list[dict]): List of tenders to match against
        min_score (float): Minimum score threshold for inclusion (default: 1.0)
    
    Returns:
        list[dict]: List of match results with structure:
            {
                "tender_id": str,
                "tender_name": str,
                "matched_offering": str,
                "score": float,
                "reasons": list[str]
            }
    
    Example:
        >>> offerings = [{"name": "AI Service", "keywords": ["ai", "ml"]}]
        >>> tenders = [{"id": "123", "display_name": "AI Development", 
        ...             "search_tags": ["AI", "Machine Learning"]}]
        >>> matches = score_matches_batch(offerings, tenders)
        >>> print(len(matches))
        1
    """
    results = []
    
    for tender in tenders:
        for offering in offerings:
            score, reasons = score_match(offering, tender)
            
            if score >= min_score:
                results.append({
                    "tender_id": tender.get("id"),
                    "tender_name": tender.get("display_name"),
                    "matched_offering": offering.get("name"),
                    "score": round(score, 2),
                    "reasons": reasons,
                    "market_url": tender.get("market_url", "")
                })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results


if __name__ == "__main__":
    # Example usage and testing
    print("🧪 Testing scorer module...\n")
    
    # Test case 1: Perfect match
    offering1 = {
        "name": "3D Printing Service",
        "keywords": ["3d printing", "additive manufacturing", "rapid prototyping"],
        "category": "manufacturing"
    }
    
    tender1 = {
        "id": "services_home_3d22084507",
        "display_name": "3D Printing Service",
        "description": "Additive manufacturing services for prototyping",
        "search_tags": ["3D Printing", "Rapid Prototyping"],
        "market_url": "https://example.com/tender1"
    }
    
    score1, reasons1 = score_match(offering1, tender1)
    print(f"Test 1 - Perfect Match:")
    print(f"  Score: {score1}")
    print(f"  Reasons: {reasons1}\n")
    
    # Test case 2: Partial match
    offering2 = {
        "name": "AI Consulting",
        "keywords": ["artificial intelligence", "machine learning"],
        "category": "it"
    }
    
    tender2 = {
        "id": "services_home_cloud_001",
        "display_name": "Cloud Migration Service",
        "description": "Cloud infrastructure migration with AI optimization",
        "search_tags": ["Cloud Computing", "Migration"],
        "market_url": "https://example.com/tender2"
    }
    
    score2, reasons2 = score_match(offering2, tender2)
    print(f"Test 2 - Partial Match:")
    print(f"  Score: {score2}")
    print(f"  Reasons: {reasons2}\n")
    
    # Test case 3: No match
    offering3 = {
        "name": "Housekeeping Service",
        "keywords": ["cleaning", "sanitation"],
        "category": "facility"
    }
    
    tender3 = {
        "id": "services_home_software_002",
        "display_name": "Software Development",
        "description": "Custom software development services",
        "search_tags": ["Software", "Development"],
        "market_url": "https://example.com/tender3"
    }
    
    score3, reasons3 = score_match(offering3, tender3)
    print(f"Test 3 - No Match:")
    print(f"  Score: {score3}")
    print(f"  Reasons: {reasons3}\n")
    
    print("✅ Scorer module tests complete!")
