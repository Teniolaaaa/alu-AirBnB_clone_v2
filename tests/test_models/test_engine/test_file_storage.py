#!/usr/bin/python3
"""
Unit tests for the FileStorage class.

This module contains comprehensive tests for the FileStorage class
including save, reload, all, new, and delete operations.
"""
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestFileStorageInstantiation(unittest.TestCase):
    """Test cases for FileStorage instantiation."""

    def test_instantiation_no_args(self):
        """Test creating FileStorage with no arguments."""
        storage = FileStorage()
        self.assertIsInstance(storage, FileStorage)

    def test_file_path_is_private_string(self):
        """Test that __file_path is a private string attribute."""
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_is_private_dict(self):
        """Test that __objects is a private dictionary attribute."""
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestFileStorageAll(unittest.TestCase):
    """Test cases for FileStorage all method."""

    def setUp(self):
        """Set up test fixtures."""
        self.storage = FileStorage()
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_class_filter(self):
        """Test that all(cls) returns filtered dictionary."""
        state = State()
        state.name = "California"
        self.storage.new(state)
        result = self.storage.all(State)
        self.assertEqual(len(result), 1)

    def test_all_with_no_filter(self):
        """Test that all() returns all objects."""
        state = State()
        user = User()
        self.storage.new(state)
        self.storage.new(user)
        result = self.storage.all()
        self.assertEqual(len(result), 2)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestFileStorageNew(unittest.TestCase):
    """Test cases for FileStorage new method."""

    def setUp(self):
        """Set up test fixtures."""
        self.storage = FileStorage()
        FileStorage._FileStorage__objects = {}

    def test_new_adds_object(self):
        """Test that new() adds an object to __objects."""
        model = BaseModel()
        self.storage.new(model)
        key = "BaseModel.{}".format(model.id)
        self.assertIn(key, FileStorage._FileStorage__objects)

    def test_new_with_None(self):
        """Test that new() with None doesn't add anything."""
        initial_count = len(FileStorage._FileStorage__objects)
        self.storage.new(None)
        self.assertEqual(len(FileStorage._FileStorage__objects), initial_count)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestFileStorageSave(unittest.TestCase):
    """Test cases for FileStorage save method."""

    def setUp(self):
        """Set up test fixtures."""
        self.storage = FileStorage()
        FileStorage._FileStorage__objects = {}
        self.test_file = "file.json"

    def tearDown(self):
        """Clean up after tests."""
        try:
            os.remove(self.test_file)
        except FileNotFoundError:
            pass

    def test_save_creates_file(self):
        """Test that save() creates the JSON file."""
        model = BaseModel()
        self.storage.new(model)
        self.storage.save()
        self.assertTrue(os.path.exists(self.test_file))

    def test_save_writes_valid_json(self):
        """Test that save() writes valid JSON."""
        model = BaseModel()
        self.storage.new(model)
        self.storage.save()
        with open(self.test_file, "r") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestFileStorageDelete(unittest.TestCase):
    """Test cases for FileStorage delete method."""

    def setUp(self):
        """Set up test fixtures."""
        self.storage = FileStorage()
        FileStorage._FileStorage__objects = {}

    def test_delete_removes_object(self):
        """Test that delete() removes object from __objects."""
        state = State()
        self.storage.new(state)
        key = "State.{}".format(state.id)
        self.assertIn(key, FileStorage._FileStorage__objects)
        self.storage.delete(state)
        self.assertNotIn(key, FileStorage._FileStorage__objects)

    def test_delete_with_None(self):
        """Test that delete() with None doesn't cause errors."""
        state = State()
        self.storage.new(state)
        initial_count = len(FileStorage._FileStorage__objects)
        self.storage.delete(None)
        self.assertEqual(len(FileStorage._FileStorage__objects), initial_count)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestFileStorageReload(unittest.TestCase):
    """Test cases for FileStorage reload method."""

    def setUp(self):
        """Set up test fixtures."""
        self.storage = FileStorage()
        FileStorage._FileStorage__objects = {}
        self.test_file = "file.json"

    def tearDown(self):
        """Clean up after tests."""
        try:
            os.remove(self.test_file)
        except FileNotFoundError:
            pass

    def test_reload_from_nonexistent_file(self):
        """Test that reload() handles missing file gracefully."""
        try:
            os.remove(self.test_file)
        except FileNotFoundError:
            pass
        # Should not raise an exception
        self.storage.reload()

    def test_reload_restores_objects(self):
        """Test that reload() restores objects from file."""
        model = BaseModel()
        model_id = model.id
        self.storage.new(model)
        self.storage.save()
        FileStorage._FileStorage__objects = {}
        self.storage.reload()
        key = "BaseModel.{}".format(model_id)
        self.assertIn(key, FileStorage._FileStorage__objects)


if __name__ == "__main__":
    unittest.main()
