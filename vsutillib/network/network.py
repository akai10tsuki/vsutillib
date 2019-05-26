"""
Network related utilities
"""

import json
import socket
import urllib.parse
import urllib.request

REMOTE_SERVER = "www.google.com"

def isConnected(hostname=None):
    """
    Test for web server connection
    no parameters checks for
    internet connection
    """

    if hostname is None:
        hostname = REMOTE_SERVER

    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)

        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()

        return True

    except OSError:

        pass

    return False


def urlSearchJson(url, data=None, headers=None):
    """
    url search for json data retrieval
    it returns a dictionary
    """

    if data is not None:
        request = urllib.request.Request(url, data=data)
    else:
        request = urllib.request.Request(url)

    if headers is not None:
        for key in headers:
            request.add_header(key, headers[key])

    result = urllib.request.urlopen(request)

    if result.status == 200:

        bJson = result.read()
        data = json.loads(bJson.decode('utf-8'))
        return data

    return None
