#!/usr/bin/python3
"""
State module for the AirBnB clone project.

This module defines the State class which represents a geographical state
or region. States contain cities and are a fundamental part of the
location hierarchy in the application.
"""
import models
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """
    State class representing a geographical state or region.

    A State can contain multiple cities. This class supports both
    file storage and database storage backends.

    Attributes:
        __tablename__ (str): Database table name for SQLAlchemy
        name (str): The name of the state
        cities (relationship): SQLAlchemy relationship to City objects
    """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """
            Getter for cities in file storage mode.

            Returns:
                list: List of City instances belonging to this state
            """
            from models.city import City
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
