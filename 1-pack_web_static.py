#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of web_static.
"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))
        archive_size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(
            archive_path, archive_size))
        return archive_path
    except Exception:
        return None
