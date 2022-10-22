from flask import render_template, request, redirect
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import listings_collection
import utils

def listing_delete(id):
    try:
        listing = utils.get_listing_by_id(id)

        if not utils.check_listing_password(request.form, listing):
            return render_template('error.html', message = "The provided passcode is not valid for this listing."), 401

        listings_collection.delete_one({'_id': ObjectId(id)})
        return redirect("/")
    except StopIteration:
        return render_template('error.html', message = "No listing found with this id."), 404
    except InvalidId:
        return render_template('error.html', message = "The given id is invalid."), 400
    except TypeError as te:
        return render_template('error.html', message = str(te)), 400
