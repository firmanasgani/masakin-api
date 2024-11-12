from flask_smorest import Blueprint, abort
from flask import request
from models.tool import ToolModel
from schemas.tool import ToolSchema
from http import HTTPStatus
from response.response_builder import build_single_item_response, build_paginated_response, build_non_paginated_response

blp = Blueprint("tools", __name__, description="Operations on tools")

tool_schema = ToolSchema()
tools_schema = ToolSchema(many=True)

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

@blp.route("/recipes/<int:recipe_id>/tools", methods=["GET"])
def get_tools_by_recipe(recipe_id):
    """Fetch all tools for a specific recipe, with optional pagination."""
    try:
        page = request.args.get('page')
        per_page = request.args.get('per_page')

        query = ToolModel.query.filter_by(recipe_id=recipe_id)

        if page and per_page:
            page = int(page)
            per_page = min(int(per_page), MAX_PAGE_SIZE)

            if page < 1:
                abort(HTTPStatus.BAD_REQUEST, message="Page number must be greater than 0")

            pagination = query.paginate(page=page, per_page=per_page, error_out=True)
            return build_paginated_response(
                pagination=pagination,
                page=page,
                per_page=per_page,
                endpoint='tools.get_tools_by_recipe',
                schema=tools_schema,
                recipe_id=recipe_id
            )
        else:
            tools = query.all()
            return build_non_paginated_response(
                items=tools,
                endpoint='tools.get_tools_by_recipe',
                schema=tools_schema,
                recipe_id=recipe_id
            )

    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, message="Invalid parameter value")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))

@blp.route("/recipes/<int:recipe_id>/tools/<int:tool_id>", methods=["GET"])
def get_tool_by_id(recipe_id, tool_id):
    """Fetch a specific tool by its ID for a given recipe."""
    try:
        tool = ToolModel.query.filter_by(recipe_id=recipe_id, id=tool_id).first()
        if not tool:
            abort(HTTPStatus.NOT_FOUND, message=f"Tool with ID {tool_id} for Recipe ID {recipe_id} not found")

        return build_single_item_response(
            item=tool,
            endpoint='tools.get_tool_by_id',
            schema=tool_schema,
            recipe_id=recipe_id,
            tool_id=tool_id
        )
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
