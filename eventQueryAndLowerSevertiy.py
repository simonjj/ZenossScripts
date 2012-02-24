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
from Products.Zuul import getFacade
from datetime import datetime
from time import time as now
import logging
from sets import *

# old events is how far back we go with the query
OLD_EVENTS=2000 #in minutes

# new events is the events we exclude from the old events query
CURRENT_EVENTS=1000 #in minutes

#3 warning
#4 error
#5 critical
# which severity should the events older than CURRENT_EVENTS be set to
TARGET_SEVERITY=3


class EventModder(ZenScriptBase):
    
    def __init__(self):
        """
        create object and and coonect to the db
        """
        ZenScriptBase.__init__(self, connect=True)
        self.log = logging.getLogger("EventModder")
	    self.api = getFacade("event")


    def _getTimeStr(self, etime):
    	return datetime.fromtimestamp(etime).strftime("%Y-%m-%dT%H:%M:%S")


    def getEventIds(self, time):
        #time needs to look like this: 2012-02-23T00:00:00
        #EDIT HERE IF YOU NEED TO CHANGE ANYTHING
	    limit = 0
	    start = 0
	    sort = "lastTime"
	    dir = "DESC"
	    filters = {"severity"    :[5,4],
		       "eventState"  :[0,1],
                       "prodState"   :["1000"],
                       "lastTime"    :time}
	    result = self.api.query(limit, start, sort, dir, filters)
	    events = []
	    if result['total'] > 0:
		    count = result['total']
		    events = result['data']
		    self.log.debug("found %s events for filter %s" % (count, filters))
	    else:
		    self.log.error("not result returned for query: %s" % filters)
		
        return [e['evid'] for e in events]


    def getEventIdsForUpdate(self):
	    current = Set(self.getCurrentEvents())
        old = Set(self.getOldEvents())
        old.difference_update(current)
        return [evid for evid in old]
            

    def lowerSeverityToWarning(self, evids):
        target_severity = TARGET_SEVERITY
	    q = 'update status set severity=%d where evid in ' % target_severity
        q += '(%s)' % ','.join(['%s']*len(evids))
        self.api._run_query(q, evids)
                               

    #get events that did get an update in the last 10min
    def getCurrentEvents(self):
	    self.log.debug("getting current events ===============")
	    time = self._getTimeStr(now()-(CURRENT_EVENTS-60))
    	    return self.getEventIds(time)

	
    #get events that got an update in the last 20min	
    def getOldEvents(self):
	    self.log.debug("getting old events ===============")
	    time = self._getTimeStr(now()-(OLD_EVENTS-60))
	    return self.getEventIds(time)



if __name__ == "__main__":
	mod = EventModder()
	ids = mod.getEventIdsForUpdate()
	if len(ids) > 0:
		print "changing the severity for the following evids: %s" % ids
		mod.lowerSeverityToWarning(ids)
