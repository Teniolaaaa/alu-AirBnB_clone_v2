#!/usr/bin/python3
import cmd
from models import storage
from models.user import User

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, arg):
        return True

    def do_EOF(self, arg):
        print()
        return True

    def help_quit(self):
        print("Quit command to exit the program")

    def emptyline(self):
        pass
