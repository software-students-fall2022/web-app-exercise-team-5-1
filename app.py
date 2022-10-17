from flask import Flask, render_template
from db import get_listings_collection

app = Flask(__name__)
listings = get_listings_collection()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/newlisting')
def listing_create():
    return render_template('newlisting.html')

@app.route('/listing/<id>')
def listing(id):
    return render_template('listing.html')

@app.route('/listing/<id>/update')
def listing_update(id):
    return render_template('listing_update.html')

@app.route('/listing/<id>/ask')
def listing_ask(id):
    return render_template('listing_ask.html')

@app.route('/listing/<id>/answer/<qid>')
def listing_answer(id, qid):
    return render_template('listing_answer.html')

#test to insert data to the data base
@app.route("/api/db_test")
def test():
    listings.insert_one({"title": "A thing I want to sell", "description": "I want to sell this"})
    return "Conection is ok"

if __name__ == '__main__':
    app.run(port=3000)
