#!/usr/bin/python3
from fabric.api import *
from time import strftime
from pathlib import Path

# Set webservers to upload to
env.hosts = ['ubuntu@35.153.194.26', 'ubuntu@18.210.13.137']


def do_pack():
    """Return the archive path

    if the archive has been correctly generated.
    Otherwise, it should return False"""

    # Use strftime to format time
    time_now = strftime("%Y%m%d%H%M%S")
    try:
        # Create filename
        filename = "versions/web_static_{}.tgz".format(time_now)

        # Run fabric locally
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return False


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    path = Path(archive_path)
    if not path.exists():
        return False

    try:
        filename = archive_path.split("/")[-1]
        no_exten = filename.split(".")[0]
        data_path = "/data/web_static/releases/{}/".format(no_exten)
        symlink = "/data/web_static/current"
        # upload archive_path to /tmp
        put(archive_path, "/tmp")

        # cd into /tmp and put the archive_path file into it
        with cd("/tmp"):
            # Create folder
            sudo("mkdir -p {}".format(data_path))
            # Unpack the archive_path file to destination
            sudo("tar -zxf {0} -C {1}".format(filename, data_path))

            # Delete the archive from the web server
            sudo("rm {}".format(filename))

            # Move files one level up
            sudo("mv {0}web_static/* {0}".format(data_path))

            # Delete folder
            sudo("rm -rf {}web_static/".format(data_path))

            # Delete and recreate the symbolic link /data/web_static/current
            sudo("rm -rf {}".format(symlink))
            sudo("ln -s {0} {1}".format(data_path, symlink))
        return True
    except Exception:
        return False


def deploy():
    """Call do_pack and do_deploy function"""
    # Archive
    archive_path = do_pack()

    # Deploy to web servers
    do_deploy(archive_path)
