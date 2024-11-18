from flask.views import MethodView
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, current_app
from sqlalchemy import desc

from schemas.recipe import RecipeSchema
from models.recipe import RecipeModel

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

blp = Blueprint("categories", __name__, description="Operations on recipes")


@blp.route("/category/<string:category>")
class GetRecipeCategory(MethodView):
    @blp.response(200, recipes_schema)
    def get(self, category):
        recipes = RecipeModel.query.filter_by(country=category).all()
        serialized_recipes = recipes_schema.dump(recipes)
        return jsonify(serialized_recipes), 200
