#!/usr/bin/python3
"""This module defines the Place class."""
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column("place_id", String(60), ForeignKey("places.id"),
               primary_key=True, nullable=False),
        Column("amenity_id", String(60), ForeignKey("amenities.id"),
               primary_key=True, nullable=False)
    )


class Place(BaseModel, Base):
    """Place class for the places table."""

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

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False,
                                 backref="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Get list of Review instances with place_id equals self.id."""
            import models
            from models.review import Review
            review_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get list of Amenity instances linked to this Place."""
            import models
            from models.amenity import Amenity
            amenity_list = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Add an Amenity to the Place."""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
