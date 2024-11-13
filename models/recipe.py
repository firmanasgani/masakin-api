from datetime import datetime
from db import db
from sqlalchemy.orm import relationship


class RecipeModel(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    img_banner = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    difficulty = db.Column(db.Integer, nullable=False)
    estimated_time = db.Column(db.String(11), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    ingredients = relationship("IngredientModel", back_populates="recipe")
    tools = relationship("ToolModel", back_populates="recipe")
    categories = relationship("CategoryModel", back_populates="recipe")
