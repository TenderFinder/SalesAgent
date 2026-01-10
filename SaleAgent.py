import json
import ollama

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def clean_html(text):
    """Basic cleanup if needed, though LLMs handle HTML well."""
    return text

def analyze_bulk_matches(tenders, products):
    """
    Uses Ollama to analyze matches between ALL tenders and ALL products in a single call.
    Returns a list of match objects.
    """
    
    # Prepare concise lists for the prompt
    tenders_list_str = json.dumps([{
        "id": t.get('id'),
        "title": t.get('display_name'),
        "description": t.get('description'),
        "sla": t.get('sla'),
        "tags": t.get('search_tags')
    } for t in tenders], indent=2)

    products_list_str = json.dumps([{
        "name": p.get('name'),
        "keywords": p.get('keywords'),
        "category": p.get('category')
    } for p in products], indent=2)

    prompt = f"""
    You are a Sales Engineer. Analyze the following list of Tenders and Company Products to find viable sales opportunities.
    
    AVAILABLE TENDERS:
    {tenders_list_str}
    
    COMPANY PRODUCTS:
    {products_list_str}
    
    Task:
    1. For each tender, identify if any of our products act as a solution.
    2. Only return substantial matches (Matching Score > 50).
    3. Analyze if the product needs customization.
    
    Return ONLY a JSON list of objects in this format:
    [
        {{
            "tender_id": "<id from tender list>",
            "tender_title": "<title from tender list>",
            "matched_product": "<product name>",
            "matching_score": <int 0-100>,
            "customization_possibility": "<string explanation>",
            "reasoning": "<short reasoning>"
        }}
    ]
    
    If no matches are found, return an empty list [].
    """

    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        content = response['message']['content']
        print(f"DEBUG LLM RAW: {content[:100]}...") # Debugging
        
        # Clean up markdown
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        matches = json.loads(content.strip())
        return matches
        
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return []

def main():
    print("🚀 Starting Sales Agent Analysis with Ollama (Bulk Mode)...")
    
    try:
        tenders_data = load_json('available_tenders.json')
        products_data = load_json('data/our_products.json')
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return

    tenders = tenders_data.get('services', [])
    offerings = products_data.get('offerings', [])
    
    print(f"📡 Loaded {len(tenders)} tenders and {len(offerings)} products.")
    print("🧠 Analyze matches contextually (Bulk)...")

    matches = analyze_bulk_matches(tenders, offerings)

    # Output Result
    print(f"\n✅ Analysis Complete. Found {len(matches)} matches:")
    print(json.dumps(matches, indent=4))
    
    # Save to file
    with open('matched_tenders.json', 'w') as f:
        json.dump(matches, f, indent=4)
    print("💾 Saved results to matched_tenders.json")

if __name__ == "__main__":
    main()
