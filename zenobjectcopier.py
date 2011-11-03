#!/usr/bin/env python
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import os
import sys
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase


class ZenObjectCopier(ZenScriptBase):
    """
    Class that can be used to export and import specific Zobjects out of one
    zenoss instance and into another. To be used when a full ZenPack is
    overkill for the situation.
    
    Example export command:
        zenobjectcopier.py --export \
            --object="/zport/dmd/Devices/rrdTemplates/Oracle Tablespaces" \
            --file=oracleTablespacesTemplate.xml
    
    Example import command:
        zenobjectcopier.py --import --file=oracleTablespacesTemplate.xml
    """
    
    def __init__(self):
        ZenScriptBase.__init__(self, connect=True)
    
    def buildOptions(self):
        ZenScriptBase.buildOptions(self)
        self.parser.add_option('--export', dest='export',
            action='store_true', default=False,
            help='Perform an XML export of an object')
        self.parser.add_option('--object', dest='object',
            help='Full path to the object being exported ' + 
                 '(e.g. /zport/dmd/Devices/rrdTemplates/Oracle Tablespaces)')

        self.parser.add_option('--import', dest='imprt',
            action='store_true', default=False,
            help='Perform an import of an object from XML')
            
        self.parser.add_option('--file', dest='file',
            help='Filename to of XML to import')
    
    def validateOptions(self):
        if self.options.export:
            if not self.options.object:
                print >> sys.stderr, 'You must specify the object to export.'
                sys.exit(1)
            if not self.options.file:
                print >> sys.stderr, 'You must specify the export file.'
                sys.exit(1)
        elif self.options.imprt:
            if not self.options.file:
                print >> sys.stderr, 'You must specify the file to import.'
                sys.exit(1)
            if not os.path.isfile(self.options.file):
                print >> sys.stderr, 'The specified file does not exist.'
                sys.exit(1)
        else:
            print >> sys.stderr, 'You must specify either export or import.'
            sys.exit(1)
    
    def doExport(self):
        obj = None
        try:
            obj = self.dmd.getObjByPath(self.options.object)
        except:
            print >> sys.stderr, 'No object at %s.' % self.options.object
            sys.exit(3)
        
        f = None
        try:
            f = open(self.options.file, 'w')
        except:
            print >> sys.stderr, 'Error writing to %s.' % self.options.file
            sys.exit(2)
        
        # Write the initial XML representation of the object to the file.
        print "Writing object XML to %s." % self.options.file
        obj.exportXml(f)
        f.close()
        
        # Open the file so we can make modifications to the XML.
        f = open(self.options.file, 'r')
        from xml.dom.minidom import parse
        xml = parse(f)
        f.close()
        
        # We need to specify the full path to the object so it can be imported.
        xml.getElementsByTagName('object')[0].setAttribute(
            'id', self.options.object)
        
        # Write the modified XML back to the file.
        f = open(self.options.file, 'w')
        xml.writexml(f, addindent="    ")
        f.close()
    
    def doImport(self):
        from Products.ZenRelations.ImportRM import ImportRM
        im = ImportRM(noopts=True, app=self.dmd.zport)
        
        f = None
        try:
            f = open(self.options.file, 'r')
        except:
            print >> sys.stderr, 'Error reading from %s.' % self.options.file
            sys.exit(2)
        
        print "Importing objects from %s." % self.options.file
        im.loadObjectFromXML(xmlfile=f)
        from transaction import commit
        commit()
        f.close()
    
    def run(self):
        self.validateOptions()
        if self.options.export:
            self.doExport()
        else:
            self.doImport()


if __name__ == '__main__':
    copier = ZenObjectCopier()
    copier.run()
