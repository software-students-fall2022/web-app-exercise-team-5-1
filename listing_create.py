from flask import render_template, request, redirect, url_for
from db import listings_collection
import time
import bcrypt

def listing_create():
    if request.method == "POST":
        # If request method is POST process submitted form data.
        try:
            # If no errors, add listing to database and redirect to new listing page.
            listing = listing_object_from_params(request.form, request.files)
            result = listings_collection.insert_one(listing)
            return redirect(url_for("listing", id=str(result.inserted_id)))
        except ValueError as ve:
            # Return any raised validation errors and send 400 code.
            return str(ve), 400
        except Exception as e:
            # Any other uncaught errors at this point will get a 500 code.
            return str(e), 500
    else:
        # Otherwise, request method was GET so load the form.
        return render_template('listing_create.html')

def listing_object_from_params(form, files):
    # Check that all required attributes are present in the request.
    reqs = ["title", "description", "price", "author", "password"]
    for req in reqs:
        if req not in form:
            raise ValueError(f"\"{req}\" attribute must be present.")

    # Handle hashing and salting of provided password.
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(form.get("password").encode('utf8'), salt)
    
    # Return database-ready listing. ValueErrors may still arise in this section.
    return {
        "timestamp": int(time.time()),
        "title": form.get("title"),
        "description": form.get("description"),
        "price": round(float(form.get("price")), 2),
        "images": [], # TODO: Handle images.
        "author": form.get("author"),
        "password": {
            "hash": hash,
            "salt": salt,
        },
        "questions": []
    }
