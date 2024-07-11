#!/usr/bin/python3
"""2-do_deploy_web_static Module"""

# Import fabric module
from fabric.api import *
from pathlib import Path

env.hosts = ['ubuntu@34.202.164.88', 'ubuntu@54.173.60.114']


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    filename = archive_path.split("/")[-1]
    no_exten = filename.split(".")[0]
    data_path = "/data/web_static/releases/{}/".format(no_exten)
    symlink = "/data/web_static/current"

    if Path(archive_path).exists() is False:
        return False
    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(data_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, data_path))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(data_path, data_path))
        run("rm -rf {}web_static".format(data_path))
        run("rm {}".format(symlink))
        run("ln -s {} {}".format(data_path, symlink))
        return True
    except Exception:
        return False
