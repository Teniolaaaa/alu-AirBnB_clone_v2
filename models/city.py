#!/usr/bin/python3
"""
City module for the AirBnB clone project.

This module defines the City class which represents a city within a state.
Cities are associated with states and can contain multiple places.
"""
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """
    City class representing a city within a state.

    A City belongs to a State and can contain multiple Places.
    This class supports both file storage and database storage backends.

    Attributes:
        __tablename__ (str): Database table name for SQLAlchemy
        name (str): The name of the city
        state_id (str): Foreign key reference to the parent State
        places (relationship): SQLAlchemy relationship to Place objects
    """

    # Database table name
    __tablename__ = "cities"

    # Column definitions for database storage
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)

    # Relationship to places - only for database storage
    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship(
            "Place",
            backref="cities",
            cascade="all, delete-orphan"
        )
