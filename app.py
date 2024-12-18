import os

from flask import Flask, jsonify
from flask_smorest import Api
from dotenv import load_dotenv
from db import db
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from controllers.recipes_controller import blp as RecipeBlueprint
from controllers.ingredients_controller import blp as IngredientBlueprint
from controllers.tools_controller import blp as ToolBlueprint
from controllers.howto_controller import howtocook_bp
from controllers.users_controller import users_routes

from models.category import CategoryModel
from models.recipe import RecipeModel
from models.recipe import RecipeModel
from models.ingredient import IngredientModel
from models.ingredient_group import IngredientGroupModel
from models.howtocook import HowToCook
from models.users import UserModel
from models.rating import RatingModel
from models.how_to_cook_image import HowToCookImage

migrate = Migrate()


def create_app(is_test=False):
    app = Flask(__name__)
    load_dotenv()

    app.config.update(
        API_TITLE="Masakin",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.2",
        OPENAPI_SWAGGER_UI_PATH="/swagger",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        OPENAPI_URL_PREFIX="/",
        SQLALCHEMY_ECHO=True,
        DEBUG=True,
    )

    if is_test is True:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URI", "sqlite:///data.db"
        )

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)

    app.register_blueprint(users_routes)

    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", "default-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 36000))
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = int(
        os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000))

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(expired_token, jwt_data):
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(_):
        return jsonify({"message": "Invalid token"}), 400

    @jwt.unauthorized_loader
    def unauthorized_callback(_):
        return jsonify({"message": "Unauthorized access"}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(_):
        return jsonify({"message": "Fresh token required"}), 401

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return UserModel.query.filter_by(id=identity).one_or_none()

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user['user_id']

    api = Api(app)
    api.register_blueprint(RecipeBlueprint)
    api.register_blueprint(IngredientBlueprint)
    api.register_blueprint(ToolBlueprint)
    api.register_blueprint(howtocook_bp)

    return app
