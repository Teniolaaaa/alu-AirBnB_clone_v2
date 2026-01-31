#!/usr/bin/python3
"""
Console module for the AirBnB clone project.

This module provides an interactive command-line interface for managing
AirBnB clone objects. It supports creating, showing, updating, and
deleting objects, as well as listing all objects of a specific type.
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter for the AirBnB clone project.

    This class provides an interactive shell for managing objects
    in the AirBnB clone application. It supports various commands
    for CRUD operations on all model types.

    Attributes:
        prompt (str): The command prompt displayed to the user
    """

    prompt = "(hbnb) "

    # Dictionary mapping class names to class objects
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line input."""
        pass

    def do_create(self, arg):
        """
        Create a new instance of a class with optional parameters.

        Usage: create <class name> [<param 1> <param 2> ...]
        Parameter syntax: <key>=<value>
        Value types:
            - String: "value" (underscores become spaces)
            - Float: 1.5
            - Integer: 42

        Example: create State name="California"
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        # Create a new instance of the specified class
        new_instance = HBNBCommand.__classes[class_name]()

        # Process additional parameters if provided
        for param in args[1:]:
            # Parameters must be in key=value format
            if "=" not in param:
                continue

            key, value = param.split("=", 1)

            # Skip if key or value is empty
            if not key or not value:
                continue

            # Parse the value based on its type
            parsed_value = self._parse_param_value(value)

            if parsed_value is not None:
                setattr(new_instance, key, parsed_value)

        # Save the instance and print its ID
        new_instance.save()
        print(new_instance.id)

    def _parse_param_value(self, value):
        """
        Parse a parameter value and return the appropriate Python type.

        Args:
            value: The string value to parse

        Returns:
            The parsed value as string, int, or float; or None if invalid
        """
        # Check if it's a string (starts and ends with double quotes)
        if value.startswith('"') and value.endswith('"'):
            # Remove quotes and process the string
            string_value = value[1:-1]

            # Replace escaped double quotes with actual double quotes
            string_value = string_value.replace('\\"', '"')

            # Replace underscores with spaces
            string_value = string_value.replace("_", " ")

            return string_value

        # Check if it's a float (contains a dot)
        if "." in value:
            try:
                return float(value)
            except ValueError:
                return None

        # Try to parse as integer
        try:
            return int(value)
        except ValueError:
            return None

    def do_show(self, arg):
        """
        Display the string representation of an instance.

        Usage: show <class name> <id>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        print(objects[key])

    def do_destroy(self, arg):
        """
        Delete an instance based on class name and id.

        Usage: destroy <class name> <id>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        # Delete the object from storage
        objects[key].delete()
        storage.save()

    def do_all(self, arg):
        """
        Display all instances, or all instances of a specific class.

        Usage: all [<class name>]
        """
        args = arg.split()

        if len(args) > 0 and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        object_list = []

        if len(args) == 0:
            # Get all objects
            objects = storage.all()
        else:
            # Get objects of specific class
            objects = storage.all(HBNBCommand.__classes[args[0]])

        for obj in objects.values():
            object_list.append(str(obj))

        print(object_list)

    def do_update(self, arg):
        """
        Update an instance attribute based on class name and id.

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        if len(args) == 2:
            print("** attribute name missing **")
            return

        if len(args) == 3:
            print("** value missing **")
            return

        obj = objects[key]
        attr_name = args[2]
        attr_value = args[3]

        # Remove quotes from string values
        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value[1:-1]

        # Try to cast to appropriate type
        try:
            if hasattr(obj, attr_name):
                attr_type = type(getattr(obj, attr_name))
                attr_value = attr_type(attr_value)
        except (ValueError, TypeError):
            pass

        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_count(self, arg):
        """
        Count the number of instances of a class.

        Usage: count <class name>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        objects = storage.all(HBNBCommand.__classes[args[0]])
        print(len(objects))

    def default(self, line):
        """
        Handle commands in the format: <class name>.<command>(<args>)

        Supports: all(), count(), show(id), destroy(id), update(id, ...)
        """
        # Pattern to match <class>.<method>(<args>)
        match = re.match(r"^(\w+)\.(\w+)\((.*)\)$", line)

        if not match:
            print("*** Unknown syntax: {}".format(line))
            return

        class_name, method, args = match.groups()

        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        # Handle different methods
        if method == "all":
            self.do_all(class_name)
        elif method == "count":
            self.do_count(class_name)
        elif method == "show":
            # Remove quotes from id
            obj_id = args.strip('"\'')
            self.do_show("{} {}".format(class_name, obj_id))
        elif method == "destroy":
            obj_id = args.strip('"\'')
            self.do_destroy("{} {}".format(class_name, obj_id))
        elif method == "update":
            # Parse update arguments
            self._handle_update(class_name, args)
        else:
            print("*** Unknown syntax: {}".format(line))

    def _handle_update(self, class_name, args):
        """
        Handle the update command with various argument formats.

        Supports:
            - update(id, attr_name, attr_value)
            - update(id, {dict})
        """
        # Check for dictionary update format
        dict_match = re.match(r'^"([^"]+)",\s*(\{.*\})$', args)

        if dict_match:
            obj_id, dict_str = dict_match.groups()
            try:
                update_dict = eval(dict_str)
                for key, value in update_dict.items():
                    self.do_update('{} {} {} "{}"'.format(
                        class_name, obj_id, key, value
                    ))
            except (ValueError, SyntaxError):
                pass
            return

        # Regular update format: id, attr_name, attr_value
        parts = [p.strip().strip('"\'') for p in args.split(",")]

        if len(parts) >= 3:
            obj_id, attr_name, attr_value = parts[0], parts[1], parts[2]
            self.do_update('{} {} {} "{}"'.format(
                class_name, obj_id, attr_name, attr_value
            ))
        elif len(parts) == 2:
            self.do_update("{} {} {}".format(class_name, parts[0], parts[1]))
        elif len(parts) == 1:
            self.do_update("{} {}".format(class_name, parts[0]))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
