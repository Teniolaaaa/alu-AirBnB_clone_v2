#!/usr/bin/python3
"""
Unit tests for the Review class.

This module contains comprehensive tests for the Review class
including attribute validation and relationship verification.
"""
import unittest
import os
from models.review import Review
from models.base_model import BaseModel


class TestReviewInstantiation(unittest.TestCase):
    """Test cases for Review instantiation."""

    def test_no_args_instantiation(self):
        """Test creating a Review with no arguments."""
        review = Review()
        self.assertIsInstance(review, Review)

    def test_inherits_from_base_model(self):
        """Test that Review inherits from BaseModel."""
        review = Review()
        self.assertIsInstance(review, BaseModel)

    def test_id_is_string(self):
        """Test that Review id is a string."""
        review = Review()
        self.assertIsInstance(review.id, str)

    def test_text_attribute_exists(self):
        """Test that Review has text attribute."""
        review = Review()
        self.assertTrue(hasattr(review, "text"))

    def test_place_id_attribute_exists(self):
        """Test that Review has place_id attribute."""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))

    def test_user_id_attribute_exists(self):
        """Test that Review has user_id attribute."""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))


class TestReviewAttributes(unittest.TestCase):
    """Test cases for Review attributes."""

    def test_text_can_be_set(self):
        """Test that text can be set."""
        review = Review()
        review.text = "Amazing place, huge kitchen"
        self.assertEqual(review.text, "Amazing place, huge kitchen")

    def test_place_id_can_be_set(self):
        """Test that place_id can be set."""
        review = Review()
        review.place_id = "12345"
        self.assertEqual(review.place_id, "12345")

    def test_user_id_can_be_set(self):
        """Test that user_id can be set."""
        review = Review()
        review.user_id = "67890"
        self.assertEqual(review.user_id, "67890")


class TestReviewToDict(unittest.TestCase):
    """Test cases for Review to_dict method."""

    def test_to_dict_returns_dict(self):
        """Test that to_dict returns a dictionary."""
        review = Review()
        self.assertIsInstance(review.to_dict(), dict)

    def test_to_dict_contains_class(self):
        """Test that to_dict contains __class__ key with value 'Review'."""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(review_dict["__class__"], "Review")


if __name__ == "__main__":
    unittest.main()
