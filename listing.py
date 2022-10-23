from flask import render_template, request
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import listings_collection
from base64 import b64encode

def listing(id):
    if request.method == "GET":
        # display listing page
        try:
            listing_cursor = listings_collection.find({'_id': ObjectId(id)})
            listing = listing_cursor.next() # get the first (only) listing with the id
            listing_cursor.close()
            questions = listing["questions"]

            # decode image binaries
            images = listing["images"]
            for idx in range(len(images)):
                images[idx] = b64encode(images[idx]).decode("utf-8")
            
            return render_template('listing.html', listing = listing, questions = questions, images = images)
        except StopIteration:
            # cursor.next did not find anything
            # no listing with the id was found
            return "No listing found with this id."
        except InvalidId:
            return "The given id is invalid."
