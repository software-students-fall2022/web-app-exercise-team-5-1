from flask import render_template, request, redirect, url_for
from bson.objectid import ObjectId
from bson.errors import InvalidId
from db import listings_collection
import utils

def listing_update(id):
    try:
        listing = utils.get_listing_by_id(id)

        if request.method == "GET":
            # Request method is GET, display the form for editing and do not run below code.
            return render_template('listing_update.html', listing = listing)
        
        if not utils.check_listing_password(request.form, listing):
            return render_template('error.html', message = "The provided passcode is not valid for this listing."), 401
        
        newlistinginfo = {}
        # Check each field and see if the form data has a value for it. If so, update the database.
        for param in ["title", "description", "author"]:
            if "author" in request.form:
                newlistinginfo[param] = request.form.get(param)
        if "price" in request.form:
            newlistinginfo["price"] = round(float(request.form.get("price")), 2)

        # if the user wants no change in image, upload nothing
        # otherwise, they will have to reupload the entire set of images they want
        if ('images' in request.files) and (request.files['images'].filename != ''):
            # a file was uploaded
            image_binaries = []
            images = request.files.getlist('images')

            for image in images:
                if utils.is_file_image(image.filename):
                    image_binaries.append(image.read())
                else:
                    return render_template("error.html", message="Invalid file type uploaded.")
            newlistinginfo["images"] = image_binaries

        # Update the listing in the database and redirect to that listing page.
        listings_collection.update_one({'_id': ObjectId(id)}, {'$set': newlistinginfo})
        return redirect(url_for("listing", id=id))

    except StopIteration:
        return render_template('error.html', message = "No listing found with this id."), 404
    except InvalidId:
        return render_template('error.html', message = "The given id is invalid."), 400
    except TypeError as te:
        return render_template('error.html', message = str(te)), 400
