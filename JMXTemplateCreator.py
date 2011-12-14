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
    """
    This method reads in the contents of filename and
    split each line using the seperator. It then stuffs all
    this into an array of arrays (one per line). This gets
    returned.
    """
    if not isfile(filename):
        return NoneA
    tempData = None
    with open(filename, "r") as infile:
        lines = infile.readlines()
        #split each line by the sperator and turn it into an array of
        #arrays
        tempData = [l.strip().split(seperator) for l in lines]
    return tempData
            

class TemplateCreator(ZenScriptBase):
    
    def __init__(self):
        """
        Connect to the dmd and make the template facade
        available to all other methods via self.api
        """
        ZenScriptBase.__init__(self, connect=True)
        self.api = getFacade("template")
        self.log = logging.getLogger("TemplateCreator")
        
        
    def _checkPath(self, path):
        """
        Check if a given path actually exists. e.g.
        /Devices/Server/Stuff
        """
        org = None
        try:
            self.dmd.getObjByPath("/zport/dmd"+ path)
            return True
        except:
            return False
        
        
    def createTemplate(self):
        """
        Create a template, use the name that is specified on 
        the command line (target_template_name).
        """
        self.log.debug("creating template now...")
        #define some easier to use variables
        tp = self.options.target_template_path
        tn = self.options.target_template_name
        #check to make sure the path is valid before we proceed
        if self._checkPath(tp):
            return self.api.addTemplate(tn, "/zport/dmd" + tp)
        else:
            self.log.error("path %s does not exist" % tp)
            return None
            
            
    def getGraphById(self, t, graphid):
        """
        Given template t and graphid find the graph object
        and return it.
        """
        for g in self.api.getGraphs(t.uid):
            if graphid == g.id: return g
            
            
    def createJMXDatasourceAndHookup(self, t, dsname, dpname, 
                                    gname, jmxoname, jmxport, dstype="JMX"):
        """
        Create the JMXDatasource, datapoint and hook them up to a graph,
        also specifiy the objectname and jmxport.
        """
	    self.log.debug("working on template %s, creating datasource %s" % (t.uid, dsname))
	    #clean up the id for the datasource (replace spaces with _)
	    dsname = prepId(dsname)
	    a = self.api
	    #create the data source and turn it into an info object
	    nds = IRRDDataSourceInfo(a.addDataSource(t.uid, dsname, dstype))
	    #set a bunch of attributes on the data source
	    nds.objectName = jmxoname
	    nds.jmxPort = jmxport
	    #create a datapoint
	    ndp = IDataPointInfo(a.addDataPoint(nds.uid, dpname))
	    #create the graph and associate the datapoint with it
	    a.addGraphDefinition(t.uid, gname)
	    ng = self.getGraphById(t, gname)
	    a.addDataPointToGraph(ndp.uid, ng.uid)
        
    
    def buildOptions(self):
        """
        Add some additional options to the command so they can be specified
        on the command line.
        """
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
        templateCranker.createJMXDatasourceAndHookup(newTemplate, entry[0], entry[2], entry[0], entry[1], "1234")
    
    commit()

