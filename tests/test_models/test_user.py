#!/usr/bin/python3
"""
Unit tests for the User class.

This module contains comprehensive tests for the User class
including attribute validation and inheritance verification.
"""
import unittest
import os
from models.user import User
from models.base_model import BaseModel


class TestUserInstantiation(unittest.TestCase):
    """Test cases for User instantiation."""

    def test_no_args_instantiation(self):
        """Test creating a User with no arguments."""
        user = User()
        self.assertIsInstance(user, User)

    def test_inherits_from_base_model(self):
        """Test that User inherits from BaseModel."""
        user = User()
        self.assertIsInstance(user, BaseModel)

    def test_id_is_string(self):
        """Test that User id is a string."""
        user = User()
        self.assertIsInstance(user.id, str)

    def test_email_attribute_exists(self):
        """Test that User has email attribute."""
        user = User()
        self.assertTrue(hasattr(user, "email"))

    def test_password_attribute_exists(self):
        """Test that User has password attribute."""
        user = User()
        self.assertTrue(hasattr(user, "password"))

    def test_first_name_attribute_exists(self):
        """Test that User has first_name attribute."""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))

    def test_last_name_attribute_exists(self):
        """Test that User has last_name attribute."""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))


class TestUserAttributes(unittest.TestCase):
    """Test cases for User attributes."""

    def test_email_can_be_set(self):
        """Test that email can be set."""
        user = User()
        user.email = "test@example.com"
        self.assertEqual(user.email, "test@example.com")

    def test_password_can_be_set(self):
        """Test that password can be set."""
        user = User()
        user.password = "securepassword"
        self.assertEqual(user.password, "securepassword")

    def test_first_name_can_be_set(self):
        """Test that first_name can be set."""
        user = User()
        user.first_name = "John"
        self.assertEqual(user.first_name, "John")

    def test_last_name_can_be_set(self):
        """Test that last_name can be set."""
        user = User()
        user.last_name = "Doe"
        self.assertEqual(user.last_name, "Doe")

    def test_instantiation_with_kwargs(self):
        """Test User instantiation with keyword arguments."""
        user = User(email="test@example.com", password="pwd",
                   first_name="John", last_name="Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "pwd")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")


class TestUserToDict(unittest.TestCase):
    """Test cases for User to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary."""
        user = User()
        self.assertIsInstance(user.to_dict(), dict)

    def test_to_dict_contains_class(self):
        """Test that to_dict contains __class__ key with value 'User'."""
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")


if __name__ == "__main__":
    unittest.main()
