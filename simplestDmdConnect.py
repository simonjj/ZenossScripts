#!/usr/bin/env python

print "starting up..."

import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.Zuul import getFacade

print "connecting to dmd..."
dmd = ZenScriptBase(connect=True).dmd
print "...connected"


template_api = getFacade("template")
all_templates = template_api.getTemplates("/zport/dmd/Devices")
for t in all_templates:
    print t

print "... done"

