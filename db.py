from flask_pymongo import pymongo
from dotenv import dotenv_values

def get_listings_collection():
    config = dotenv_values(".env")
    CONNECTION_STRING = config["MONGODB_URI"]
    try:
        client = pymongo.MongoClient(CONNECTION_STRING)
        db = client.get_database('laigscrist')
        return pymongo.collection.Collection(db, 'listings')
    except pymongo.errors.ConnectionFailure as e:
        print("MongoDB server connection error.")
    except Exception as e:
        print(e)

listings_collection = get_listings_collection()
