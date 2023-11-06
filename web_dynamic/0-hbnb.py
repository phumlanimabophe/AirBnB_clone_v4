#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, render_template, url_for
from models import storage
import uuid

# Flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
server_host = '0.0.0.0'

# Teardown app context
@app.teardown_appcontext
def teardown_database_session(exception):
    """
    After each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()

# Route for rendering the HTML page
@app.route('/0-hbnb/')
def render_hbnb_page(the_id=None):
    """
    Handles requests to a custom template with states, cities, and amenities
    """
    state_objects = storage.all('State').values()
    states_data = dict([state.name, state] for state in state_objects)
    amenities_data = storage.all('Amenity').values()
    places_data = storage.all('Place').values()
    users_data = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                      for user in storage.all('User').values())
    cache_id = uuid.uuid4()
    return render_template('0-hbnb.html',
                           states=states_data,
                           amens=amenities_data,
                           places=places_data,
                           users=users_data,
                           cache_id=cache_id)

if __name__ == "__main__":
    """
    Main Flask App
    """
    app.run(host=server_host, port=port)
