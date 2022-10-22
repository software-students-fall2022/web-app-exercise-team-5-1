from db import listings_collection
from bson.objectid import ObjectId
import bcrypt

def get_listing_by_id(id):
    listing_cursor = listings_collection.find({'_id': ObjectId(id)})
    listing = listing_cursor.next() # get the first (only) listing with the id
    listing_cursor.close()
    return listing

def check_listing_password(form, listing):
    return "password" in form and bcrypt.checkpw(form["password"].encode('utf8'), listing["password"].encode('utf8'))

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

def is_file_image(filename):
    return filename != '' and '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
