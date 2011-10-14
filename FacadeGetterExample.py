#! /usr/bin/env python
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################


import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.ZenModel.DeviceOrganizer import DeviceOrganizer
import logging


class FacadeGetterExample(ZenScriptBase):
    
    def __init__(self):
        """
        create object and and coonect to the db
        """
        ZenScriptBase.__init__(self, connect=True)
        self.log = logging.getLogger("SR")


    def getFacadeByName(self, name):
        return getFacade(name)


    def otherThings(self):
        #one also has access to the dmd here
        org = self.dmd.getObjByPath("/zport/dmd"+ orgname)


if __name__ == "__main__":
    fg = FacadeGetterExample()
    api = fg.getFacadeByName("zep")
    if api:
        print "we got an api reference to work with now: %s" % repr(api)
