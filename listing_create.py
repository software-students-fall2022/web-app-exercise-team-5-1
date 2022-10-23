from flask import render_template, request, redirect, url_for
from db import listings_collection
import time
import bcrypt

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
    hash = bcrypt.hashpw(form.get("password").encode('utf8'), bcrypt.gensalt())

    # Take images and convert them into binary to upload
    image_binaries = []
    if ('images' in files) and (request.files['images'].filename != ''):
        # a file was uploaded
        images = files.getlist('images')
        for image in images:
            if image.filename != '' and allowed_file(image.filename):
                image_binaries.append(image.read())
            else:
                raise ValueError("Invalid file type uploaded.")
    
    # Return database-ready listing. ValueErrors may still arise in this section.
    return {
        "timestamp": int(time.time()),
        "title": form.get("title"),
        "description": form.get("description"),
        "price": round(float(form.get("price")), 2),
        "images": image_binaries,
        "author": form.get("author"),
        "password": hash,
        "questions": []
    }

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
