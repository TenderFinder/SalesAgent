import requests

def fetch_data(api_url):
    print("📡 Fetching data from API...")

    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Failed to fetch data")
        return None
