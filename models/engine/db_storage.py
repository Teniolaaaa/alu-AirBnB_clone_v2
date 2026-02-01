#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the current database session"""
        new_dict = {}
        for clss in classes.values():
            if cls is None or cls == clss or cls == clss.__name__:
                objs = self.__session.query(clss).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commit all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and start a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()   # ✅ critical fix

    def close(self):
        """Close the session"""
        self.__session.close()
