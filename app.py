import os

from flask import Flask, jsonify
from flask_smorest import Api
from dotenv import load_dotenv
from db import db
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


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
    Migrate(app, db)

    CORS(app)

    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = "Mau Masak Ya Masakin"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 36000  #  Expires in 10 hours
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 2592000  #  Expires in 30 days

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

    api = Api(app)

    return app
