from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey, Date, Text

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)
