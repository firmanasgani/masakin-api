from datetime import datetime, timezone, timedelta
from db import db
from models.tool import ToolModel
from app import create_app
import random

def generate_tool_data():
    base_tools = [
        {"nama_alat": "Mixing Bowl"},
        {"nama_alat": "Whisk"},
        {"nama_alat": "Spatula"},
        {"nama_alat": "Frying Pan"},
        {"nama_alat": "Oven"},
        {"nama_alat": "Blender"},
        {"nama_alat": "Knife"},
        {"nama_alat": "Cutting Board"},
        {"nama_alat": "Rolling Pin"},
        {"nama_alat": "Measuring Cup"}
    ]

    tools = []
    for i in range(1000):
        base = random.choice(base_tools)
        tools.append({
            "recipe_id": str(random.randint(1, 50)),  # Assuming you have 50 recipes
            "nama_alat": f"{base['nama_alat']} Variant {i+1}",
            "created_at": datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30)),
            "updated_at": None
        })
    return tools

def seed_data():
    """Seed the database with sample tools."""
    app = create_app()
    tools = generate_tool_data()
    with app.app_context():
        print("Seeding tool data...")
        for tool in tools:
            existing_tool = ToolModel.query.filter_by(
                recipe_id=tool["recipe_id"],
                nama_alat=tool["nama_alat"]
            ).first()
            if not existing_tool:
                print(f"Adding tool: {tool['nama_alat']} for Recipe ID {tool['recipe_id']}")
                new_tool = ToolModel(**tool)
                db.session.add(new_tool)
        
        db.session.commit()
        print("Database seeded with sample tools.")

if __name__ == "__main__":
    seed_data()
