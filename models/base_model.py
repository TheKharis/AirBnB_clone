#!/usr/bin/python3
""" Define main model class for console"""
import uuid
from datetime import datetime


class BaseModel:
    """Defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """initialize BaseModel Instances"""
        from models import storage
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    if k in ('created_at', 'updated_at'):
                        setattr(self, k, datetime.fromisoformat(v))
                    else:
                        setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """informal string representation of class objects"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """saves object instance modification date"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns dictionary copy of all instances"""
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
