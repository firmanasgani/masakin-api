from flask_smorest import Blueprint, abort
from flask import request
from models.rating import RatingModel
from schemas.rating import RatingSchema, AddRatingSchema
from http import HTTPStatus
from response.response_builder import build_single_item_response, build_non_paginated_response
from sqlalchemy.exc import SQLAlchemyError
from controllers.users_controller import s

blp = Blueprint("ratings", __name__, description="Operations on ratings")

rating_schema = RatingSchema()
add_rating_schema = AddRatingSchema()

@blp.route("/recipes/<int:recipe_id>/ratings", methods=["GET"])
def get_average_rating(recipe_id):
    """Fetch the average rating for a specific recipe."""
    try:
        query = RatingModel.query.filter_by(recipe_id=recipe_id)
        ratings = query.all()

        if not ratings:
            abort(HTTPStatus.NOT_FOUND, message=f"No ratings found for Recipe ID {recipe_id}")

        # Calculate average rating
        total_rating = sum(rating.rating_value for rating in ratings)
        average_rating = total_rating / len(ratings)

        return {
            "recipe_id": recipe_id,
            "average_rating": average_rating,
            "total_ratings": len(ratings)
        }, HTTPStatus.OK

    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))

@blp.route("/recipes/<int:recipe_id>/ratings", methods=["POST"])
def add_rating(recipe_id):
    """Add a rating for a specific recipe."""
    try:
        rating_data = request.get_json()
        validated_data = add_rating_schema.load(rating_data)

        # Check if rating value is valid
        rating_value = validated_data['rating_value']
        if not 1 <= rating_value <= 5:
            abort(HTTPStatus.BAD_REQUEST, message="Rating value must be between 1 and 5")

        new_rating = RatingModel(
            users_id=validated_data['users_id'],
            recipe_id=recipe_id,
            rating_value=rating_value
        )

        s.session.add(new_rating)
        s.session.commit()

        return build_single_item_response(
            item=new_rating,
            endpoint='ratings.add_rating',
            schema=rating_schema,
            recipe_id=recipe_id
        )

    except SQLAlchemyError as e:
        s.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"Database error: {str(e)}")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
