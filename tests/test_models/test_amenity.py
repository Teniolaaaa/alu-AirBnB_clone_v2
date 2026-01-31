#!/usr/bin/python3
"""
Unit tests for the Amenity class.

This module contains comprehensive tests for the Amenity class
including attribute validation and relationship verification.
"""
import unittest
import os
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenityInstantiation(unittest.TestCase):
    """Test cases for Amenity instantiation."""

    def test_no_args_instantiation(self):
        """Test creating an Amenity with no arguments."""
        amenity = Amenity()
        self.assertIsInstance(amenity, Amenity)

    def test_inherits_from_base_model(self):
        """Test that Amenity inherits from BaseModel."""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)

    def test_id_is_string(self):
        """Test that Amenity id is a string."""
        amenity = Amenity()
        self.assertIsInstance(amenity.id, str)

    def test_name_attribute_exists(self):
        """Test that Amenity has name attribute."""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))


class TestAmenityAttributes(unittest.TestCase):
    """Test cases for Amenity attributes."""

    def test_name_can_be_set(self):
        """Test that name can be set."""
        amenity = Amenity()
        amenity.name = "WiFi"
        self.assertEqual(amenity.name, "WiFi")

    def test_instantiation_with_kwargs(self):
        """Test Amenity instantiation with keyword arguments."""
        amenity = Amenity(name="Pool")
        self.assertEqual(amenity.name, "Pool")


class TestAmenityToDict(unittest.TestCase):
    """Test cases for Amenity to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary."""
        amenity = Amenity()
        self.assertIsInstance(amenity.to_dict(), dict)

    def test_to_dict_contains_class(self):
        """Test that to_dict contains __class__ key with value 'Amenity'."""
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(amenity_dict["__class__"], "Amenity")


if __name__ == "__main__":
    unittest.main()
