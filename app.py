from flask import Flask

# Import page view methods from other files.
from index import index
from listing_create import listing_create
from listing import listing
from listing_update import listing_update
from listing_ask import listing_ask
from listing_answer import listing_answer

# Create new Flask app.
app = Flask(__name__)

# Instead of using annotations, link routes to methods in other files.
app.add_url_rule('/', view_func=index)
app.add_url_rule('/listing/create', methods=["GET", "POST"], view_func=listing_create)
app.add_url_rule('/listing/<id>', methods=["GET", "POST"], view_func=listing)
app.add_url_rule('/listing/<id>/update', methods=["GET", "POST"], view_func=listing_update)
app.add_url_rule('/listing/<id>/ask', methods=["GET", "POST"], view_func=listing_ask)
app.add_url_rule('/listing/<id>/answer', view_func=listing_answer)

# Run the app.
if __name__ == '__main__':
    # Host 0.0.0.0 will allow you to access the web server from other computers (i.e. a phone) connected to your local network.
    app.run(host='0.0.0.0', port=5000)
