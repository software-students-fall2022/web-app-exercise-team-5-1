from flask import Flask, render_template, request, redirect
from db import get_listings_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)
listings_collection = get_listings_collection()

# TODO: this file is getting a little big. we should refactor some routes into different files

@app.route('/')
def index():
    listings_cursor = listings_collection.find()
    # create simplified listing object for each listing in the db
    # @bruce - I don't love the way I implemented this (because in theory the db can be very very long)
    #          but the alternative is to rate limit/paginate. we could make a todo item for that, but this works for now
    listings = [{
        "id": str(listing["_id"]), 
        "title": listing["title"], 
        "price": listing["price"],
        "description": listing["description"],
        "author": listing["author"]
        } for listing in list(listings_cursor)]
    listings_cursor.close()
    return render_template('index.html', listings = listings)

@app.route('/newlisting')
def listing_create():
    return render_template('newlisting.html')

@app.route('/listing/<id>', methods = ["GET", "POST"])
def listing(id):
    if request.method == "GET":
        # display listing page
        try:
            listing_cursor = listings_collection.find({'_id': ObjectId(id)})
            listing = listing_cursor.next() # get the first (only) listing with the id
            listing_cursor.close()
            questions = listing["questions"]
            # TODO: add image support
            return render_template('listing.html', listing = listing, questions = questions)
        except StopIteration:
            return "No listing found with this id."
        except InvalidId:
            return "The given id is invalid."
    
    elif request.method == "POST":
        # validate listing update authentication before redirecting to editing page
        # TODO: implement listing update authetication
        # TODO: add routing for question answering
        data = request.form
        print(data)
        return redirect(f'/listing/{id}/update')

@app.route('/listing/<id>/update')
def listing_update(id):
    return render_template('listing_update.html')

@app.route('/listing/<id>/ask')
def listing_ask(id):
    return render_template('listing_ask.html')

@app.route('/listing/<id>/answer/<qid>')
def listing_answer(id, qid):
    return render_template('listing_answer.html')

if __name__ == '__main__':
    app.run(port=5000)
