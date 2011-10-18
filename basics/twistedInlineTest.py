#!/usr/bin/env python

# Just a simple test to implement this:
# http://twistedmatrix.com/documents/current/api/twisted.internet.defer.html#inlineCallbacks

from twisted.internet import reactor, defer
from commands import getstatusoutput
from twisted.internet.threads import deferToThread


def printMsg(msg):
    print msg

def kickTimer():
    getstatusoutput("/bin/sleep 5")
    
@defer.inlineCallbacks
def startTimer():
    d = deferToThread(kickTimer)
    d.addCallback(lambda _: printMsg("timer run completed"))
    yield d
    

def runStuff():
    printMsg("starting to runStuff")
    runs = []
    for i in range(0,10):
        printMsg("starting timer #%s" % i)
        d = startTimer()
        runs.append(d)
    #stop the reactor when all the callbacks have been fired    
    defer.DeferredList(runs).addCallback(lambda _: reactor.stop())
    
    
if __name__ == "__main__":
    reactor.callLater(0, runStuff)
    reactor.run()

