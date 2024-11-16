from datetime import datetime, timezone, timedelta
from db import db
from models.recipe import RecipeModel
from models.ingredient import IngredientModel
from models.ingredient_group import IngredientGroupModel
from app import create_app
import random


def generate_ingredient_group_data(recipe_id):
    base_groups = [
        {"group_name": "Bahan Utama"}, 
        {"group_name": "Bumbu Dasar"}, 
        {"group_name": "Marinasi Bulgogi"}, 
        {"group_name": "Pelengkap"}, 
        {"group_name": "Saus dan Topping"}, 
        {"group_name": "Bumbu Tumis"}, 
        {"group_name": "Kuah atau Kaldu"}, 
        {"group_name": "Adonan"}, 
        {"group_name": "Isian"}, 
        {"group_name": "Pemanis"}, 
        {"group_name": "Pengental"}, 
        {"group_name": "Bahan Fermentasi"}, 
        {"group_name": "Bumbu Rendaman"}, 
        {"group_name": "Penambah Tekstur"}, 
        {"group_name": "Bahan Garnish"}, 
    ]
    
    groups = []
    for group in base_groups:
        groups.append({
            "recipe_id": recipe_id,
            "group_name": group["group_name"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": None
        })
    return groups


def generate_ingredient_data(group_id):
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
    for i in range(5):  # Assign 5 random ingredients per group
        base = random.choice(base_ingredients)
        ingredients.append({
            "ingredient_group_id": group_id,
            "nama_bahan": f"{base['nama_bahan']} Variant {i+1}",
            "takaran": base["takaran"],
            "created_at": datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30)),
            "updated_at": None
        })
    return ingredients


def seed_data():
    """Seed the database with sample recipes, ingredient groups, and ingredients."""
    app = create_app()
    with app.app_context():
        print("Seeding data...")
        
        for recipe_id in range(1, 51):  # Assuming 50 recipes
            print(f"Seeding ingredient groups for Recipe ID {recipe_id}...")
            groups = generate_ingredient_group_data(recipe_id)
            
            for group_data in groups:
                existing_group = IngredientGroupModel.query.filter_by(
                    recipe_id=group_data["recipe_id"],
                    group_name=group_data["group_name"]
                ).first()
                
                if not existing_group:
                    new_group = IngredientGroupModel(**group_data)
                    db.session.add(new_group)
                    db.session.flush()  # Get the group ID
                    
                    ingredients = generate_ingredient_data(new_group.id)
                    for ingredient in ingredients:
                        new_ingredient = IngredientModel(**ingredient)
                        db.session.add(new_ingredient)
        
        db.session.commit()
        print("Database seeded with sample ingredient groups and ingredients.")


if __name__ == "__main__":
    seed_data()
