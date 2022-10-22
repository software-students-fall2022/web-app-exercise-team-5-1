from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import listings_collection
import utils

def listing_answer(id, qid):
    try:
        listing = utils.get_listing_by_id(id)

        if request.method == "GET":
            # Request method is GET, display the form for editing and do not run below code.
            return render_template('listing_answer.html', listing = listing, qid = qid)
        
        if not utils.check_listing_password(request.form, listing):
            return render_template('error.html', message = "The provided passcode is not valid for this listing."), 401

        if "answer" not in request.form or request.form["answer"] == "":
            return render_template('error.html', message = "You must provide an answer to the question."), 400
        
        answer = {
            "_id": ObjectId(),
            "body": request.form["answer"]
        }

        # Update the listing in the database and redirect to that listing page.
        listings_collection.update_one({'_id': ObjectId(id)}, {'$set': {f"questions.{qid}.answer": answer}})
        return redirect(url_for("listing", id=id))

    except StopIteration:
        return render_template('error.html', message = "No listing found with this id."), 404
    except InvalidId:
        return render_template('error.html', message = "The given id is invalid."), 400
    except TypeError as te:
        return render_template('error.html', message = str(te)), 400
