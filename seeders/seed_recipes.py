from datetime import datetime, timezone, timedelta
from db import db
from models.recipe import RecipeModel
from app import create_app
import random

def generate_recipe_data():
    base_recipes = [
        {
            "name": "Nasi Goreng",
            "img_banner": "https://example.com/images/nasi-goreng.jpg",
            "country": "Indonesia",
            "description": "Delicious fried rice with traditional spices.",
            "video_url": "https://example.com/videos/nasi-goreng.mp4",
            "difficulty": 2,
            "estimated_time": "30 minutes"
        },
        {
            "name": "Spaghetti Carbonara",
            "img_banner": "https://example.com/images/carbonara.jpg",
            "country": "Italy",
            "description": "Classic Italian pasta dish with creamy sauce.",
            "video_url": "https://example.com/videos/carbonara.mp4",
            "difficulty": 3,
            "estimated_time": "25 minutes"
        },
        {
            "name": "Sushi",
            "img_banner": "https://example.com/images/sushi.jpg",
            "country": "Japan",
            "description": "Fresh sushi rolls with various fillings.",
            "video_url": "https://example.com/videos/sushi.mp4",
            "difficulty": 4,
            "estimated_time": "45 minutes"
        }
    ]

    recipes = []
    for i in range(100):
        base = random.choice(base_recipes)
        recipes.append({
            "name": f"{base['name']} Variant {i+1}",
            "img_banner": base["img_banner"].replace(".jpg", f"-{i+1}.jpg"),
            "country": base["country"],
            "description": f"{base['description']} (Variant {i+1})",
            "video_url": base["video_url"].replace(".mp4", f"-{i+1}.mp4"),
            "difficulty": random.randint(1, 5),
            "estimated_time": f"{random.randint(15, 60)} minutes",
            "created_at": datetime.now(timezone.utc) - timedelta(days=i)
        })
    return recipes

def seed_data():
    """Seed the database with sample recipes."""
    app = create_app()
    recipes = generate_recipe_data()
    with app.app_context():
        print("Seeding data...")
        for recipe in recipes:
            existing_recipe = RecipeModel.query.filter_by(name=recipe["name"]).first()
            if not existing_recipe:
                print(f"Adding recipe: {recipe['name']}")
                new_recipe = RecipeModel(**recipe)
                db.session.add(new_recipe)
        
        db.session.commit()
        print("Database seeded with sample data.")

if __name__ == "__main__":
    seed_data()