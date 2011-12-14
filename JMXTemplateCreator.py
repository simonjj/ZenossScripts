#!/usr/bin/env python
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.Zuul import getFacade
from Products.ZenUtils.Utils import prepId
from os.path import isfile
from Products.Zuul.interfaces import IDataPointInfo, IRRDDataSourceInfo, IGraphInfo
import logging
from transaction import commit



def readInTemplateFile(filename, seperator="@"):
    if not isfile(filename):
        return NoneA
    tempData = None
    with open(filename, "r") as infile:
        lines = infile.readlines()
        tempData = [l.strip().split(seperator) for l in lines]
    return tempData
            

class TemplateCreator(ZenScriptBase):
    
    def __init__(self):
        """
        create object and and coonect to the db
        """
        ZenScriptBase.__init__(self, connect=True)
        self.api = getFacade("template")
        self.log = logging.getLogger("TemplateCreator")
        
    def _checkPath(self, path):
        org = None
        try:
            self.dmd.getObjByPath("/zport/dmd"+ path)
            return True
        except:
            return False
        
        
    def createTemplate(self):
        self.log.debug("creating template now...")
        tp = self.options.target_template_path
        tn = self.options.target_template_name
        if self._checkPath(tp):
            return self.api.addTemplate(tn, "/zport/dmd" + tp)
        else:
            self.log.error("path %s does not exist" % tp)
            return None
            
            
    def getGraphById(self, t, graphid):
        for g in self.api.getGraphs(t.uid):
            if graphid == g.id: return g
            
            
    def createDatasourceAndHookup(self, t, dsname, dpname, 
                                    gname, dstype="COMMAND"):
	    self.log.debug("working on template %s, creating datasource %s" % (t.uid, dsname))
	    dsname = prepId(dsname)
	    a = self.api
	    nds = IRRDDataSourceInfo(a.addDataSource(t.uid, dsname, dstype))
	    ndp = IDataPointInfo(a.addDataPoint(nds.uid, dpname))
	    a.addGraphDefinition(t.uid, gname)
	    ng = self.getGraphById(t, gname)
	    a.addDataPointToGraph(ndp.uid, ng.uid)

        
    
    def buildOptions(self):
        ZenScriptBase.buildOptions(self)
        self.parser.add_option('--datasource_input_file',
                    dest="datasource_input_file", default=None,
                    help="which file contains the datasource information")
        self.parser.add_option('--target_template_path',
                    dest="target_template_path", default="/Devices/Server",
                    help="where should the new template be created, (e.g. /Devices/Server/Linux)")
        self.parser.add_option('--target_template_name',
                    dest="target_template_name", default=None,
                    help="where should the new template be created")
        
        





if __name__ == "__main__":
    templateCranker = TemplateCreator()
    data = readInTemplateFile(templateCranker.options.datasource_input_file)
    
    newTemplate = templateCranker.createTemplate()
    entry = data[0]
    templateCranker.createDatasourceAndHookup(newTemplate, entry[0], entry[2], entry[0])
    commit()


"""
# Copy old template to new template
a.copyTemplate(ZenJMX, ZenJMX_Hotels_Cassandra)
c.copyTemplate(template.uid, "/zport/dmd/Devices/ZenJMX_Hotels_Cassandra")

# Add new template to a certain device class
a.addTemplate("ZenJMX_Hotels_Cassandra ", "/zport/dmd/Devices/Server/SSH/Linux/Hotels.com/Production/Cassandra")

# read in a file and parse it into an array
myfile = open("/home/zenoss/templateCreations/hotels_cassandra_jmx.txt")
lines = [l.strip() for l in myfile.readlines()]
dsdata = []
for l in lines:
	dsdata.append(l.split()]

def mystuff(t, dsname, dpname, gname, dsobjectname, dsattribute, type="JMX"):
	from Products.Zuul.interfaces import IDataPointInfo, IRRDDataSourceInfo, IGraphInfo
	print "working on %s" % dsname
	nds = (IRRDDataSourceInfo(a.addDataSource(t.uid, dsname, type))
	print "created datasource"
	ndp = IDataPointInfo(a.addDataPoint(nds.uid, dpname))
	print "created data point"
	newT.addGraphDefinition(t.uid, gname)
	ng = getGraphById(t, gname)
	print "created graph def"
	a.addDataPointToGraph(ndp.uid, ng.uid)
	print "done"
print "... done"

"""

