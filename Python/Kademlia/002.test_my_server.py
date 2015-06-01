from twisted.internet import reactor
from twisted.python import log
from myserver import MyServer
import sys

def done(result):
    print "Key result:", result
    reactor.stop()

def setDone(result, server):
    server.get("a key").addCallback(done)

def bootstrapDone(found, server):
    server.set("a key", "a value").addCallback(setDone, server)

bt_list = [
        ("213.125.18.163", 14662),
        ("114.39.181.172", 11194),
        ("71.238.187.114", 4662),
        ("115.70.239.220", 3389),
        ("85.241.34.5", 61153)]
server = MyServer()
server.listen(8468)
server.bootstrap(bt_list).addCallback(bootstrapDone, server)

reactor.run()
