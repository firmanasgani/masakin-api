from flask_smorest import Blueprint, abort
from flask import request
from models.recipe import RecipeModel
from schemas.recipe import RecipeSchema
from http import HTTPStatus
from response.response_builder import build_paginated_response, build_single_item_response

blp = Blueprint("recipes", __name__, description="Operations on recipes")

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

# Constants
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

@blp.route("/recipes", methods=["GET"])
def get_all_recipes():
    """
    Fetch all recipes with pagination, filtering, and sorting capabilities.
    """
    try:
        # Query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', DEFAULT_PAGE_SIZE)), MAX_PAGE_SIZE)
        country = request.args.get('country')
        difficulty = request.args.get('difficulty', type=int)
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc').lower()
        name = request.args.get('name')

        # Validations
        if page < 1:
            abort(HTTPStatus.BAD_REQUEST, message="Page number must be greater than 0")
        valid_sort_fields = {'created_at', 'name', 'difficulty'}
        if sort_by not in valid_sort_fields:
            abort(HTTPStatus.BAD_REQUEST, message=f"Invalid sort field. Valid options are: {', '.join(valid_sort_fields)}")
        if order not in {'asc', 'desc'}:
            abort(HTTPStatus.BAD_REQUEST, message="Invalid order. Use 'asc' or 'desc'")
     
        # Query construction
        query = RecipeModel.query
        if country:
            query = query.filter(RecipeModel.country == country)
        if difficulty:
            query = query.filter(RecipeModel.difficulty == difficulty)
        if name:
            query = query.filter(RecipeModel.name.ilike(f"%{name}%"))

        sort_column = getattr(RecipeModel, sort_by)
        query = query.order_by(sort_column.desc() if order == 'desc' else sort_column.asc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=True)

        # Build paginated response
        return build_paginated_response(
            pagination=pagination,
            page=page,
            per_page=per_page,
            endpoint='recipes.get_all_recipes',
            schema=recipes_schema,
            country=country,
            difficulty=difficulty,
            sort_by=sort_by,
            order=order
        )
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, message="Invalid parameter value")
    except Exception:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="An unexpected error occurred")


@blp.route("/recipes/<string:recipe_id>", methods=["GET"])
def get_recipe_by_id(recipe_id):
    """Fetch a recipe by ID, including its ingredients."""
    try:
        recipe = RecipeModel.query.get(recipe_id)
        if not recipe:
            abort(HTTPStatus.NOT_FOUND, message=f"Recipe with ID {recipe_id} not found")

        # Build single item response
        return build_single_item_response(
            item=recipe,
            endpoint='recipes.get_recipe_by_id',
            schema=recipe_schema, 
            recipe_id=recipe_id
        )
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=f"An unexpected error occurred: {str(e)}")