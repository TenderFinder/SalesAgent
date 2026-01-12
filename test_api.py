#!/usr/bin/env python3
"""
Test FastAPI Endpoints

Tests the API by calling endpoints and showing results.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_api():
    """Test the FastAPI endpoints."""
    print("🧪 Testing SalesAgent FastAPI")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n📡 Step 1: Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 2: Get API status
    print("\n📡 Step 2: Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Service: {data.get('service')}")
    print(f"   Version: {data.get('version')}")
    
    # Test 3: Run matching (rule-based)
    print("\n🔍 Step 3: Running rule-based matching via API...")
    response = requests.post(
        f"{BASE_URL}/api/v1/match",
        json={
            "use_ai": True,
            "min_score": 1.0,
            "save_results": False  # Don't save to DB for now
        }
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Success: {result['message']}")
        print(f"   📊 Total matches: {result['total_matches']}")
        
        if result['matches']:
            print(f"\n   Top 3 Matches:")
            for i, match in enumerate(result['matches'][:3], 1):
                print(f"   {i}. {match['tender_name']}")
                print(f"      → Product: {match['matched_product']}")
                print(f"      → Score: {match['score']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 4: Get statistics
    print("\n📈 Step 4: Getting statistics...")
    response = requests.get(f"{BASE_URL}/api/v1/stats")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"   Total matches in DB: {stats.get('total_matches', 0)}")
    else:
        print(f"   Note: {response.json().get('detail', 'No stats available')}")
    
    print("\n" + "=" * 60)
    print("✅ API TEST COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    test_api()
