#!/usr/bin/env python
from optparse import OptionParser, OptionValueError
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit
import sys

def processAll(options):
        dmd = ZenScriptBase(connect=True).dmd
        devpath = dmd.getObjByPath('/zport/dmd' + options.path)
        print "Processing Devices under %s" % options.path
        print "Turning %s processes/ip services\n" % prettyAction(options.action)
        if not devpath:
                raise OptionValueError("Path %s does not exist, " +
                                       "please specify existing path" \
                                       % options.path)
                sys.exit(1)

        todos = {}
        if options.process:
                todos["processes"] = options.process.split(",")
        if options.ipservice:
                todos["ipservices"] = options.ipservice.split(",")

        for d in devpath.getSubDevices():
            for todo, procs in todos.items():
                processDevice(todo, d, procs, options.action)


def processDevice(todo, dev, procs, action):
        dprocs = getattr(dev.os, todo)
        changed = False
        for p in dprocs():
                if p.name() in procs:
                        #import pdb; pdb.set_trace()
                        if not changed:
                                print "Device: %s" % dev.id
                        print " - process: %s" % p.name()
                        changed = True
                        p.setZenProperty("zMonitor", action)
        if changed:
                commit()
                print ""


def prettyAction(action):
        if action:
                return "on"
        return "off"


def checkOpts(opts):
        '''do some basic checking on the command line options here'''
        on = opts.action
        if on and on.lower() == "on": opts.action = True
        elif on and on.lower() == "off": 
                opts.action = False
        else:
                raise OptionValueError("Please use either 'on' " +
                                       " or 'off' for the action option")
        if not opts.path or opts.action == None or \
          (not opts.ipservice and not opts.process):
                raise OptionValueError("Please specify path, action " + 
                                       "and processes/ipservices to operate on")
        #delete argv so we don't run into conflict later
        sys.argv = []


def myOptions():
        parser = OptionParser()
        parser.add_option('-d', '--path', dest='path',
            default="/Devices",
            help='Group, System or Device class path, e.g. /Devices/Server/Linux')
        parser.add_option('-i', '--ipservice', dest='ipservice',
            help='Process name or comma seperated list of ' +
                 'ip services to manipulate.') 
        parser.add_option('-p', '--process', dest='process',
            help='Process name or comma seperated list of ' +
                 'processes to manipulate.') 
        parser.add_option('-a', '--action', dest='action', 
            help='Turn on (on) or off (off) the monitoring ' +
                 ' for the given processs')
        options, args = parser.parse_args()
        return options


if __name__ == "__main__":
        opts = myOptions()
        try:
                checkOpts(opts)
        except OptionValueError, e:
                print e
                sys.exit(1)
        processAll(opts)

