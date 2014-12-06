__author__ = 'Maxiee'

import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8800


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("Hello from server!")
        return


class CustomHTTPServer(HTTPServer):
    def __init__(self, host, port):
        server_address = (host, port)
        HTTPServer.__init__(self, server_address, RequestHandler)


def run_server():
    try:
        server = CustomHTTPServer(DEFAULT_HOST, DEFAULT_PORT)
        print "Server started"
        server.serve_forever()
    except Exception, err:
        print  "Error:%s" % err
    except KeyboardInterrupt:
        print "Server interrupted and is shutting down..."
        server.socket.close()


if __name__ == "__main__":
    run_server()