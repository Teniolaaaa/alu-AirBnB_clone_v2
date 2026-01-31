#!/usr/bin/python3
"""
Amenity module for the AirBnB clone project.

This module defines the Amenity class which represents an amenity
that can be offered at a place (e.g., WiFi, Pool, Kitchen).
"""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """
    Amenity class representing a feature or service offered at places.

    Amenities are shared across places using a Many-to-Many relationship.
    Common examples include WiFi, Air Conditioning, Pool, etc.
    This class supports both file storage and database storage backends.

    Attributes:
        __tablename__ (str): Database table name for SQLAlchemy
        name (str): The name of the amenity
        place_amenities (relationship): Back-reference to places with this amenity
    """

    # Database table name
    __tablename__ = "amenities"

    # Column definition for database storage
    name = Column(String(128), nullable=False)
