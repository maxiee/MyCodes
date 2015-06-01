from twisted.internet import reactor
from twisted.python import log
from kademlia.network import Server
import sys

def done(result):
    print "Key result:", result
    reactor.stop()

def setDone(result, server):
    server.get("a key").addCallback(done)

def bootstrapDone(found, server):
    server.set("a key", "a value").addCallback(setDone, server)

server = Server()
server.listen(8468)
server.bootstrap([("94.34.192.216", 1755)]).addCallback(bootstrapDone, server)

reactor.run()
