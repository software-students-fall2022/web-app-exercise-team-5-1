# adapted from https://medium.com/@summerxialinqiao/connect-flask-app-to-mongodb-atlas-using-pymongo-328e119a7bd8

from flask import Flask
from db import db

app = Flask(__name__)

@app.route('/')
def flask_mongodb_atlas():
    return "flask mongodb atlas!"

#test to insert data to the data base
@app.route("/test")
def test():
    db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"

if __name__ == '__main__':
    app.run(port=8000)
