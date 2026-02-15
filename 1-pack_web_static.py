#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    All files in the folder web_static are added to the final archive.
    All archives are stored in the folder versions.
    The archive name format is: web_static_<year><month><day><hour><minute><second>.tgz

    Returns:
        Archive path if the archive has been correctly generated, None otherwise.
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Generate archive filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)
        archive_path = "versions/{}".format(archive_name)

        # Print packing message
        print("Packing web_static to {}".format(archive_path))

        # Create the archive using tar
        result = local("tar -cvzf {} web_static".format(archive_path))

        # Get archive size
        archive_size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path,
                                                         archive_size))

        return archive_path

    except Exception:
        return None
