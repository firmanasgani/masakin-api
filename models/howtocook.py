from datetime import datetime
from db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class HowToCook(db.Model):
    __tablename__ = "howtocook"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    steps = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, ForeignKey("recipes.id"), nullable=False)
    description = db.Column(db.Text, nullable=False)

    images = relationship("HowToCookImage", back_populates="howtocook", cascade="all, delete-orphan")
    recipe = relationship("RecipeModel", back_populates="how_to_cooks")

