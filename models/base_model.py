#!/usr/bin/python3
"""BaseModel module."""
import uuid
from datetime import datetime
from os import getenv
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """BaseModel class."""

    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel."""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ("created_at", "updated_at"):
                        if isinstance(value, str):
                            value = datetime.strptime(value, time_fmt)
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return string representation."""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, d)

    def save(self):
        """Save to storage."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return dictionary representation."""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        new_dict.pop("_sa_instance_state", None)
        return new_dict

    def delete(self):
        """Delete from storage."""
        models.storage.delete(self)
