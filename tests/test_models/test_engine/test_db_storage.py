#!/usr/bin/python3
"""
Unit tests for the DBStorage class.

This module contains comprehensive tests for the DBStorage class
including database operations with MySQL using SQLAlchemy.
"""
import unittest
import os
from models import storage


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "Testing database storage only")
class TestDBStorageInstantiation(unittest.TestCase):
    """Test cases for DBStorage instantiation."""

    def test_storage_is_db_storage(self):
        """Test that storage is DBStorage when env is set."""
        from models.engine.db_storage import DBStorage
        self.assertIsInstance(storage, DBStorage)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "Testing database storage only")
class TestDBStorageAll(unittest.TestCase):
    """Test cases for DBStorage all method."""

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        result = storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_class_filter(self):
        """Test that all(cls) filters by class."""
        from models.state import State
        result = storage.all(State)
        self.assertIsInstance(result, dict)
        for key in result:
            self.assertTrue(key.startswith("State."))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "Testing database storage only")
class TestDBStorageNew(unittest.TestCase):
    """Test cases for DBStorage new method."""

    def test_new_adds_object(self):
        """Test that new() adds object to session."""
        from models.state import State
        state = State(name="TestState")
        storage.new(state)
        # Object should be in session
        self.assertIn(state, storage._DBStorage__session.new)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "Testing database storage only")
class TestDBStorageSaveAndDelete(unittest.TestCase):
    """Test cases for DBStorage save and delete methods."""

    def test_save_commits_changes(self):
        """Test that save() commits changes to database."""
        from models.state import State
        state = State(name="SaveTestState")
        storage.new(state)
        storage.save()
        # After save, object should be in database
        key = "State.{}".format(state.id)
        all_states = storage.all(State)
        self.assertIn(key, all_states)

    def test_delete_removes_object(self):
        """Test that delete() removes object from database."""
        from models.state import State
        state = State(name="DeleteTestState")
        storage.new(state)
        storage.save()
        state_id = state.id
        storage.delete(state)
        storage.save()
        key = "State.{}".format(state_id)
        all_states = storage.all(State)
        self.assertNotIn(key, all_states)


if __name__ == "__main__":
    unittest.main()
