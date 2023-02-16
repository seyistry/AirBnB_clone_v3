#!/usr/bin/python3
"""
This module contains endpoint(route) users
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """get all users"""
    result = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(result)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """retrieve user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_id(user_id):
    """delete user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user_id():
    """create new user """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js = request.get_json()
    user_obj = User(**js)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user_id(user_id):
    """ update methods """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at']:
            setattr(user_obj, key, value)
    storage.save()
    return jsonify(user_obj.to_dict())
