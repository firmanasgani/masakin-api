from datetime import datetime, timezone
from db import db

class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False)
    nama_bahan = db.Column(db.String(255), nullable=False)   
    takaran = db.Column(db.String(255), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now(timezone.utc))
