#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='states', 
                              cascade='all, delete, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            """Getter for cities"""
            city_list = []
            all_cities = models.storage.all(City).values()

            for city in all_cities:
                if city.state_id == self.id:
                    city_list.append(city)
            return all_cities
