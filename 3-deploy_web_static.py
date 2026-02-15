#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers.
"""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists
import os

env.hosts = ['13.220.103.184', '3.85.233.7']


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


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
