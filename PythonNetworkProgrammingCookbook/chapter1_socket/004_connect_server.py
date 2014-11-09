__author__ = 'maxiee'

import sys
import socket
import argparse


def main():
    parser = argparse.ArgumentParser(description='socket error examples')
    parser.add_argument('--host', action='store', dest='host', required=False)
    parser.add_argument('--port', action='store', dest='port', type=int, required=False)
    parser.add_argument('--file', action='store', dest='file', required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        print e
        sys.exit(1)

    try:
        s.connect((host, port))
    except socket.gaierror, e:
        print e
        sys.exit(1)
    except socket.error, e:
        print e
        sys.exit(1)

    try:
        s.sendall("GET %s HTTP/1.0\r\n\r\n" % filename)
    except socket.error, e:
        print e
        sys.exit(1)

    while 1:
        try:
            buf = s.recv(2048)
        except socket.error, e:
            print e
            sys.exit(1)
        if not len(buf):
            break
        sys.stdout.write(buf)


if __name__ == '__main__':
    main()