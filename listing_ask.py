from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from bson.errors import InvalidId
import time
from db import listings_collection

def listing_ask(id):
    if request.method != "POST":
        # Request method is GET, display the form for editing and do not run below code.
        return render_template('listing_ask.html')
    try:
        # Request method is POST, process form data.
        if not ("author" in request.form and "question" in request.form):
            return render_template('error.html', message = "Author and question are both required attributes."), 400

        # Not actually using this data, but will throw an error if selected question does not exist in the database.
        # We don't want to be adding questions for nonexistent listings, since I think MongoDB would allow it.
        # There's probably a better way to do this but this is the best I could think of for now.
        listing_cursor = listings_collection.find({'_id': ObjectId(id)})
        listing_cursor.next()
        listing_cursor.close()
        
        # Generate question in database-ready format.
        question = {
            "timestamp": int(time.time()),
            "author": request.form["author"],
            "body": request.form["question"]
        }

        # Push (append) the question onto the array of questions stored in the database.
        listings_collection.update_one({'_id': ObjectId(id)}, {'$push': {'questions': question}})

        # Redirect user to the listing page for the listing they just asked a question on.
        return redirect(url_for("listing", id=str(id)))
    except StopIteration:
        return render_template('error.html', message = "No listing found with this id."), 404
    except InvalidId:
        return render_template('error.html', message = "The given id is invalid."), 400
    except TypeError as te:
        return render_template('error.html', message = str(te)), 400
