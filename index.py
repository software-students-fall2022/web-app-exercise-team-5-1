from flask import render_template
import pymongo
from db import listings_collection

def index():
    listings_cursor = listings_collection.find()
    # create simplified listing object for each listing in the db
    # @bruce - I don't love the way I implemented this (because in theory the db can be very very long)
    #          but the alternative is to rate limit/paginate. we could make a todo item for that, but this works for now
    listings = [{ # TODO: implement a projection instead
        "id": str(listing["_id"]), 
        "title": listing["title"], 
        "price": listing["price"],
        "description": listing["description"],
        "author": listing["author"]
        } for listing in list(listings_cursor.sort("timestamp", pymongo.DESCENDING))]
    listings_cursor.close()
    return render_template('index.html', listings = listings)
