from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from bson.errors import InvalidId
import bcrypt
from db import listings_collection

# TODO: a lot of this is largely the same as the update. We should pull together a util file
def listing_delete(id):
    try:
        listing_cursor = listings_collection.find({'_id': ObjectId(id)})
        listing = listing_cursor.next()
        listing_cursor.close()

        # Check password was submitted and correct before changing the listing in any way.
        if "password" not in request.form:
            return render_template('error.html', message = "You must submit a passcode to delete this listing."), 401

        if not bcrypt.checkpw(request.form.get("password").encode('utf8'), listing["password"]):
            return render_template('error.html', message = "The provided passcode is not valid for this listing."), 401

        listings_collection.delete_one({'_id': ObjectId(id)})
        return redirect("/")
    except StopIteration:
        return render_template('error.html', message = "No listing found with this id."), 404
    except InvalidId:
        return render_template('error.html', message = "The given id is invalid."), 400
    except TypeError as te:
        return render_template('error.html', message = str(te)), 400
