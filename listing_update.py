from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from bson.errors import InvalidId
import bcrypt
from db import listings_collection

# TODO: figure out user experience of how to update multiple images

def listing_update(id):
    try:
        listing_cursor = listings_collection.find({'_id': ObjectId(id)})
        listing = listing_cursor.next()
        listing_cursor.close()

        if request.method == "GET":
            # Request method is GET, display the form for editing and do not run below code.
            return render_template('listing_update.html', listing = listing)
        
        # Check password was submitted and correct before changing the listing in any way.
        if "password" not in request.form:
            return render_template('error.html', message = "You must submit a passcode to edit this listing."), 401
        if not bcrypt.checkpw(request.form.get("password").encode('utf8'), listing["password"]):
            return render_template('error.html', message = "The provided passcode is not valid for this listing."), 401
        
        # Check value of submit button. (TODO: Maybe there is a better way to do this?)
        # Process the form based on which action the user has taken.
        if "action" not in request.form:
            return render_template('error.html', message = "No action type given with form data."), 400
        action = request.form.get("action")
        if action == "Delete Listing":
            # Delete the listing from the database and redirect to index.
            listings_collection.delete_one({'_id': ObjectId(id)})
            return redirect("/")
        elif action == "Edit Listing":
            # Otherwise edit the listing with the new form data.
            return edit_listing(id, request.form, request.files)
        else:
            # If action is not equal to one of the predefined options, raise an error.
            return render_template('error.html', message = "Invalid action type given with form data."), 400
    except StopIteration:
        return render_template('error.html', message = "No listing found with this id."), 404
    except InvalidId:
        return render_template('error.html', message = "The given id is invalid."), 400
    except TypeError as te:
        return render_template('error.html', message = str(te)), 400

def edit_listing(id, form, files):
    newlistinginfo = {}
    # Check each field and see if the form data has a value for it. If so, update the database.
    for param in ["title", "description", "author"]:
        if "author" in form:
            newlistinginfo[param] = form.get(param)
    if "price" in form:
        newlistinginfo["price"] = round(float(form.get("price")), 2)

    # Update the listing in the database and redirect to that listing page.
    listings_collection.update_one({'_id': ObjectId(id)}, {'$set': newlistinginfo})
    return redirect(url_for("listing", id=str(id)))
