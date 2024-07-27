#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import models

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objs = {}  # store objs of one type of class
        if cls:  # cls is not empty
            for key, value in FileStorage.__objects.items():
                if cls.__name__ == value.to_dict()['__class__']:
                    objs.update({key: value.to_dict()})
            return objs
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = models.classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects"""
        if obj:
            _cls = obj.to_dict()['__class__']
            _id = obj.to_dict()['id']
            key = _cls + '.' + _id
            # Delete key if found
            if key in self.all().keys():
                del self.all()[key]
            self.save()
