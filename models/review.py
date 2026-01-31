#!/usr/bin/python3
"""This module defines the Review class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from os import getenv


class Review(BaseModel, Base):
    """Review class for the reviews table."""

    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        place_id = ""
        user_id = ""
        text = ""
