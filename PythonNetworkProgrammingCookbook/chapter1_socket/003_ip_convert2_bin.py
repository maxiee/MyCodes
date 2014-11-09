__author__ = 'maxiee'

import socket
from binascii import hexlify

origin_ip = socket.gethostbyname('www.weibo.com')
print(origin_ip)

packeted_ip = socket.inet_aton(origin_ip)
print(hexlify(packeted_ip))

unpacked_ip = socket.inet_ntoa(packeted_ip)
print(unpacked_ip)
