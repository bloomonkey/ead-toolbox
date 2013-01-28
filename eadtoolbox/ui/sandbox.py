
import sys
import webbrowser

from eadtoolbox.sandbox import EADSandboxWsgiApp
application = EADSandboxWsgiApp()

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    try:
        host = sys.argv[1]
    except IndexError:
        try:
            import socket
            host = socket.gethostname()
        except:
            host = 'localhost'
    try:
        port = int(sys.argv[2])
    except IndexError, ValueError:
        port = 8008
    httpd = make_server(host, port, application)
    url = "http://{0}:{1}".format(host, port)
    webbrowser.open(url)
    print """\
Hopefully a new browser window/tab should have opened displaying the
application.

If not, you should be able to access the application at:
"""
    print url
    httpd.serve_forever()
