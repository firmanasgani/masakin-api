from flask_smorest import Blueprint, abort
from flask import request
from models.ingredient import IngredientModel
from schemas.ingredient import IngredientSchema
from http import HTTPStatus
from response.response_builder import build_single_item_response, build_paginated_response, build_non_paginated_response

blp = Blueprint("ingredients", __name__, description="Operations on ingredients")

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

@blp.route("/recipes/<int:recipe_id>/ingredients", methods=["GET"])
def get_ingredients_by_recipe(recipe_id):
    """Fetch all ingredients for a specific recipe, with optional pagination."""
    try:
        # Check if pagination parameters are provided
        page = request.args.get('page')
        per_page = request.args.get('per_page')

        query = IngredientModel.query.filter_by(recipe_id=recipe_id)

        if page and per_page:
            # Validate and apply pagination
            page = int(page)
            per_page = min(int(per_page), MAX_PAGE_SIZE)

            if page < 1:
                abort(HTTPStatus.BAD_REQUEST, message="Page number must be greater than 0")

            pagination = query.paginate(page=page, per_page=per_page, error_out=True)
            return build_paginated_response(
                pagination=pagination,
                page=page,
                per_page=per_page,
                endpoint='ingredients.get_ingredients_by_recipe',
                schema=ingredients_schema,
                recipe_id=recipe_id
            )
        else:
            # No pagination, return all ingredients for the recipe
            ingredients = query.all()
            return build_non_paginated_response(
                items=ingredients,
                endpoint='ingredients.get_ingredients_by_recipe',
                schema=ingredients_schema,
                recipe_id=recipe_id
            )

    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, message="Invalid parameter value")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))

@blp.route("/recipes/<int:recipe_id>/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient_by_id(recipe_id, ingredient_id):
    """Fetch a specific ingredient by its ID for a given recipe."""
    try:
        ingredient = IngredientModel.query.filter_by(recipe_id=recipe_id, id=ingredient_id).first()
        if not ingredient:
            abort(HTTPStatus.NOT_FOUND, message=f"Ingredient with ID {ingredient_id} for Recipe ID {recipe_id} not found")

        return build_single_item_response(
            item=ingredient,
            endpoint='ingredients.get_ingredient_by_id',
            schema=ingredient_schema,
            recipe_id=recipe_id,
            ingredient_id=ingredient_id
        )
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
