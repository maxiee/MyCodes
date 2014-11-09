__author__ = 'maxiee'

import socket

remote_host = 'www.baidu.com'

try:
    print socket.gethostbyname(remote_host)
except socket.error, err_msg:
    print err_msg