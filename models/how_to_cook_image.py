from datetime import datetime, timezone
from db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class HowToCookImage(db.Model):
    __tablename__ = "howtocook_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    howtocook_id = db.Column(db.Integer, ForeignKey("howtocook.id"), nullable=False)
    img_url = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now(timezone.utc))

    howtocook = relationship("HowToCook", back_populates="images")