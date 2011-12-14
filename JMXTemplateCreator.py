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
            
            
    def createJMXDatasourceAndHookup(self, t, dsname, dpname, 
                                    gname, jmxoname, dstype="JMX"):
	    self.log.debug("working on template %s, creating datasource %s" % (t.uid, dsname))
	    dsname = prepId(dsname)
	    a = self.api
	    nds = IRRDDataSourceInfo(a.addDataSource(t.uid, dsname, dstype))
	    nds.objectName = jmxoname
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
    for entry in data:
        templateCranker.createJMXDatasourceAndHookup(newTemplate, entry[0], entry[2], entry[0], entry[1])
    
    commit()

