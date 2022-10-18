from flask import render_template, request
import pymongo
from db import listings_collection

LISTINGS_PER_PAGE = 1 # for testing, probably will be 20 or something in prod

def index():
    try:
        page_number = int(request.args["page_number"]) if "page_number" in request.args.keys() else 1
        listings_cursor = listings_collection.find({}, ["title", "price", "description", "author"]) \
                                             .sort("timestamp", pymongo.DESCENDING) \
                                             .skip((page_number - 1) * LISTINGS_PER_PAGE) \
                                             .limit(LISTINGS_PER_PAGE)
    except ValueError:
        return render_template('error.html', message = "Bad page number query")
    
    listings = list(listings_cursor.sort("timestamp", pymongo.DESCENDING))
    listings_cursor.close()

    if len(listings) == 0:
        # there are no listings at this page number
        return render_template('error.html', message = "No listings at this page query")

    # check if there are any more listings after this page
    next_listings_cursor = listings_collection.find({}, ["_id"]) \
                                               .sort("timestamp", pymongo.DESCENDING) \
                                               .skip(page_number * LISTINGS_PER_PAGE) \
                                               .limit(1)
    prev_page = page_number - 1
    next_page = page_number + 1 if len(list(next_listings_cursor)) != 0 else -1 
    # next page is -1 if there is no next page

    return render_template('index.html', listings = listings, prev_page = prev_page, next_page = next_page)
