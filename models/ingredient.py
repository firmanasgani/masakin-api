from datetime import datetime, timezone
from db import db
from sqlalchemy.orm import relationship

class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    ingredient_group_id = db.Column(db.Integer, db.ForeignKey('ingredient_groups.id'), nullable=True)
    nama_bahan = db.Column(db.String(255), nullable=False)   
    takaran = db.Column(db.String(255), nullable=False) 
    image = db.Column(db.Text, nullable=False) 
    description = db.Column(db.Text, nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now(timezone.utc))

    ingredient_group = relationship("IngredientGroupModel", back_populates="ingredients")
 