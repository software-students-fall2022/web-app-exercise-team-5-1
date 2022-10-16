from flask import Flask, render_template
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
def listing_ask(id, qid):
    return render_template('listing_answer.html')



if __name__ == '__main__':
    app.run()
