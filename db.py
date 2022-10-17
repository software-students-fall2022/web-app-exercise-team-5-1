from flask_pymongo import pymongo
import configparser

def get_listings_collection():
    config = configparser.ConfigParser()
    config.read('config.ini')
    CONNECTION_STRING = config['mongodb']['CONNECTION_STRING']

    try:
        client = pymongo.MongoClient(CONNECTION_STRING)
        db = client.get_database('laigscrist')
        return pymongo.collection.Collection(db, 'listings')
    except pymongo.errors.ConnectionFailure as e:
        print("MongoDB server connection error.")
        return
    except Exception as e:
        print(e)
