from datetime import datetime, timezone, timedelta
from db import db
from models.ingredient import IngredientModel
from app import create_app
import random

def generate_ingredient_data():
    base_ingredients = [
        {"nama_bahan": "Sugar", "takaran": "2 tbsp"},
        {"nama_bahan": "Salt", "takaran": "1 tsp"},
        {"nama_bahan": "Flour", "takaran": "500 g"},
        {"nama_bahan": "Egg", "takaran": "3 pcs"},
        {"nama_bahan": "Milk", "takaran": "1 cup"},
        {"nama_bahan": "Butter", "takaran": "100 g"},
        {"nama_bahan": "Chicken Breast", "takaran": "250 g"},
        {"nama_bahan": "Garlic", "takaran": "2 cloves"},
        {"nama_bahan": "Onion", "takaran": "1 large"},
        {"nama_bahan": "Olive Oil", "takaran": "3 tbsp"}
    ]

    ingredients = []
    for i in range(100):
        base = random.choice(base_ingredients)
        ingredients.append({
            "recipe_id": random.randint(1, 50),  # Assuming you have 50 recipes
            "nama_bahan": f"{base['nama_bahan']} Variant {i+1}",
            "takaran": base["takaran"],
            "created_at": datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30)),
            "updated_at": None
        })
    return ingredients

def seed_data():
    """Seed the database with sample ingredients."""
    app = create_app()
    ingredients = generate_ingredient_data()
    with app.app_context():
        print("Seeding ingredient data...")
        for ingredient in ingredients:
            existing_ingredient = IngredientModel.query.filter_by(
                recipe_id=ingredient["recipe_id"],
                nama_bahan=ingredient["nama_bahan"]
            ).first()
            if not existing_ingredient:
                print(f"Adding ingredient: {ingredient['nama_bahan']} for Recipe ID {ingredient['recipe_id']}")
                new_ingredient = IngredientModel(**ingredient)
                db.session.add(new_ingredient)
        
        db.session.commit()
        print("Database seeded with sample ingredients.")

if __name__ == "__main__":
    seed_data()
