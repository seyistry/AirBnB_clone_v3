#!/usr/bin/python3
"""
This module contains endpoint(route) Place
"""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places():
    """get all places"""
    result = [obj.to_dict() for obj in storage.all(Place).values()]
    return jsonify(result)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """retrieve user by id """
    user = storage.get(Place, place_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    """delete user by id """
    user = storage.get(Place, place_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places', methods=['POST'],
                 strict_slashes=False)
def create_place_id():
    """create new user """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(
            jsonify({"error": "Missing user_id"}), 400)
    kwarg = request.get_json()
    user_obj = Place(**kwarg)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place_id(place_id):
    """ update methods """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_obj = storage.get(Place, place_id)
    if user_obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(user_obj, key, value)
    storage.save()
    return jsonify(user_obj.to_dict())
