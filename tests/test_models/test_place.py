#!/usr/bin/python3
"""
Unit tests for the Place class.

This module contains comprehensive tests for the Place class
including attribute validation and relationship verification.
"""
import unittest
import os
from models.place import Place
from models.base_model import BaseModel


class TestPlaceInstantiation(unittest.TestCase):
    """Test cases for Place instantiation."""

    def test_no_args_instantiation(self):
        """Test creating a Place with no arguments."""
        place = Place()
        self.assertIsInstance(place, Place)

    def test_inherits_from_base_model(self):
        """Test that Place inherits from BaseModel."""
        place = Place()
        self.assertIsInstance(place, BaseModel)

    def test_id_is_string(self):
        """Test that Place id is a string."""
        place = Place()
        self.assertIsInstance(place.id, str)


class TestPlaceAttributes(unittest.TestCase):
    """Test cases for Place attributes."""

    def test_city_id_attribute_exists(self):
        """Test that Place has city_id attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))

    def test_user_id_attribute_exists(self):
        """Test that Place has user_id attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "user_id"))

    def test_name_attribute_exists(self):
        """Test that Place has name attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "name"))

    def test_description_attribute_exists(self):
        """Test that Place has description attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "description"))

    def test_number_rooms_attribute_exists(self):
        """Test that Place has number_rooms attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))

    def test_number_bathrooms_attribute_exists(self):
        """Test that Place has number_bathrooms attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))

    def test_max_guest_attribute_exists(self):
        """Test that Place has max_guest attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "max_guest"))

    def test_price_by_night_attribute_exists(self):
        """Test that Place has price_by_night attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "price_by_night"))

    def test_latitude_attribute_exists(self):
        """Test that Place has latitude attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "latitude"))

    def test_longitude_attribute_exists(self):
        """Test that Place has longitude attribute."""
        place = Place()
        self.assertTrue(hasattr(place, "longitude"))

    def test_name_can_be_set(self):
        """Test that name can be set."""
        place = Place()
        place.name = "My little house"
        self.assertEqual(place.name, "My little house")

    def test_number_rooms_can_be_set(self):
        """Test that number_rooms can be set."""
        place = Place()
        place.number_rooms = 4
        self.assertEqual(place.number_rooms, 4)

    def test_latitude_can_be_set(self):
        """Test that latitude can be set."""
        place = Place()
        place.latitude = 37.773972
        self.assertEqual(place.latitude, 37.773972)

    def test_longitude_can_be_set(self):
        """Test that longitude can be set."""
        place = Place()
        place.longitude = -122.431297
        self.assertEqual(place.longitude, -122.431297)


class TestPlaceToDict(unittest.TestCase):
    """Test cases for Place to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary."""
        place = Place()
        self.assertIsInstance(place.to_dict(), dict)

    def test_to_dict_contains_class(self):
        """Test that to_dict contains __class__ key with value 'Place'."""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(place_dict["__class__"], "Place")


if __name__ == "__main__":
    unittest.main()
