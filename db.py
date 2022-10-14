from flask import Flask
from flask_pymongo import pymongo
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

CONNECTION_STRING = config['mongodb']['CONNECTION_STRING']
client = pymongo.MongoClient(CONNECTION_STRING)

db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')
