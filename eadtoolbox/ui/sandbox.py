"""Start EAD Sandbox WSGI Application."""

import socket
import sys
import webbrowser

from argparse import ArgumentParser
from wsgiref.simple_server import make_server

from eadtoolbox.sandbox import EADSandboxWsgiApp

application = EADSandboxWsgiApp()

# Set up argument parser
argparser = ArgumentParser(description=__doc__.splitlines()[0])
# Find default hostname
try:
    hostname = socket.gethostname()
except:
    hostname = 'localhost'

argparser.add_argument('--hostname', type=str,
                  action='store', dest='hostname',
                  default=hostname, metavar='HOSTNAME',
                  help=("name of host to listen on. default derived by "
                        "inspection of local system"))
argparser.add_argument('-p', '--port', type=int,
                  action='store', dest='port',
                  default=8008, metavar='PORT',
                  help="number of port to listen on. default: 8008")


def start_sandbox(argv=None):
    global argparser
    if argv is None:
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(argv)
    
    httpd = make_server(args.hostname, args.port, application)
    url = "http://{0}:{1}".format(args.hostname, args.port)
    webbrowser.open(url)
    print """\
Hopefully a new browser window/tab should have opened displaying the
application.

If not, you should be able to access the application at:
"""
    print url
    return httpd.serve_forever()


if __name__ == "__main__":
    sys.exit(start_sandbox())
