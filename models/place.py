#!/usr/bin/python3
"""
Place module for the AirBnB clone project.

This module defines the Place class which represents a rental property
in the application. Places are the core entities that users can rent.
"""
import models
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

# Many-to-Many relationship table between Place and Amenity
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False
    )
)


class Place(BaseModel, Base):
    """
    Place class representing a rental property in the application.

    A Place belongs to a City and a User (host). It can have multiple
    amenities and reviews. This class supports both file storage and
    database storage backends.

    Attributes:
        __tablename__ (str): Database table name for SQLAlchemy
        city_id (str): Foreign key to the City where the place is located
        user_id (str): Foreign key to the User who owns the place
        name (str): Name of the place
        description (str): Description of the place
        number_rooms (int): Number of rooms (default: 0)
        number_bathrooms (int): Number of bathrooms (default: 0)
        max_guest (int): Maximum number of guests (default: 0)
        price_by_night (int): Price per night in cents (default: 0)
        latitude (float): Geographical latitude
        longitude (float): Geographical longitude
        amenity_ids (list): List of Amenity IDs (for file storage)
    """

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete, delete-orphan"
        )
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            backref="place_amenities"
        )
    else:
        @property
        def reviews(self):
            """
            Getter for reviews in file storage mode.

            Returns:
                list: List of Review instances for this place
            """
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """
            Getter for amenities in file storage mode.

            Returns:
                list: List of Amenity instances linked to this place
            """
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """
            Setter for amenities in file storage mode.

            Adds an Amenity ID to the amenity_ids list.

            Args:
                obj: An Amenity instance to link to this place
            """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
