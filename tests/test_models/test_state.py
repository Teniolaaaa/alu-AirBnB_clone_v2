#!/usr/bin/python3
"""
Unit tests for the State class.

This module contains comprehensive tests for the State class
including attribute validation and relationship verification.
"""
import unittest
import os
from models.state import State
from models.base_model import BaseModel


class TestStateInstantiation(unittest.TestCase):
    """Test cases for State instantiation."""

    def test_no_args_instantiation(self):
        """Test creating a State with no arguments."""
        state = State()
        self.assertIsInstance(state, State)

    def test_inherits_from_base_model(self):
        """Test that State inherits from BaseModel."""
        state = State()
        self.assertIsInstance(state, BaseModel)

    def test_id_is_string(self):
        """Test that State id is a string."""
        state = State()
        self.assertIsInstance(state.id, str)

    def test_name_attribute_exists(self):
        """Test that State has name attribute."""
        state = State()
        self.assertTrue(hasattr(state, "name"))


class TestStateAttributes(unittest.TestCase):
    """Test cases for State attributes."""

    def test_name_can_be_set(self):
        """Test that name can be set."""
        state = State()
        state.name = "California"
        self.assertEqual(state.name, "California")

    def test_instantiation_with_kwargs(self):
        """Test State instantiation with keyword arguments."""
        state = State(name="California")
        self.assertEqual(state.name, "California")


class TestStateToDict(unittest.TestCase):
    """Test cases for State to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary."""
        state = State()
        self.assertIsInstance(state.to_dict(), dict)

    def test_to_dict_contains_class(self):
        """Test that to_dict contains __class__ key with value 'State'."""
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(state_dict["__class__"], "State")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db",
                 "Testing database storage")
class TestStateDBStorage(unittest.TestCase):
    """Test cases for State with database storage."""

    def test_cities_relationship(self):
        """Test that State has cities relationship for DB storage."""
        state = State()
        self.assertTrue(hasattr(state, "cities"))


if __name__ == "__main__":
    unittest.main()
