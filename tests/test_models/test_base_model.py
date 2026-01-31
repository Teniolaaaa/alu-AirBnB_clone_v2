#!/usr/bin/python3
"""
Unit tests for the BaseModel class.

This module contains comprehensive tests for the BaseModel class
including initialization, serialization, and storage integration.
"""
import unittest
import os
from datetime import datetime
from models.base_model import BaseModel
from models import storage


class TestBaseModelInstantiation(unittest.TestCase):
    """Test cases for BaseModel instantiation."""

    def test_no_args_instantiation(self):
        """Test creating a BaseModel with no arguments."""
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)

    def test_id_is_string(self):
        """Test that id is a string."""
        model = BaseModel()
        self.assertIsInstance(model.id, str)

    def test_id_is_unique(self):
        """Test that each BaseModel gets a unique id."""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_created_at_is_datetime(self):
        """Test that created_at is a datetime object."""
        model = BaseModel()
        self.assertIsInstance(model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test that updated_at is a datetime object."""
        model = BaseModel()
        self.assertIsInstance(model.updated_at, datetime)

    def test_created_at_and_updated_at_initially_equal(self):
        """Test that created_at and updated_at are equal on creation."""
        model = BaseModel()
        # Allow for small time differences during execution
        diff = abs((model.updated_at - model.created_at).total_seconds())
        self.assertLess(diff, 1)

    def test_instantiation_with_kwargs(self):
        """Test creating a BaseModel with keyword arguments."""
        dt = datetime.now()
        dt_iso = dt.isoformat()
        model = BaseModel(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(model.id, "123")
        self.assertEqual(model.created_at, dt)
        self.assertEqual(model.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that None values in kwargs don't cause errors."""
        model = BaseModel(id=None, created_at=None, updated_at=None)
        self.assertIsNotNone(model.id)

    def test_instantiation_with_args_and_kwargs(self):
        """Test that args are ignored when kwargs are present."""
        dt = datetime.now()
        dt_iso = dt.isoformat()
        model = BaseModel("12345", id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(model.id, "123")


class TestBaseModelStr(unittest.TestCase):
    """Test cases for BaseModel __str__ method."""

    def test_str_representation(self):
        """Test the string representation of BaseModel."""
        model = BaseModel()
        model.id = "12345"
        expected_start = "[BaseModel] (12345)"
        self.assertIn(expected_start, str(model))

    def test_str_contains_dict(self):
        """Test that __str__ contains the __dict__ representation."""
        model = BaseModel()
        self.assertIn("id", str(model))
        self.assertIn("created_at", str(model))
        self.assertIn("updated_at", str(model))


class TestBaseModelSave(unittest.TestCase):
    """Test cases for BaseModel save method."""

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at timestamp."""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(old_updated_at, model.updated_at)
        self.assertGreater(model.updated_at, old_updated_at)


class TestBaseModelToDict(unittest.TestCase):
    """Test cases for BaseModel to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict() returns a dictionary."""
        model = BaseModel()
        self.assertIsInstance(model.to_dict(), dict)

    def test_to_dict_contains_class_key(self):
        """Test that to_dict() contains __class__ key."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIn("__class__", model_dict)
        self.assertEqual(model_dict["__class__"], "BaseModel")

    def test_to_dict_contains_id(self):
        """Test that to_dict() contains id."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIn("id", model_dict)

    def test_to_dict_contains_created_at(self):
        """Test that to_dict() contains created_at as string."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIn("created_at", model_dict)
        self.assertIsInstance(model_dict["created_at"], str)

    def test_to_dict_contains_updated_at(self):
        """Test that to_dict() contains updated_at as string."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIn("updated_at", model_dict)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_to_dict_datetime_iso_format(self):
        """Test that datetime attributes are in ISO format."""
        model = BaseModel()
        model_dict = model.to_dict()
        # ISO format: YYYY-MM-DDTHH:MM:SS.ffffff
        self.assertRegex(model_dict["created_at"],
                        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+")

    def test_to_dict_output_differs_from_dunder_dict(self):
        """Test that to_dict() output differs from __dict__."""
        model = BaseModel()
        self.assertNotEqual(model.to_dict(), model.__dict__)


if __name__ == "__main__":
    unittest.main()
