from datetime import datetime, timezone
from db import db
from sqlalchemy.orm import relationship

class IngredientGroupModel(db.Model):
    __tablename__ = "ingredient_groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now(timezone.utc))

    ingredients = db.relationship("IngredientModel", back_populates="ingredient_group")
    recipe = db.relationship("RecipeModel", back_populates="ingredient_groups")