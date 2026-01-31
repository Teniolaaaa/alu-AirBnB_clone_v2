#!/usr/bin/python3
"""
User module for the AirBnB clone project.

This module defines the User class which represents a user account
in the application. Users can own places and write reviews.
"""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """
    User class representing a user account in the application.

    Users can create places (as hosts) and write reviews (as guests).
    This class supports both file storage and database storage backends.

    Attributes:
        __tablename__ (str): Database table name for SQLAlchemy
        email (str): User's email address (required)
        password (str): User's password (required)
        first_name (str): User's first name (optional)
        last_name (str): User's last name (optional)
        places (relationship): Places owned by the user
        reviews (relationship): Reviews written by the user
    """

    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship(
            "Place",
            backref="user",
            cascade="all, delete, delete-orphan"
        )
        reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete, delete-orphan"
        )
