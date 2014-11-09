__author__ = 'maxiee'

import os
import socket
import threading
import SocketServer

SERVER_HOST = 'localhost'
SERVER_PORT = 0 # tell kernel to pick up a port dynamically
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ForkingClient():
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip,port))

    def run(self):
        current_process_id = os.getpid()
        print 'PID %s' %current_process_id
        sent_data_length = self.sock.send(ECHO_MSG)
        print 'Sent %d characters' % sent_data_length

        response = self.sock.recv(BUF_SIZE)
        print 'PID %s received: %s' %(current_process_id,response[5:])

    def shutdown(self):
        self.sock.close()

class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # send the echo back to the client
        data = self.request.recv(BUF_SIZE)
        current_pocess_id = os.getpid()
        response = '%s:%s'%(current_pocess_id,data)
        print "Server sending response [%s]" % response
        self.request.send(response)
        return

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    # inherited everything necessary from parents
    pass

def main():
    server = ForkingServer((SERVER_HOST,SERVER_PORT),ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True) # dont't hang on exit
    server_thread.start()
    print 'Server loop running PID %s' %os.getpid()

    # launch the clients
    client1 = ForkingClient(ip,port)
    client1.run()

    client2 = ForkingClient(ip,port)
    client2.run()

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()

if __name__=="__main__":
    main()