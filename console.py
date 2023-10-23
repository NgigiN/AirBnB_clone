#!/usr/bin/python3
"""Defines the console."""

import cmd
import re
from shlex import split
from models.engine.file_storage import FileStorage
from models.__init__ import storage
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

storage = FileStorage()
storage.reload()


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """The console class - command interpreter"""

    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Does nothing when an empty line."""
        pass

    def dquit(o_self, arg):
        """Exit the console"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit console"""
        print("")
        return True

    def help_EOF(self):
        """Prints documentation for EOF"""
        print("Exits the program without formatting\n")

    def do_create(self, arg):
        """Creates a new instance of the BaseModel, saves it
        and prints the id."""
        if len(args) == 0:
            print("** class name missing **")
            return

        args = parse(arg)

        if args[0] not in HBNBCommand.__classes:
            print("** classs doesn't exits **")
            return
        instance = eval(args[0])()

        storage.save()

        print(instance.id)

    def help_create(self):
        """Prints documentation for create"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, arg):
        """Displays the string represetation ofa class inatance"""

        if len(arg) == 0:
            print("** class name missing **")
            return

        argl = parse(arg)

        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(argl) == 1:
            print("** instance id missing **")
            return

        obj_dict = storage.all()
        obj_key = argl[0] + "." + argl[1]
        if obj_key not in obj_dict:
            print("** no instance found **")
            return

        obj = obj_dict[obj_key]
        print(obj)

    def help_show(self):
        """Prints documentation for Show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, arg):
        """Deletes an instance of a class of a given id"""

        if len(arg) == 0:
            print("** class name missing **")
            return

        argl = parse(arg)

        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(argl) == 1:
            print("** instance id missing **")
            return

        obj_dict = storage.all()
        obj_key = argl[0] + "." + argl[1]
        if obj_key not in obj_dict:
            print("** no instance found **")
            return

        else:
            del obj_dict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def help_destroy(self):
        """Prints documentation for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arg):
        """Disppalys string representation of all instances of a given class.
        If no class is specified, displays all instantiated objects"""
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def help_all(self):
        """Prints documentation of all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, arg):
        """Retrieves the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def help_count(self):
        """Prints documentation of the count command"""
        print("Usage: count <class_name>")

    def do_update(self, arg):
        """Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def help_update(self):
        """Prints documentation for the update command"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
