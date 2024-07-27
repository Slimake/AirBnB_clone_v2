#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel
from os import getenv


envv = getenv('HBNB_TYPE_STORAGE')
if envv == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

classes = {
    'BaseModel': BaseModel, 'User': User,
    'Place': Place, 'State': State,
    'City': City, 'Amenity': Amenity,
    'Review': Review
}

storage.reload()
