#!/usr/bin/env python

# Just a simple test to implement this:
# http://twistedmatrix.com/documents/current/api/twisted.internet.defer.html#deferredGenerator

from twisted.internet import reactor, defer
from commands import getstatusoutput
from twisted.internet.threads import deferToThread
from copy import deepcopy


def printMsg(msg):
    print msg


def kickTimer():
    getstatusoutput("/bin/sleep 5")[0]
   
    
@defer.deferredGenerator
def startTimer():
    d = defer.waitForDeferred(deferToThread(kickTimer))
    yield d
    #this is absolutely necessary
    d.getResult()
    

def runStuff():
    printMsg("starting to runStuff")
    runs = []
    for i in range(0,10):
        myint = deepcopy(i)
        printMsg("starting timer #%s" % i)
        d = startTimer()
        d.addCallback(lambda _: printMsg("done"))
        runs.append(d)
    #stop the reactor when all the callbacks have been fired    
    defer.DeferredList(runs).addCallback(lambda _: reactor.stop())
    
    
if __name__ == "__main__":
    reactor.callLater(0, runStuff)
    reactor.run()
