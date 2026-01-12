#!/usr/bin/env python3
"""
Run Rule-Based Matching

Simple script to run rule-based matching on local tender files.
"""

import json
import sys
from app.agents.rule_based_agent import RuleBasedMatchingAgent
from app.models import Tender, Product


def main():
    """Run rule-based matching."""
    print("🚀 Starting Rule-Based Matching...")
    
    # Load data
    try:
        with open('data/tenders/available_tenders.json') as f:
            tenders_data = json.load(f)
        with open('data/products/our_products.json') as f:
            products_data = json.load(f)
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("💡 Make sure you have run 'python main.py' first to fetch tenders")
        sys.exit(1)
    
    # Convert to models
    tenders = [Tender(**t) for t in tenders_data.get('services', [])]
    products = [Product(**p) for p in products_data.get('offerings', [])]
    
    print(f"📡 Loaded {len(tenders)} tenders and {len(products)} products")
    
    # Get min_score from command line or use default
    min_score = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    print(f"🎯 Minimum score threshold: {min_score}")
    
    # Run matching
    agent = RuleBasedMatchingAgent()
    matches = agent.analyze(tenders, products, min_score=min_score)
    
    print(f"\n✅ Found {len(matches)} matches:\n")
    
    # Display results
    for i, match in enumerate(matches[:10], 1):
        print(f"{i}. {match.tender_name}")
        print(f"   Product: {match.matched_product}")
        print(f"   Score: {match.score}")
        print(f"   Reasons: {', '.join(match.reasons)}")
        print(f"   URL: {match.market_url}")
        print()
    
    if len(matches) > 10:
        print(f"... and {len(matches) - 10} more matches")
    
    # Save to file
    output_file = 'data/outputs/rule_based_matches.json'
    match_dicts = [
        {
            "tender_id": m.tender_id,
            "tender_name": m.tender_name,
            "matched_product": m.matched_product,
            "score": m.score,
            "reasons": m.reasons,
            "market_url": m.market_url
        }
        for m in matches
    ]
    
    with open(output_file, 'w') as f:
        json.dump(match_dicts, f, indent=2)
    
    print(f"💾 Saved {len(matches)} matches to {output_file}")


if __name__ == "__main__":
    main()
