#!/usr/bin/python3
"""City module."""
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """City class."""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "cities"
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
    else:
        state_id = ""
        name = ""
