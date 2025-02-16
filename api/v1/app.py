#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
from flask import make_response
from flask_cors import CORS
from os import environ


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    """ Main function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
