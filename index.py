from flask import render_template, request
import pymongo
from db import listings_collection
from base64 import b64encode

LISTINGS_PER_PAGE = 5 # for testing, probably will be 20 or something in prod

def index():
    try:
        page = int(request.args["page"]) if "page" in request.args.keys() else 1
        listings_cursor = listings_collection.find({}, ["title", "price", "description", "author", "images"]) \
                                             .sort("timestamp", pymongo.DESCENDING) \
                                             .skip((page - 1) * LISTINGS_PER_PAGE) \
                                             .limit(LISTINGS_PER_PAGE + 1)
    except ValueError:
        return render_template('error.html', message = "Bad page query."), 404
    
    listings = list(listings_cursor)
    for listing in listings:
        if len(listing["images"]) > 0:
            listing["image"] = b64encode(listing["images"][0]).decode("utf-8")

    listings_cursor.close()

    num_listings = len(listings)

    if num_listings == 0:
        # there are no listings at this page number
        return render_template('error.html', message = "No listings at this page query")

    del listings[LISTINGS_PER_PAGE:]
    next_page = page + 1 if num_listings > LISTINGS_PER_PAGE else -1
    return render_template('index.html', listings = listings, prev_page = page - 1, next_page = next_page)
