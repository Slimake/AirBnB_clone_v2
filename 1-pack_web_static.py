#!/usr/bin/python3
# a Fabric script that generates a .tgz archive
# from the contents of the web_static folder of your AirBnB Clone repo
# using the function do_pack

from fabric.api import local
from time import strftime


def do_pack():
    """Return the archive path

    if the archive has been correctly generated.
    Otherwise, it should return None"""
    # Use strftime to format time
    time_now = strftime("%Y%m%d%H%M%S")
    try:
        # Create filename
        filename = 'web_static_' + time_now

        # Run fabric locally
        local("mkdir -p versions")
        local("tar -cvzf versions/{}.tgz web_static".format(filename))
        return filename
    except Exception:
        return None
