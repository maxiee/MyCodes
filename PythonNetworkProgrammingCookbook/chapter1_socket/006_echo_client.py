__author__ = 'maxiee'

import socket
import sys
import argparse

host = 'localhost'


def echo_client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print 'Connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        message = 'Test Msg...'
        print 'Sending %s' % message
        sock.sendall(message)
        amount_received = 0
        amount_expexted = len(message)
        while amount_received < amount_expexted:
            data = sock.recv(16)
            amount_received += len(data)
            print 'Received: %s' % data
    except socket.errno, e:
        print str(e)
    except Exception, e:
        print str(e)
    finally:
        print 'Closing connection to the server'
        sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action='store', dest='port', type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)