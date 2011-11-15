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
from pprint import pprint
import logging


class UserSettingsDumper(ZenScriptBase):
    
    def __init__(self):
        """
        create object and and coonect to the db
        """
        ZenScriptBase.__init__(self, connect=True)
        self.log = logging.getLogger("UIdumper")

    def dumpUserBrowserState(self, userId):
        if not userId:
            self.log.error("Please specify a valid user id.")
            return None
        usersettings = self.dmd.getObjByPath("/zport/dmd/ZenUsers/"+ userId)
        if usersettings:
            false = False
            true = True
            pprint(eval(usersettings._browser_state["state"]))
        else:
            self.log.error("Unable to find user settings for %s" % userId)


    def buildOptions(self):
        """
        add some additional options
        """
        ZenScriptBase.buildOptions(self)
        self.parser.add_option('--userid',
                    dest="userid",default=None,
                    help="Specify the user id to dump the settings for.")


if __name__ == "__main__":
    dumper = UserSettingsDumper()
    dumper.dumpUserBrowserState(dumper.options.userid)

