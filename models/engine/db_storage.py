#!/usr/bin/python3
"""This module defines the DBStorage class."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """DBStorage class for MySQL database operations."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance."""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", "localhost")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(
            user, password, host, database
        )

        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects from the database."""
        classes = [State, City, User, Place, Review, Amenity]
        objects = {}

        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            for c in classes:
                query_result = self.__session.query(c).all()
                for obj in query_result:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Add object to current database session."""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the database."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """Close the session."""
        self.__session.remove()
