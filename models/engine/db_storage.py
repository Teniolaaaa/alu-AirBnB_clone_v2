#!/usr/bin/python3
"""
DBStorage module for the AirBnB clone project.

This module defines the DBStorage class which handles database
operations using SQLAlchemy ORM. It provides MySQL database
persistence for all model objects.
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """
    DBStorage class for MySQL database operations using SQLAlchemy.

    This class manages database connections and operations including
    querying, adding, updating, and deleting objects from the database.

    Attributes:
        __engine: SQLAlchemy engine for database connection
        __session: SQLAlchemy session for database operations
    """

    # Private class attributes for database connection
    __engine = None
    __session = None

    # List of all model classes for querying
    __classes = [User, State, City, Place, Amenity, Review]

    def __init__(self):
        """
        Initialize the DBStorage instance.

        Creates the SQLAlchemy engine using environment variables for
        database connection parameters. Drops all tables if running
        in test environment.
        """
        # Get database connection parameters from environment
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", "localhost")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        # Create the database connection URL (using pymysql driver)
        db_url = "mysql+pymysql://{}:{}@{}/{}".format(
            user, password, host, database
        )

        # Create the SQLAlchemy engine with connection pooling
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        # Drop all tables if in test environment
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects from the database, optionally filtered by class.

        Args:
            cls: Optional class to filter objects by. Can be a class
                 object or a string class name.

        Returns:
            dict: Dictionary of objects with keys as '<class>.<id>'
        """
        objects = {}

        if cls is not None:
            # Handle string class names
            if isinstance(cls, str):
                cls = eval(cls)

            # Query objects of the specified class
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            # Query all objects from all classes
            for model_class in DBStorage.__classes:
                query_result = self.__session.query(model_class).all()
                for obj in query_result:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """
        Add a new object to the current database session.

        Args:
            obj: The object to add to the session
        """
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """
        Commit all changes in the current database session.

        Persists all pending changes to the database.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session.

        Args:
            obj: The object to delete. If None, nothing happens.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all database tables and initialize the session.

        Creates tables based on SQLAlchemy model definitions and
        sets up a thread-safe scoped session for database operations.
        """
        # Create all tables defined in the models
        Base.metadata.create_all(self.__engine)

        # Create a session factory with specific options
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )

        # Create a thread-safe scoped session
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Close the current database session.

        Removes the current session, releasing database resources.
        """
        self.__session.close()
