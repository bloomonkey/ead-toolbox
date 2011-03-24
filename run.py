
import sys
sys.path.insert(1, 'src')

from eadsandbox.wsgi import EADSandboxWsgiApp
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
    print """You will be able to access the application at:
http://{0}:{1}""".format(host, port)
    httpd.serve_forever()