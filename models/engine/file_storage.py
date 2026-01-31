#!/usr/bin/python3
"""
FileStorage module for the AirBnB clone project.

This module defines the FileStorage class which handles serialization
and deserialization of objects to/from a JSON file. It provides a
simple file-based persistence mechanism.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    FileStorage class for serializing/deserializing objects to JSON file.

    This class manages the storage of all objects in a JSON file,
    providing methods for adding, retrieving, saving, and deleting objects.

    Attributes:
        __file_path (str): Path to the JSON storage file
        __objects (dict): Dictionary storing all objects by <class>.<id>
    """

    # Path to the JSON file for persistence
    __file_path = "file.json"

    # Dictionary to store all objects in memory
    __objects = {}

    # Mapping of class names to actual classes for reconstruction
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def all(self, cls=None):
        """
        Retrieve all objects, optionally filtered by class.

        Args:
            cls: Optional class to filter objects by. Can be a class
                 object or a string class name.

        Returns:
            dict: Dictionary of objects. If cls is specified, only objects
                  of that class are returned. Otherwise, all objects.
        """
        if cls is None:
            return FileStorage.__objects

        # Handle both class objects and class name strings
        if isinstance(cls, str):
            cls = FileStorage.__classes.get(cls)

        if cls is None:
            return {}

        # Filter objects by class type
        filtered = {}
        for key, obj in FileStorage.__objects.items():
            if isinstance(obj, cls):
                filtered[key] = obj
        return filtered

    def new(self, obj):
        """
        Add a new object to the storage dictionary.

        Args:
            obj: The object to add. Must have 'id' attribute and
                 __class__.__name__ property.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """
        Serialize and save all objects to the JSON file.

        Converts all objects to dictionary format and writes them
        to the JSON file specified by __file_path.
        """
        json_objects = {}
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserialize and load objects from the JSON file.

        Reads the JSON file and reconstructs all objects, storing
        them in the __objects dictionary. If the file doesn't exist,
        does nothing (no exception raised).
        """
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                json_objects = json.load(f)

            for key, obj_dict in json_objects.items():
                class_name = obj_dict["__class__"]
                if class_name in FileStorage.__classes:
                    cls = FileStorage.__classes[class_name]
                    FileStorage.__objects[key] = cls(**obj_dict)
        except FileNotFoundError:
            # File doesn't exist yet, nothing to load
            pass

    def delete(self, obj=None):
        """
        Delete an object from storage.

        Args:
            obj: The object to delete. If None, nothing happens.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """
        Reload objects from JSON file.

        This method is called to deserialize the JSON file to objects.
        Used for consistency with DBStorage interface.
        """
        self.reload()
