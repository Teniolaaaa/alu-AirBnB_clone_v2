#!/usr/bin/python3
"""This module contains the entry point of the command interpreter."""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB clone project."""

    prompt = "(hbnb) "

    __classes = {
        "BaseModel": BaseModel,
        "State": State,
        "City": City,
        "User": User,
        "Place": Place,
        "Review": Review,
        "Amenity": Amenity
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_create(self, arg):
        """Create a new instance with given parameters.
        Usage: create <class> [<key>=<value> ...]
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.__classes[class_name]()

        for param in args[1:]:
            if "=" not in param:
                continue

            key, value = param.split("=", 1)

            if not key or not value:
                continue

            parsed_value = self._parse_param_value(value)

            if parsed_value is not None:
                setattr(new_instance, key, parsed_value)

        new_instance.save()
        print(new_instance.id)

    def _parse_param_value(self, value):
        """Parse parameter value to appropriate type."""
        if value.startswith('"') and value.endswith('"'):
            string_value = value[1:-1]
            string_value = string_value.replace('\\"', '"')
            string_value = string_value.replace("_", " ")
            return string_value

        if "." in value:
            try:
                return float(value)
            except ValueError:
                return None

        try:
            return int(value)
        except ValueError:
            return None

    def do_show(self, arg):
        """Show an instance based on class name and id.
        Usage: show <class> <id>
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
        """Delete an instance based on class name and id.
        Usage: destroy <class> <id>
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

        storage.delete(objects[key])
        storage.save()

    def do_all(self, arg):
        """Show all instances, or all instances of a class.
        Usage: all [<class>]
        """
        args = arg.split()

        if len(args) > 0 and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        object_list = []

        if len(args) == 0:
            objects = storage.all()
        else:
            objects = storage.all(HBNBCommand.__classes[args[0]])

        for obj in objects.values():
            object_list.append(str(obj))

        print(object_list)

    def do_update(self, arg):
        """Update an instance attribute.
        Usage: update <class> <id> <attribute> "<value>"
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
        attr_value = args[3].strip('"')

        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            attr_value = attr_type(attr_value)

        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_count(self, arg):
        """Count instances of a class.
        Usage: count <class> or <class>.count()
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        count = 0
        objects = storage.all(HBNBCommand.__classes[args[0]])
        count = len(objects)
        print(count)

    def default(self, line):
        """Handle <class>.<command>() syntax."""
        match = re.match(r"^(\w+)\.(\w+)\((.*)\)$", line)

        if match:
            class_name = match.group(1)
            method = match.group(2)
            args = match.group(3)

            if class_name not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return

            if method == "all":
                self.do_all(class_name)
            elif method == "count":
                self.do_count(class_name)
            elif method == "show":
                self.do_show("{} {}".format(class_name, args.strip('"')))
            elif method == "destroy":
                self.do_destroy("{} {}".format(class_name, args.strip('"')))
            elif method == "update":
                if args.startswith("{"):
                    match2 = re.match(r'"([^"]+)",\s*(\{.*\})', args)
                    if match2:
                        obj_id = match2.group(1)
                        dict_str = match2.group(2)
                        try:
                            update_dict = eval(dict_str)
                            for k, v in update_dict.items():
                                self.do_update('{} {} {} "{}"'.format(
                                    class_name, obj_id, k, v))
                        except Exception:
                            pass
                else:
                    args_list = args.split(", ")
                    if len(args_list) >= 3:
                        obj_id = args_list[0].strip('"')
                        attr = args_list[1].strip('"')
                        val = args_list[2].strip('"')
                        self.do_update('{} {} {} "{}"'.format(
                            class_name, obj_id, attr, val))
                    elif len(args_list) >= 1:
                        obj_id = args_list[0].strip('"')
                        self.do_update("{} {}".format(class_name, obj_id))
            else:
                print("*** Unknown syntax: {}".format(line))
        else:
            print("*** Unknown syntax: {}".format(line))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
