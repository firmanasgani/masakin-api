from flask import Blueprint,request, jsonify
from models.howtocook import HowToCook

howtocook_bp = Blueprint("howtocook", __name__)

@howtocook_bp.route("/recipes/<int:recipe_id>/howtocook", methods=["GET"])
def get_steps(recipe_id):
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    search_query = request.args.get("search", default="", type=str)

    query = HowToCook.query.filter(HowToCook.recipe_id == recipe_id)
    if search_query:
        query = query.filter(HowToCook.description.ilike(f"%{search_query}%"))

    total_steps = query.count()
    steps = query.order_by(HowToCook.steps).paginate(page=page, per_page=limit, error_out=False)

    if not steps.items:
        return jsonify({"error": "No steps found for this recipe"}), 404

    result = [
        {
            "id": step.id,
            "steps": step.steps,
            "description": step.description,
            "img_urls": step.img_urls
        }
        for step in steps.items
    ]

    response = {
        "total_steps": total_steps,
        "page": page,
        "limit": limit,
        "steps": result
    }

    return jsonify(response), 200
