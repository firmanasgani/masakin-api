from datetime import datetime, timezone
from db import db
from models.howtocook import HowToCook
from models.how_to_cook_image import HowToCookImage
from models.recipe import RecipeModel
from app import create_app
import random

def generate_how_to_cook_data(valid_recipe_ids):
    base_steps = [
        {"description": "Preheat the oven to 350°F (175°C)."},
        {"description": "Mix the ingredients in a bowl."},
        {"description": "Pour the batter into a baking pan."},
        {"description": "Bake for 25 minutes or until golden brown."},
        {"description": "Stir-fry the vegetables on medium heat."},
        {"description": "Serve the dish hot with a garnish of parsley."},
    ]

    steps = []
    for _ in range(100):
        base = random.choice(base_steps)
        recipe_id = random.choice(valid_recipe_ids)
        step_number = random.randint(1, 10)  # Generate random step numbers between 1 and 10
        steps.append({
            "recipe_id": recipe_id,
            "steps": step_number,
            "description": base["description"]
        })
    return steps

def generate_how_to_cook_images(howtocook_id):
    """Generate random image URLs for each HowToCook record."""
    img_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg",
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
    """Seed the database with HowToCook and HowToCookImage data."""
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
                # Check if the step already exists
                existing_step = HowToCook.query.filter_by(
                    recipe_id=step["recipe_id"],
                    steps=step["steps"]
                ).first()

                if not existing_step:
                    print(f"Adding step {step['steps']} for Recipe ID {step['recipe_id']}")
                    new_step = HowToCook(
                        recipe_id=step["recipe_id"],
                        steps=step["steps"],
                        description=step["description"]
                    )
                    db.session.add(new_step)
                    db.session.flush()  # Ensure new_step.id is available before adding images

                    # Generate and add images for this step
                    images = generate_how_to_cook_images(new_step.id)
                    for image in images:
                        new_image = HowToCookImage(**image)
                        db.session.add(new_image)

            except Exception as e:
                db.session.rollback()
                print(f"Error adding step {step['steps']} for Recipe ID {step['recipe_id']}: {str(e)}")

        try:
            db.session.commit()
            print("Database seeded with HowToCook and HowToCookImage data.")
        except Exception as e:
            print(f"Error committing the session: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    seed_data()
