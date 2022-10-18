from flask import render_template, request
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import listings_collection

def listing(id):
    if request.method == "GET":
        # display listing page
        try:
            listing_cursor = listings_collection.find({'_id': ObjectId(id)})
            listing = listing_cursor.next() # get the first (only) listing with the id
            listing_cursor.close()
            questions = listing["questions"]
            # TODO: add image support
            return render_template('listing.html', listing = listing, questions = questions)
        except StopIteration:
            return "No listing found with this id."
        except InvalidId:
            return "The given id is invalid."
