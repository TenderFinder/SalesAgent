import json
import ollama

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def clean_html(text):
    """Basic cleanup if needed, though LLMs handle HTML well."""
    return text

def analyze_match(tender, product):
    """
    Uses Ollama to analyze the match between a tender and a product.
    Returns a dict with 'score', 'customization_analysis', and 'reasoning'.
    """
    
    # Construct a concise prompt
    tensor_desc = f"Title: {tender.get('display_name')}\nDescription: {tender.get('description')}\nSLA: {tender.get('sla')}\nTags: {tender.get('search_tags')}"
    product_desc = f"Product: {product.get('name')}\nKeywords: {product.get('keywords')}\nCategory: {product.get('category')}"

    prompt = f"""
    You are a Sales Engineer. Analyze if the following Company Product can fulfill the Tender requirement.
    
    TENDER DETAILS:
    {tensor_desc}
    
    COMPANY PRODUCT:
    {product_desc}
    
    Task:
    1. Determine a Matching Score (0-100). 100 = Perfect match, 0 = No relation.
    2. Analyze if the product can be customized to fit (if not a perfect match).
    
    Return ONLY a JSON object in this format:
    {{
        "score": <int>,
        "customization_possibility": "<string explanation>",
        "reasoning": "<short reasoning>"
    }}
    """

    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        content = response['message']['content']
        # Attempt to parse JSON from the response. 
        # LLMs might add text around it, so we might need robust parsing if it fails often.
        # For now, relying on "Return ONLY JSON" instruction.
        
        print(f"DEBUG LLM RAW: {content[:100]}...") # Debugging
        # Check if content is wrapped in markdown code block
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        return json.loads(content.strip())
        
    except Exception as e:
        print(f"DEBUG ERROR: {e}") # Debugging
        return {
            "score": 0,
            "customization_possibility": "Error in analysis",
            "reasoning": str(e)
        }

def main():
    print("🚀 Starting Sales Agent Analysis with Ollama...")
    
    try:
        tenders_data = load_json('final.json')
        products_data = load_json('data/product.json')
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return

    tenders = tenders_data.get('services', [])
    offerings = products_data.get('offerings', [])
    
    matches = []
    
    print(f"📡 Loaded {len(tenders)} tenders and {len(offerings)} products.")
    print("🧠 Analyzing matches contextually (this may take a moment)...")

    for tender in tenders:
        best_match = None
        highest_score = -1
        
        # Strategies: 
        # 1. Compare against ALL products and pick the best? 
        # 2. Return all viable matches (score > 50)?
        # Let's return all matches with score > 60 to be helpful.
        
        for product in offerings:
            # Optimization: Quick keyword check? 
            # Skipping optimization to ensure semantic matching (e.g. "Sanitation" vs "Cleaning").
            
            print(f"   Running: {tender['display_name']} vs {product['name']}...")
            result = analyze_match(tender, product)
            
            if result['score'] >= 50:  # Threshold for relevance
                match_record = {
                    "tender_id": tender.get('id'),
                    "tender_title": tender.get('display_name'),
                    "matched_product": product.get('name'),
                    "matching_score": result['score'],
                    "customization_possibility": result['customization_possibility']
                }
                matches.append(match_record)

    # Output Result
    print("\n✅ Analysis Complete. Matches found:")
    print(json.dumps(matches, indent=4))
    
    # Save to file
    with open('matched_tenders.json', 'w') as f:
        json.dump(matches, f, indent=4)
    print("💾 Saved results to matched_tenders.json")

if __name__ == "__main__":
    main()
