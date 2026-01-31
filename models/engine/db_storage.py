#!/usr/bin/python3
"""DBStorage module."""
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

classes = {"State": State, "City": City, "User": User,
           "Place": Place, "Review": Review, "Amenity": Amenity}


class DBStorage:
    """DBStorage class."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage."""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", "localhost")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects."""
        objs = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs[key] = obj
        else:
            for c in classes.values():
                for obj in self.__session.query(c).all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs[key] = obj
        return objs

    def new(self, obj):
        """Add object to session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """Close session."""
        self.__session.remove()
