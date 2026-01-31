#!/usr/bin/python3
"""This module defines the State class."""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """State class for the states table."""

    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Get list of City instances with state_id equals to self.id."""
            import models
            from models.city import City
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
