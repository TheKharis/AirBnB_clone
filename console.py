#!/usr/bin/python3
"""
Defines the entry point of command interpreter
"""
import cmd
import re
from shlex import split
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


# global tokenizing function
def parse(arg):
    """ Tokenize input from cmd line and perform approriate function"""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    b_brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:  # extract contents of braces or bracts
        if b_brackets is None:
            return [i.strip(",") for i in split(arg)]  # return if not found
        else:  # if content in b_bracts found, add to list of tokens
            expr = split(arg[:brackets.span()[0]])
            exprlst = [i.strip(",") for i in expr]
            exprlst.append(brackets.group())
            return exprlst
    else:  # if content in c_braces found
        expr = split(arg[:curly_braces.span()[0]])
        exprlst = [i.strip(",") for i in expr]
        exprlst.append(curly_braces.group())
        return exprlst


AVAILABLE_CLASSES = ['BaseModel', 'User', 'Place',
                     'State', 'City', 'Amenity', 'Review']


class HBNBCommand(cmd.Cmd):
    """Creates command line interpreter for AirBnB console"""
    prompt = '(hbnb) '

    def default(self, arg):
        """defines behaviour if cmd receives invalid command

        Args:
            arg (str): invalid command entered by user

        Return:
            executes invalid command if tokens are in cmd module
            else unknown syntax result
        How it works:
            split command entered into two: outer method name
            and inner method name. Look for parentheses in inner method
            if inner method name contains parentheses and outher method name
            is in dict_args, construct new command string by combining
            outer method name with args passed to inner method.
            Look up corresponding method of outer method name in dict_args
            and call method with new command string as args.
            Return False if method cannot parse invalud command by user
        """
        dict_args = {  # command keywords to implement
                "all": self.do_all,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update,
                "create": self.do_create,
                "count": self.do_count
                }
        match = re.search(r"\.", arg)  # arg search pattern
        if match is not None:  # if match is found
            arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                command = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in dict_args.keys():
                    call = "{} {}".format(arg_list[0], command[1])
                    return dict_args[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def emptyline(self):
        """Do nothing when an empty line + ENTER is pressed"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """CTRL+D function to abruptly but cleanly terminate program"""
        print("")
        return True

    def do_create(self, arg):
        """
        Usage: <create classname>
        Creates new instance of class. Saves it and prints id
        """
        arg_list = parse(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in AVAILABLE_CLASSES:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

        '''
            Extra feature (Because of ALX checker):
            Incase of excess Arguments tell the user it is not required
            if len(args_list) > 1:
            print("Excess ClassName (Not Required)")
        '''

    def do_show(self, arg):
        """
        Usage: show <class> <id> or <class>.show(<id>)
        Prints the string repr of an instance based on
        class name and id
        """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in AVAILABLE_CLASSES:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def do_destroy(self, arg):
        """
        Delete an instance based on the className and Id,
        and update JSON storage file
        Usage: <destroy ClassName Id>
        """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in AVAILABLE_CLASSES:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            """Modify the abstract storage and save the modified version
            to the JSON file
            """
            del obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            storage.save()

    def do_all(self, arg):
        """
        Print all string repr of all instances based or not
        on the class name
        Usage: <all classname> or <all>
        """
        arg_list = parse(arg)
        objs = storage.all()
        if len(arg_list) > 0 and arg_list[0] not in AVAILABLE_CLASSES:
            print("** class doesn't exist **")
        else:
            output = []
            for v in objs.values():
                if len(arg_list) > 0 and arg_list[0] == v.__class__.__name__:
                    output.append(v.__str__())
                elif len(arg_list) == 0:
                    output.append(v.__str__())
            print(output)

    def do_update(self, arg):
        """Updates an instance based on the class name and id
        by adding or updating a given attribute.
        Can also be updated using a k/v pair in dict.
        Usage: update <class> <id> <attr name> <attr value>
        or <class>.update(<id>, <attr name>, <attr value>)
        or <class>.update(<id>, <dictionary>)
        Only one attribute can be updated at a time.
        Attribute value is casted to attribute type
        """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
            return
        if arg_list[0] not in AVAILABLE_CLASSES:
            print("** class doesn't exist **")
            return
        if len(arg_list) == 1:
            print("** instance id missing **")
            return
        if "{}.{}".format(arg_list[0], arg_list[1]) not in obj_dict.keys():
            print("** no instance found **")
            return
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg_list) == 4:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = value_type(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for k, v in eval(arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = value_type(v)
                else:
                    obj.__dict__[k] = v

        storage.save()

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        arg_list = parse(arg)
        objs = storage.all()
        count = 0
        for obj in objs.values():
            if arg_list[0] == type(obj).__name__:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
