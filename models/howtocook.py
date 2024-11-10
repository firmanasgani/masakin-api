from datetime import datetime
from db import db
from sqlalchemy import ForeignKey

class HowToCook(db.Model):
    __tablename__ = "howtocook"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    steps = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, ForeignKey("recipes.id"), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_urls = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<HowToCook(id={self.id}, steps={self.steps}, recipe_id={self.recipe_id})>"
