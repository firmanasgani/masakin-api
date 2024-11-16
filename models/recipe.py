from datetime import datetime
from db import db
from sqlalchemy.orm import relationship


class RecipeModel(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    img_banner = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    difficulty = db.Column(db.Integer, nullable=False)
    estimated_time = db.Column(db.String(11), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now())

    ingredient_groups = relationship("IngredientGroupModel", back_populates="recipe")
    tools = relationship("ToolModel", back_populates="recipe")
    category = relationship("CategoryModel", back_populates="recipes")