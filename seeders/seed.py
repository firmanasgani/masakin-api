from app import create_app
from db import db
from seeders.seed_category import seed_data as seed_categories
from seeders.seed_howto import seed_data as seed_howto
from seeders.seed_ingredient_group import seed_data as seed_ingredient_groups
from seeders.seed_ingredients import seed_data as seed_ingredients
from seeders.seed_recipes import seed_data as seed_recipes
from seeders.seed_tools import seed_data as seed_tools
from seeders.seed_user import seed_user_data as seed_users

def run_all_seeders():
    """Run all seeders in the correct order."""
    app = create_app()
    with app.app_context():
        try:
            print("Running Category Seeder...")
            seed_categories()

            print("Running User Seeder...")
            seed_users()

            print("Running Recipe Seeder...")
            seed_recipes()

            print("Running HowTo Seeder...")
            seed_howto()

            print("Running Ingredient Group Seeder...")
            seed_ingredient_groups()

            print("Running Tools Seeder...")
            seed_tools()

            db.session.commit()
            print("All seeders have been successfully executed.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
        finally:
            db.session.close()

if __name__ == "__main__":
    run_all_seeders()
