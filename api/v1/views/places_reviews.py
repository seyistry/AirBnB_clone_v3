#!/usr/bin/python3
"""
This module contains endpoint(route) status
"""
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """get reviews by place id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get reviews by review id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete review by review id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create review in place """
    place = storage.get(Place, place_id)
    user = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    kwargs = request.get_json()
    kwargs['place_id'] = place_id
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    review_obj = Review(**kwargs)
    review_obj.place_id = place.id
    review_obj.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """update review in place """
    review_obj = storage.get(Review, review_id)
    if review_obj is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict())
