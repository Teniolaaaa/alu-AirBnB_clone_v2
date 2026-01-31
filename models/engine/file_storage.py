#!/usr/bin/python3
"""FileStorage module."""
import json
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {"BaseModel": BaseModel, "State": State, "City": City,
           "User": User, "Place": Place, "Review": Review, "Amenity": Amenity}


class FileStorage:
    """FileStorage class."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return all objects."""
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls = classes.get(cls)
        result = {}
        for key, obj in FileStorage.__objects.items():
            if isinstance(obj, cls):
                result[key] = obj
        return result

    def new(self, obj):
        """Add object."""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Save to file."""
        json_dict = {}
        for key, obj in FileStorage.__objects.items():
            json_dict[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(json_dict, f)

    def reload(self):
        """Load from file."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                json_dict = json.load(f)
            for key, val in json_dict.items():
                cls_name = val["__class__"]
                if cls_name in classes:
                    FileStorage.__objects[key] = classes[cls_name](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete object."""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects.pop(key, None)

    def close(self):
        """Reload."""
        self.reload()
