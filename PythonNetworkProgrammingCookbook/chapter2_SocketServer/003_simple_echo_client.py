__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import socket

host = 'localhost'  # 服务器地址
data_payload = 2048  # 一次接受数据大小上限
port = 1127  # 服务器端口


def echo_client(port):
    # 创建socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接服务器
    server_address = (host, port)
    print 'Connecting to %s port %s' % server_address
    sock.connect(server_address)

    try:
        # 发送信息
        message = 'Test Msg...'
        print 'Sending %s' % message
        sock.sendall(message)
        # 接收信息并显示
        data = sock.recv(data_payload)
        print 'Received: %s' % data
    # 处理异常
    except socket.errno, e:
        print str(e)
    except Exception, e:
        print str(e)
    finally:
        # 发送完后，客户端自动关闭
        print 'Closing connection to the server'
        sock.close()


if __name__ == '__main__':
    # 启动客户端
    echo_client(port)