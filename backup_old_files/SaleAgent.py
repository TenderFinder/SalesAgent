"""
Sales Agent - LLM-Powered Matching

AI-powered tender matching using Ollama.
Now uses the new agent architecture.
"""

import json
from app.agents.llm_agent import LLMMatchingAgent
from app.repositories.product_repository import ProductRepository
from app.models import Tender, Product
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_json(path):
    """Load JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def main():
    """Main LLM matching workflow."""
    print("🚀 Starting Sales Agent Analysis with Ollama (AI Mode)...")
    logger.info("Starting LLM matching")
    
    try:
        # Load data
        tenders_data = load_json('data/tenders/available_tenders.json')
        products_data = load_json('data/products/our_products.json')
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        logger.error(f"File not found: {e}")
        return
    
    # Convert to models
    tenders = [Tender(**t) for t in tenders_data.get('services', [])]
    offerings = [Product(**p) for p in products_data.get('offerings', [])]
    
    print(f"📡 Loaded {len(tenders)} tenders and {len(offerings)} products.")
    logger.info(f"Loaded {len(tenders)} tenders and {len(offerings)} products")
    
    print("🧠 Analyzing matches with AI...")
    
    # Use LLM agent
    agent = LLMMatchingAgent()
    matches = agent.analyze(tenders, offerings)
    
    # Output results
    print(f"\n✅ Analysis Complete. Found {len(matches)} matches:")
    
    # Convert to dict for display
    match_dicts = [
        {
            "tender_id": m.tender_id,
            "tender_title": m.tender_name,
            "matched_product": m.matched_product,
            "matching_score": int(m.score),
            "reasoning": m.reasons[0] if m.reasons else "",
            "customization_possibility": m.metadata.get("customization_possibility", "")
        }
        for m in matches
    ]
    
    print(json.dumps(match_dicts, indent=4))
    
    # Save to file
    output_file = 'data/outputs/matched_tenders.json'
    with open(output_file, 'w') as f:
        json.dump(match_dicts, f, indent=4)
    print(f"💾 Saved results to {output_file}")
    logger.info(f"Saved {len(matches)} matches to {output_file}")


if __name__ == "__main__":
    main()
