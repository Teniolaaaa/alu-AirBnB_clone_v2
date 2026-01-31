#!/usr/bin/python3
"""This module defines the FileStorage class."""
import json


class FileStorage:
    """FileStorage class for JSON file persistence."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return all objects, optionally filtered by class."""
        if cls is None:
            return FileStorage.__objects

        if isinstance(cls, str):
            cls = eval(cls)

        filtered = {}
        for key, obj in FileStorage.__objects.items():
            if isinstance(obj, cls):
                filtered[key] = obj
        return filtered

    def new(self, obj):
        """Add object to storage."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Save objects to JSON file."""
        json_objects = {}
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(json_objects, f)

    def reload(self):
        """Load objects from JSON file."""
        from models.base_model import BaseModel
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        classes = {
            "BaseModel": BaseModel,
            "State": State,
            "City": City,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity
        }

        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                json_objects = json.load(f)

            for key, obj_dict in json_objects.items():
                class_name = obj_dict["__class__"]
                if class_name in classes:
                    cls = classes[class_name]
                    FileStorage.__objects[key] = cls(**obj_dict)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete object from storage."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """Reload objects from JSON file."""
        self.reload()
