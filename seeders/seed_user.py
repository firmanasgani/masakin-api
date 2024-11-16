from datetime import datetime, timezone, timedelta
from db import db
from models.users import UserModel
from app import create_app
import random

def generate_user_data():
    base_users = [
        {
            "email": "user1@example.com",
            "full_name": "John Doe",
            "password": "password123"
        },
        {
            "email": "user2@example.com",
            "full_name": "Jane Smith",
            "password": "password456"
        },
        {
            "email": "user3@example.com",
            "full_name": "Alice Johnson",
            "password": "password789"
        }
    ]

    users = []
    for i in range(20):  # Generate 20 users
        base = random.choice(base_users)
        user = {
            "email": f"user{i+1}@example.com",
            "full_name": f"{base['full_name']} {i+1}",
            "password": base["password"],
            "created_at": datetime.now(timezone.utc) - timedelta(days=i),
            "updated_at": datetime.now(timezone.utc) - timedelta(days=i)
        }
        users.append(user)
    return users

def seed_user_data():
    """Seed the database with sample users."""
    app = create_app()
    users = generate_user_data()
    with app.app_context():
        print("Seeding user data...")
        for user_data in users:
            existing_user = UserModel.query.filter_by(email=user_data["email"]).first()
            if not existing_user:
                print(f"Adding user: {user_data['email']}")
                new_user = UserModel(
                    email=user_data["email"],
                    full_name=user_data["full_name"]
                )
                new_user.set_password(user_data["password"])
                db.session.add(new_user)
        
        db.session.commit()
        print("Database seeded with sample users.")

if __name__ == "__main__":
    seed_user_data()
