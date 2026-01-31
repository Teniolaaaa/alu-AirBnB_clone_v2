#!/usr/bin/python3
"""This module defines the Amenity class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv


class Amenity(BaseModel, Base):
    """Amenity class for the amenities table."""

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        name = ""
