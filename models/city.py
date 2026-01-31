#!/usr/bin/python3
"""This module defines the City class."""
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """City class for the cities table."""

    __tablename__ = "cities"

    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
    else:
        state_id = ""
        name = ""
