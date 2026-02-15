#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.
"""
from fabric.api import env, put, run
import os


# Define the web server hosts
env.hosts = ['13.220.103.184', '3.85.233.7']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path: Path to the archive file to deploy.

    Returns:
        True if all operations have been done correctly, False otherwise.
    """
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
