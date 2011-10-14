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


class SoftwareRetriever(ZenScriptBase):
    
    def __init__(self):
        """
        create object and and coonect to the db
        """
        ZenScriptBase.__init__(self, connect=True)
        self.log = logging.getLogger("SR")


    def _getSoftware(self, devobjects):
        """
        for a bunch of device objects query their software
        """
        self.log.debug("getting software for: %s" % devobjects)
        softwarelist = {}
        for d in devobjects:
            softwarelist[d.titleOrId()] = [s.id for s in d.os.software()]
        return softwarelist


    def getSoftwareForDevices(self, servers):
        """
        take an array of device ids, make sure to check their ids and 
        retrieve the device object
        """
        if not servers: return
        if isinstance(servers, str):
            servers = [servers]
        #prune the server ids to make sure they are all valid
        vservers = []
        for s in servers:
            d = self.dmd.Devices.findDevice(s)
            if d: vservers.append(d)
            else: self.log.warning("invalid device id %s, skipping..." % s)
        return self._getSoftware(vservers)


    def getSoftwareForOrganizer(self, orgname):
        """
        check the validity of a given oragnizer and retrive the devices under it
        """
        org = None
        try:
            org = self.dmd.getObjByPath("/zport/dmd"+ orgname)
        except:
            pass
        if not isinstance(org, DeviceOrganizer):
            self.log.error("no organizer with the name %s exists" % orgname)
            return None
        return self._getSoftware(org.getSubDevices())


    def buildOptions(self):
        """
        add some additional options
        """
        ZenScriptBase.buildOptions(self)
        self.parser.add_option('--organizer',
                    dest="orgname",default=None,
                    help="specify the organizer for which you'd like to query software for, "\
                    "this setting will take presedence over the devices setting")
        self.parser.add_option('--device',
                    dest="devices", type="str", default=None, action="append",
                    help="specify the device(s) you want to query software for")
        self.parser.add_option('--settype', type="str",
                    dest="settype", default=None,
                    help="specify which type of set operation you'd like to perform, \
                    i.e. union, difference, intersection")



def main():
    #retrieve the software
    sq = SoftwareRetriever()
    software = None
    if sq.options.orgname:
        sq.log.info("retieving software for %s" % sq.options.orgname)
        software = sq.getSoftwareForOrganizer(sq.options.orgname)
    elif sq.options.devices:
        sq.log.info("retieving software for %s" % sq.options.orgname)
        software = sq.getSoftwareForDevices(sq.options.devices)
    else:
        raise Exception("please specify at least one organizer of devicename")
    
    #if we have software, let's do something with it
    if software:
        stype = sq.options.settype
        myset = None
        if stype:
            myset = None
            sq.log.info("determining the %s of the all the software" % stype)
            if stype == "union":
                myset = reduce(lambda a, b: set(a).union(b), software.values())
            elif stype == "intersection":
                myset = reduce(lambda a, b: set(a).intersection(b), software.values())
            elif stype == "difference":
                myset = reduce(lambda a, b: set(a).difference(b), software.values())
            else:
                raise Exception("set type %s is unsupported" % stype)
            
        #print the output
        for d,s in software.items():
            print "-" * 50
            print d
            print ",".join(s)
        if myset:
            print "-" * 50
            print "set type: %s" % stype
            print ",".join(myset)
            

if __name__ == "__main__":
    main()
