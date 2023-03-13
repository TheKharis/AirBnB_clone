#!/usr/bin/python3
"""Define a file storage class for BaseModel object storage"""

import json

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Serialize and deserialize instances to a JSON file
    and deserialize JSON file to instances
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """set __objects with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, 'w') as f:
            json.dump({k: obj.to_dict() for k, obj in
                      self.__objects.items()}, f)

    def reload(self):
        """deserialize JSON file to __objects
        Return:
            deserialize only if file exist.
            else do nothing. No exception should be raised
        """
        try:
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                obj_dict = json.load(f)
                for key, obj_data in obj_dict.items():
                    class_name, obj_id = key.split(".")
                    obj_class = eval(class_name)
                    obj = obj_class(**obj_data)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass
