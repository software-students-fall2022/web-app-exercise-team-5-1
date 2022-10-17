from flask import Flask, render_template
from db import db

app = Flask(__name__)

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
    db.collection.insert_one({"name": "John"})
    return "Connected to the database!"

if __name__ == '__main__':
    app.run(port=3000)
