from models.base import Base

from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column

from flask_login import UserMixin

import bcrypt

class Users(Base, UserMixin):
    __tablename__ = "users"

    id = mapped_column(String(255), primary_key=True)
    email = mapped_column(String(255))
    full_name = mapped_column(String(255))
    password = mapped_column(String(255))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
