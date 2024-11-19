from db import db
from sqlalchemy.orm import relationship

class RatingModel(db.Model):
    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)  
    rating_value = db.Column(db.Integer, nullable=False)

    recipe = relationship("RecipeModel", back_populates="ratings")
    user = relationship("UserModel", back_populates="rating")
