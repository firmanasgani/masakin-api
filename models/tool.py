from datetime import datetime, timezone
from db import db
from sqlalchemy.orm import relationship

class ToolModel(db.Model):
    __tablename__ = "tools_recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)  
    nama_alat = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now(timezone.utc))

    recipe = relationship("RecipeModel", back_populates="tools")
