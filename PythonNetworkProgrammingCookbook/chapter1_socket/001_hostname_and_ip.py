__author__ = 'maxiee'

import socket

host = socket.gethostname()

print host
print socket.gethostbyname(host)