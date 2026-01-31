#!/usr/bin/python3
"""
Unit tests for the City class.

This module contains comprehensive tests for the City class
including attribute validation and relationship verification.
"""
import unittest
import os
from models.city import City
from models.state import State
from models.base_model import BaseModel


class TestCityInstantiation(unittest.TestCase):
    """Test cases for City instantiation."""

    def test_no_args_instantiation(self):
        """Test creating a City with no arguments."""
        city = City()
        self.assertIsInstance(city, City)

    def test_inherits_from_base_model(self):
        """Test that City inherits from BaseModel."""
        city = City()
        self.assertIsInstance(city, BaseModel)

    def test_id_is_string(self):
        """Test that City id is a string."""
        city = City()
        self.assertIsInstance(city.id, str)

    def test_name_attribute_exists(self):
        """Test that City has name attribute."""
        city = City()
        self.assertTrue(hasattr(city, "name"))

    def test_state_id_attribute_exists(self):
        """Test that City has state_id attribute."""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))


class TestCityAttributes(unittest.TestCase):
    """Test cases for City attributes."""

    def test_name_can_be_set(self):
        """Test that name can be set."""
        city = City()
        city.name = "San Francisco"
        self.assertEqual(city.name, "San Francisco")

    def test_state_id_can_be_set(self):
        """Test that state_id can be set."""
        city = City()
        city.state_id = "12345"
        self.assertEqual(city.state_id, "12345")

    def test_instantiation_with_kwargs(self):
        """Test City instantiation with keyword arguments."""
        city = City(name="San Francisco", state_id="12345")
        self.assertEqual(city.name, "San Francisco")
        self.assertEqual(city.state_id, "12345")


class TestCityToDict(unittest.TestCase):
    """Test cases for City to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary."""
        city = City()
        self.assertIsInstance(city.to_dict(), dict)

    def test_to_dict_contains_class(self):
        """Test that to_dict contains __class__ key with value 'City'."""
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(city_dict["__class__"], "City")


if __name__ == "__main__":
    unittest.main()
