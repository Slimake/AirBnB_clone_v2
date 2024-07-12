#!/usr/bin/python3
"""
Fabric script methods:
    do_pack: bundles web_static/ files into .tgz archive
    do_deploy: deploys archive to webservers
    deploy: calls do_pack and do_deploy

Usage:
    fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
"""
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
        local("tar -cvzf {} web_static/".format(filename))
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    path = Path(archive_path)
    if path.exists() is False:
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
            run("mkdir -p {}".format(data_path))
            # Unpack the archive_path file to destination
            run("tar -zxf {0} -C {1}".format(filename, data_path))

            # Delete the archive from the web server
            run("rm {}".format(filename))

            # Move files one level up
            run("mv {0}web_static/* {0}".format(data_path))

            # Delete folder
            run("rm -rf {}web_static/".format(data_path))

            # Delete and recreate the symbolic link /data/web_static/current
            run("rm -rf {}".format(symlink))
            run("ln -s {0} {1}".format(data_path, symlink))
        return True
    except Exception:
        return False


def deploy():
    """Call do_pack and do_deploy function"""
    # Archive
    archive_path = do_pack()
    if archive_path is None:
        return False

    # Deploy to web servers
    success = do_deploy(archive_path)
    return success
