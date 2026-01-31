#!/usr/bin/python3
"""
Initialize the models package.

This module sets up the storage engine based on the environment variable
HBNB_TYPE_STORAGE. If set to 'db', it uses DBStorage (MySQL),
otherwise it defaults to FileStorage (JSON file).
"""
from os import getenv

# Check which storage type to use based on environment variable
storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    # Use database storage with SQLAlchemy
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    # Use file storage with JSON (default)
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Load existing data from storage
storage.reload()
