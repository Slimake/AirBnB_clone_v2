#!/usr/bin/python3
"""
This module defines a class to manage database storage for hbnb clone
"""
from sqlalchemy import create_engine
from models.base_model import Base
import models
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """This class manages storage of hbnb models to the database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage object"""
        # Get HBNB_MYSQL environment variables
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        # An engine, which the Session will use for connection resources
        connection_string = \
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db)

        # Create engine with pool_pre_ping enabled
        self.__engine = create_engine(connection_string, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            # Reflect existing table from database
            Base.metadata.reflect(self.__engine)

            # Drop all tables
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the current database session"""
        db_dict = {}

        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                db_dict[key] = obj
        else:
            for k, v in models.classes.items():
                if k != 'BaseModel':
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = '{}.{}'.format(type(obj).__name__, obj.id)
                            db_dict[key] = obj
        return db_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and the current session
        """
        Base.metadata.create_all(self.__engine)

        # Create a sessionmaker bound to engine
        session_factory = \
            sessionmaker(bind=self.__engine, expire_on_commit=False)

        # Scoped Session
        Session = scoped_session(session_factory)

        # Create a Session
        self.__session = Session()
