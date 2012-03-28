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

#TODO:
# - allow for setting of default dashboard

# Example Uses 
#
# copy dashboard from admin user to normal user
# dashboardStateCopier.py -s admin -t normal

# copy dashboard from admin user to admin-dash.dmd file
# dashboardStateCopier.py -s admin -f admin-dash.dmd

# copy dashboard from file admin-dash.dmd to the normal user
# dashboardStateCopier.py -t normal -f admin-dash.dmd


import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.ZenModel.UserSettings import UserSettings
import pickle
import logging
import sys
import os.path
from transaction import commit


def loadPickle(name):
    if not os.path.isfile(name): return None
    mfile = open(name, 'r')
    obj = pickle.load(mfile)
    mfile.close()
    return obj

def savePickle(name, obj):
    mfile = open(name, 'w')
    pickle.dump(obj, mfile)
    mfile.close()




class DashboardStateController(ZenScriptBase):

    def __init__(self):
        """
        create object and and connect to the db
        """
        ZenScriptBase.__init__(self, connect=True)
        self.log = logging.getLogger("dashboard state controller")


    def handleStateTransfer(self):
        # let's write directly from source to target user 
        if self.options.source and self.options.target:
            self.log.info("Transfering dashboard state from %s to %s" % (self.options.source, self.options.target))
            su = self._getUser(self.options.source)
            tu = self._getUser(self.options.target)
            if tu and su:
                tu.dashboardState = su.dashboardState
                commit()
                self.log.info("Successfully transfered dashboard state.")
            else:
                self.log.info("Please specify existing users.")
                
        # let's write from source user into a file
        elif self.options.source and self.options.capfile:
            su = self._getUser(self.options.source)
            if su:
                myd = su.dashboardState
                savePickle(self.options.capfile, myd)
                self.log.info("Successfully captured dashboard state.")
            else:
                self.log.info("Please specify existing users.")
            
        # let's put a file onto a target user
        elif self.options.target and self.options.capfile:
            tu = self._getUser(self.options.target)
            if tu and os.path.isfile(self.options.capfile):
                myd = loadPickle(self.options.capfile)
                if myd:
                    tu.dashboardState = myd
                    commit()
                self.log.info("Successfully set dashboard state.")
            else:
                self.log.info("Please specify existing users and/or file.")


    def _getUser(self, username):
        """
        check the validity of a given template path and retrieve the template
        """
        temp = None
        try:
            temp = self.dmd.getObjByPath("/zport/dmd/ZenUsers/%s" % username)
        except:
            pass
        if not isinstance(temp, UserSettings):
            self.log.error("no user with the name %s exists" % username)
        return temp


    def buildOptions(self):
        """
        add some additional options
        """
        ZenScriptBase.buildOptions(self)
        
        self.parser.add_option('--source', '-s',
                    dest="source", default=None,
                    help="Specify user id to use as a the source dashboard configuration.")
        self.parser.add_option('--target', "-t",
                    dest="target", default=None, 
                    help="Specify user id to push the dashboard configuration to.")
        self.parser.add_option('--capfile', '-f', type="str",
                    dest="capfile", default=None,
                    help="When specified the capture file will be used as a target or source for a dashboard configuration.")



if __name__ == "__main__":
    dsc = DashboardStateController()
    if dsc.options.capfile and dsc.options.source and dsc.options.target:
        print "Unclear directive, please use one of the following combinations of options:\n " \
              "source and target, source and capfile or target and capfile"
        sys.exit(1)
    else:
        dsc.handleStateTransfer()
    
