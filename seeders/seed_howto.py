from datetime import datetime, timezone, timedelta
from db import db
from models.howtocook import HowToCook
from models.recipe import RecipeModel
from app import create_app
import random

def generate_how_to_cook_data(valid_recipe_ids):
    base_steps = [
        {"description": "Preheat the oven to 350°F (175°C).", "img_urls": "['https://example.com/image1.jpg']"},
        {"description": "Mix the ingredients in a bowl.", "img_urls": "['https://example.com/image2.jpg']"},
        {"description": "Pour the batter into a baking pan.", "img_urls": "['https://example.com/image3.jpg']"},
        {"description": "Bake for 25 minutes or until golden brown.", "img_urls": "['https://example.com/image4.jpg']"},
        {"description": "Stir-fry the vegetables on medium heat.", "img_urls": "['https://example.com/image5.jpg']"},
        {"description": "Serve the dish hot with a garnish of parsley.", "img_urls": "['https://example.com/image6.jpg']"},
    ]

    steps = []
    for _ in range(100):
        base = random.choice(base_steps)
        recipe_id = random.choice(valid_recipe_ids)
        step_number = random.randint(1, 10)  # Generate random step numbers between 1 and 10
        steps.append({
            "recipe_id": recipe_id,
            "steps": step_number,
            "description": base["description"],
            "img_urls": base["img_urls"],
        })
    return steps

def generate_how_to_cook_images(howtocook_id):
    """Generate random image URLs for each HowToCook record."""
    img_urls = [
        "https://storage.googleapis.com/masak-masak-file/file-14.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-15.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-16.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-17.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-18.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-19.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-20.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-21.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-22.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-23.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-24.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-25.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-26.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-27.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-28.jpeg",
        "https://storage.googleapis.com/masak-masak-file/file-29.jpeg",
    ]
    images = []
    for img_url in img_urls:
        images.append({
            "howtocook_id": howtocook_id,
            "img_url": img_url,
            "updated_at": datetime.now(timezone.utc)
        })
    return images

def seed_data():
    """Seed the database with sample steps for recipes."""
    app = create_app()

    with app.app_context():
        print("Seeding how_to_cook data...")

        valid_recipe_ids = [recipe.id for recipe in RecipeModel.query.all()]
        if not valid_recipe_ids:
            print("No recipes found in the database. Please seed the recipes table first.")
            return

        steps = generate_how_to_cook_data(valid_recipe_ids)

        for step in steps:
            try:
                existing_step = HowToCook.query.filter_by(
                    recipe_id=step["recipe_id"],
                    steps=step["steps"]
                ).first()
                if not existing_step:
                    print(f"Adding step {step['steps']} for Recipe ID {step['recipe_id']}")
                    new_step = HowToCook(**step)
                    db.session.add(new_step)

            except Exception as e:
                print(f"Error adding step {step['steps']} for Recipe ID {step['recipe_id']}: {str(e)}")

        try:
            db.session.commit()
            print("Database seeded with sample how_to_cook data.")
        except Exception as e:
            print(f"Error committing the session: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    seed_data()