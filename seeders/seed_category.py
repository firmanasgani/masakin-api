from datetime import datetime, timezone, timedelta
from db import db
from models.category import CategoryModel  
from app import create_app
import random

def generate_country_category_data():
    base_countries = [
        {
            "name": "Indonesia",
            "description": "Rich in cultural and culinary diversity."
        },
        {
            "name": "Italy",
            "description": "Home of pasta, pizza, and a rich culinary tradition."
        },
        {
            "name": "Japan",
            "description": "Famous for sushi, ramen, and meticulous culinary arts."
        },
        {
            "name": "France",
            "description": "Known for its fine dining and exquisite pastries."
        },
        {
            "name": "Mexico",
            "description": "Spicy, vibrant, and flavorful cuisine."
        },
        {
            "name": "India",
            "description": "Known for its diverse and richly spiced dishes."
        },
        {
            "name": "Thailand",
            "description": "Famous for its balance of sweet, sour, salty, and spicy flavors."
        }
    ]

    categories = []
    for i in range(20):  # Generate 20 unique category variants
        base = random.choice(base_countries)
        categories.append({
            "name": f"{base['name']} Variant {i+1}",
            "description": f"{base['description']} (Variant {i+1})",
            "created_at": datetime.now(timezone.utc) - timedelta(days=i),
            "updated_at": datetime.now(timezone.utc) - timedelta(days=i//2)
        })
    return categories

def seed_data():
    """Seed the database with sample country categories."""
    app = create_app()
    categories = generate_country_category_data()
    with app.app_context():
        print("Seeding data...")
        for category in categories:
            existing_category = CategoryModel.query.filter_by(name=category["name"]).first()
            if not existing_category:
                print(f"Adding category: {category['name']}")
                new_category = CategoryModel(**category)
                db.session.add(new_category)
        
        db.session.commit()
        print("Database seeded with sample data.")

if __name__ == "__main__":
    seed_data()
