#!/usr/bin/python3
"""
Review module for the AirBnB clone project.

This module defines the Review class which represents a review
written by a user for a place they've stayed at.
"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """
    Review class representing a user's review of a place.

    A Review belongs to both a Place and a User. Users can only
    review places they've visited. This class supports both file
    storage and database storage backends.

    Attributes:
        __tablename__ (str): Database table name for SQLAlchemy
        place_id (str): Foreign key to the Place being reviewed
        user_id (str): Foreign key to the User who wrote the review
        text (str): The review text content
    """

    # Database table name
    __tablename__ = "reviews"

    # Column definitions for database storage
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)
