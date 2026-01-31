#!/usr/bin/python3
"""
BaseModel module for the AirBnB clone project.

This module defines the BaseModel class which serves as the foundation
for all other model classes in the project. It provides common attributes
and methods for serialization, deserialization, and database mapping.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base for SQLAlchemy ORM mapping
Base = declarative_base()


class BaseModel:
    """
    Base class for all models in the AirBnB clone project.

    This class provides common functionality including:
    - Unique ID generation
    - Timestamp management (created_at, updated_at)
    - Serialization to dictionary format
    - Integration with storage engines

    Attributes:
        id (str): Unique identifier for each instance
        created_at (datetime): Timestamp when instance was created
        updated_at (datetime): Timestamp when instance was last updated
    """

    # SQLAlchemy column definitions for database mapping
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel instance.

        Args:
            *args: Variable length argument list (not used)
            **kwargs: Keyword arguments for setting instance attributes

        If kwargs is provided, attributes are set from the dictionary.
        Special handling for 'created_at' and 'updated_at' to convert
        string representations to datetime objects.
        """
        if kwargs:
            # Set attributes from kwargs dictionary
            for key, value in kwargs.items():
                if key == "__class__":
                    # Skip the __class__ key as it shouldn't be an attribute
                    continue
                elif key in ("created_at", "updated_at"):
                    # Convert string timestamps to datetime objects
                    if isinstance(value, str):
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)

            # Ensure id exists
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())

            # Ensure timestamps exist
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            # Create new instance with generated values
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """
        Return a string representation of the instance.

        Returns:
            str: Formatted string showing class name, id, and attributes
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """
        Save the current instance to storage.

        Updates the 'updated_at' timestamp and persists the instance
        to the active storage engine (file or database).
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Convert the instance to a dictionary representation.

        Returns:
            dict: Dictionary containing all instance attributes,
                  with datetime objects converted to ISO format strings
                  and __class__ key added for reconstruction.
        """
        # Create a copy of the instance dictionary
        result = self.__dict__.copy()

        # Add the class name for reconstruction
        result["__class__"] = self.__class__.__name__

        # Convert datetime objects to ISO format strings
        if "created_at" in result:
            result["created_at"] = result["created_at"].isoformat()
        if "updated_at" in result:
            result["updated_at"] = result["updated_at"].isoformat()

        # Remove SQLAlchemy internal state if present
        if "_sa_instance_state" in result:
            del result["_sa_instance_state"]

        return result

    def delete(self):
        """
        Delete the current instance from storage.

        Removes the instance from the active storage engine.
        """
        from models import storage
        storage.delete(self)
