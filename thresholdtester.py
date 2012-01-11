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
# - add testing and evaluation for other threshold types
#


# Running the script in test mode (test an expression against a value):
# thresholdtester.py --value=123 --min="here.hw.totalMemory * 0.1" --device=localhost

# more information to the types of variables for thresholds can be found here:
# 


# Running the script in eval mode (test an existing device and a existing template):
# thresholdtester.py --template=/zport/dmd/Devices/Server/Linux/rrdTemplates/Device --device=localhost --mode=eval




import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.ZenModel.DeviceOrganizer import DeviceOrganizer
from Products.ZenModel.MinMaxThreshold import MinMaxThreshold
from Products.ZenModel.RRDTemplate import RRDTemplate

import logging


class ThresholdSandbox(ZenScriptBase):
    
    def __init__(self):
        """
        create object and and connect to the db
        """
        ZenScriptBase.__init__(self, connect=True)
        self.log = logging.getLogger("TS")
        self.mode = self.options.mode
        self.device = self.options.device
        self.template = self.options.tpath
        self.min = self.options.min
        self.max = self.options.max
        self.value = self.options.value
        

    
    def evaluate(self):
        d = self._getDevice()   
        if d:
            temp = self._getTemplate(self.template)
            if temp:
                thresholds = temp.thresholds()
                for t in thresholds:
                    ti = t.createThresholdInstance(d)
                    print "Processing Threshold %s" % ti.id
                    for dp in ti.dataPoints():
                        print " - checking datapoint %s" % dp
                        val = d.getRRDValue(dp)
                        if not val:
                            print "  ...unable to retrieve value.. skipping"
                            continue
                        print "The following event would be generated: %s" % ti.checkRange(ti.id, val)
                   
                
        
        pass
    
    def test(self):

        t = MinMaxThreshold("test_threshold")
        t.minval = self.min
        t.maxval = self.max
        ti = None
        d = self._getDevice()
        if d:
            ti = t.createThresholdInstance(d)
            if self.min:
                print "Using min of %s which evaluates to %s" % (self.min, ti.minimum)
            if self.max:
                print "Using max of %s which evaluates to %s" % (self.max, ti.maximum)
           
            print "The following event would be generated: %s" % ti.checkRange("test_threshold", self.value)


    def _getDevice(self):
        return self.dmd.Devices.findDevice(self.device)


    def _getTemplate(self, temppath):
        """
        check the validity of a given template path and retrieve the template
        """
        temp = None
        try:
            temp = self.dmd.getObjByPath(temppath)
        except:
            pass
        if not isinstance(temp, RRDTemplate):
            self.log.error("no template with the name %s exists" % temppath)
        return temp


    def buildOptions(self):
        """
        add some additional options
        """
        ZenScriptBase.buildOptions(self)
        
        self.parser.add_option('--mode',
                    dest="mode", default=None,
                    help="Specify operating mode:\neval = evaluate an existing "\
                        "threshold against a specific device\ntest = create a " \
                        "test threshold and evaluate it against a device")
        self.parser.add_option('--device', "-d",
                    dest="device", type="str", default=None, 
                    help="Specfiy a device for threshold evaluation (eval & test mode)")
        self.parser.add_option('--template_path', '-p', type="str",
                    dest="tpath", default=None,
                    help="Specify the path to a template path i.e. /zport/dmd/Devices/rrdTemplates/Device (eval mode)")
        self.parser.add_option('--min', '-i', type="str",
                    dest="min", default=None,
                    help="Specify a minimum value to be used for the threshold (eval mode)")
        self.parser.add_option('--max', '-a', type="str",
                    dest="max", default=None,
                    help="Specify a maximum value to be used for the threshold (eval mode)")
        self.parser.add_option('--value', type="str",
                    dest="value", default=None,
                    help="Specify an artificial value to use for threshold evaluation (eval mode)")


if __name__ == "__main__":
    
    
    ts = ThresholdSandbox()
    if ts.options.mode == "eval":
        ts.evaluate()
    elif ts.options.mode == "test":
        ts.test()    
    else:
        print "Please specify which mode to use (eval or test)"
