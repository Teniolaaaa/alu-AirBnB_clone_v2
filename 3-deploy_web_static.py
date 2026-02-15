#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
"""
from fabric.api import env, local
from datetime import datetime
import os


# Define the web server hosts
env.hosts = ['13.220.103.184', '3.85.233.7']


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


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path: Path to the archive file to deploy.

    Returns:
        True if all operations have been done correctly, False otherwise.
    """
    from fabric.api import put, run

    # Check if archive file exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the archive filename without path
        archive_filename = os.path.basename(archive_path)
        # Get the archive name without extension
        archive_name = archive_filename.replace(".tgz", "")

        # Define paths
        tmp_path = "/tmp/{}".format(archive_filename)
        release_path = "/data/web_static/releases/{}/".format(archive_name)

        # Upload the archive to /tmp/ directory on web server
        put(archive_path, tmp_path)

        # Create the release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive to the release folder
        run("tar -xzf {} -C {}".format(tmp_path, release_path))

        # Delete the archive from the web server
        run("rm {}".format(tmp_path))

        # Move contents from web_static subfolder to release folder
        run("mv {}web_static/* {}".format(release_path, release_path))

        # Remove the empty web_static directory
        run("rm -rf {}web_static".format(release_path))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers.

    This function:
    1. Calls do_pack() to create a new archive
    2. If no archive was created, returns False
    3. Calls do_deploy() with the new archive path
    4. Returns the result of do_deploy()

    Returns:
        True if deployment was successful, False otherwise.
    """
    # Create the archive
    archive_path = do_pack()

    # Return False if no archive was created
    if archive_path is None:
        return False

    # Deploy the archive and return the result
    return do_deploy(archive_path)

