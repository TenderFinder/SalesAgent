from config import API_URL, MONGO_URI, DB_NAME, COLLECTION_NAME
from api_client import fetch_data
from mongo_client import save_to_mongodb

def main():
    print("🚀 Starting GEM API → MongoDB pipeline")

    data = fetch_data(API_URL)

    if data:
        save_to_mongodb(data, MONGO_URI, DB_NAME, COLLECTION_NAME)
    else:
        print("⚠️ No data to store")

if __name__ == "__main__":
    main()
