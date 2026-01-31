#!/usr/bin/python3
"""
Unit tests for the console (command interpreter).

This module contains tests for the HBNBCommand class including
create, show, destroy, all, and update commands.
"""
import unittest
import os
import sys
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage


class TestHBNBCommandPrompt(unittest.TestCase):
    """Test cases for console prompt."""

    def test_prompt_string(self):
        """Test that prompt is (hbnb) ."""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        """Test that empty line doesn't produce output."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("")
            self.assertEqual("", output.getvalue())


class TestHBNBCommandHelp(unittest.TestCase):
    """Test cases for help command."""

    def test_help_quit(self):
        """Test help quit output."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("help quit")
            self.assertIn("Quit", output.getvalue())


class TestHBNBCommandExit(unittest.TestCase):
    """Test cases for exit commands."""

    def test_quit_exits(self):
        """Test that quit returns True."""
        with patch("sys.stdout", new=StringIO()):
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        """Test that EOF returns True."""
        with patch("sys.stdout", new=StringIO()):
            self.assertTrue(HBNBCommand().onecmd("EOF"))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestHBNBCommandCreate(unittest.TestCase):
    """Test cases for create command."""

    def test_create_missing_class(self):
        """Test create with missing class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create")
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_create_invalid_class(self):
        """Test create with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create InvalidClass")
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_create_valid_class(self):
        """Test create with valid class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            output_value = output.getvalue().strip()
            # Output should be a valid UUID
            self.assertEqual(len(output_value), 36)

    def test_create_with_string_param(self):
        """Test create with string parameter."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="California"')
            state_id = output.getvalue().strip()
            key = "State.{}".format(state_id)
            self.assertIn(key, storage.all())

    def test_create_with_underscore_in_string(self):
        """Test create with underscores replaced by spaces."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="New_York"')
            state_id = output.getvalue().strip()
            key = "State.{}".format(state_id)
            obj = storage.all()[key]
            self.assertEqual(obj.name, "New York")

    def test_create_with_integer_param(self):
        """Test create with integer parameter."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create Place number_rooms=4')
            place_id = output.getvalue().strip()
            key = "Place.{}".format(place_id)
            obj = storage.all()[key]
            self.assertEqual(obj.number_rooms, 4)

    def test_create_with_float_param(self):
        """Test create with float parameter."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd('create Place latitude=37.77')
            place_id = output.getvalue().strip()
            key = "Place.{}".format(place_id)
            obj = storage.all()[key]
            self.assertEqual(obj.latitude, 37.77)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestHBNBCommandShow(unittest.TestCase):
    """Test cases for show command."""

    def test_show_missing_class(self):
        """Test show with missing class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("show")
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_show_invalid_class(self):
        """Test show with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("show InvalidClass")
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_show_missing_id(self):
        """Test show with missing id."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual("** instance id missing **\n", output.getvalue())

    def test_show_invalid_id(self):
        """Test show with invalid id."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("show BaseModel 12345")
            self.assertEqual("** no instance found **\n", output.getvalue())


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestHBNBCommandDestroy(unittest.TestCase):
    """Test cases for destroy command."""

    def test_destroy_missing_class(self):
        """Test destroy with missing class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("destroy")
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_destroy_invalid_class(self):
        """Test destroy with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("destroy InvalidClass")
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_destroy_missing_id(self):
        """Test destroy with missing id."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **\n", output.getvalue())


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestHBNBCommandAll(unittest.TestCase):
    """Test cases for all command."""

    def test_all_invalid_class(self):
        """Test all with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("all InvalidClass")
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_all_valid(self):
        """Test all with no arguments."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("all")
            self.assertIn("[", output.getvalue())


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "Testing file storage")
class TestHBNBCommandUpdate(unittest.TestCase):
    """Test cases for update command."""

    def test_update_missing_class(self):
        """Test update with missing class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("update")
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_update_invalid_class(self):
        """Test update with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("update InvalidClass")
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_update_missing_id(self):
        """Test update with missing id."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("update BaseModel")
            self.assertEqual("** instance id missing **\n", output.getvalue())


if __name__ == "__main__":
    unittest.main()
