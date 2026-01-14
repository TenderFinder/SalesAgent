from pymongo import MongoClient

def save_to_mongodb(data, mongo_uri, db_name, collection_name):
    print("🗄️ Connecting to MongoDB...")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # If data is a list → insert many
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print("✅ Data saved to MongoDB successfully")
