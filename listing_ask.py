from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import listings_collection

def listing_ask(id):
    if request.method == "GET":
        # Request method is GET, display the form for editing and do not run below code.
        return render_template('listing_ask.html', id = id)
    try:
        # Request method is POST, process form data.
        if not ("author" in request.form and "question" in request.form):
            return render_template('error.html', message = "Author and question are both required attributes."), 400

        # Generate question in database-ready format.
        question = {
            # ObjectIds have a timestamp embedded in them, so use that instead of a timestamp.
            # Also acts as a unique identifier so that a question can be answered later.
            "_id": ObjectId(),
            "author": request.form["author"],
            "body": request.form["question"]
        }

        # Push (append) the question onto the array of questions stored in the database.
        success = listings_collection.find_one_and_update({'_id': ObjectId(id)}, {'$push': {'questions': question}})

        # If None is returned from find_one_and_update then the listing with given id does not exist in the database.
        if success is None:
            return render_template('error.html', message = "No listing found with this id."), 404

        # Otherwise the operation was successful, redirect user to the listing page for the listing they just asked a question on.
        return redirect(url_for("listing", id=id))
    except InvalidId:
        return render_template('error.html', message = "The given id is invalid."), 400
    except TypeError as te:
        return render_template('error.html', message = str(te)), 400
