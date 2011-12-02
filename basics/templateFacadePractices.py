#get a hold of API
from Products.Zuul import getFacade
a = getFacade("template")


#listing all of the templates
for template in a.getTemplates("/zport/dmd/Devices"):
#printing the "raw" info object
    print template
#printing the ID of the the object
    print template.id
    print template.getName()
    

#filtering out one particular template
for template in a.getTemplates("/zport/dmd/Devices"):
    if template.id == "ZenJMX":
        break
        
        
#accessing/retrieving one particular template
for template in a.getTemplates("/zport/dmd/Devices/rrdTemplates/copy_of_ZenJMX"): 
    print template
    

#copying a template
a.copyTemplate(TEMPLATE_UID_TO_COPY, TARGET_UID_FOR_THE_TARGET)
c.copyTemplate(template.uid, "/zport/dmd/Devices/Server/Tomcat")



#listing all the datasource for one template
for ds in a.getDataSources("/zport/dmd/Devices/rrdTemplates/ZenJMX_EAN_Hotels_7606"): print ds


#changing the jmxPort on a template
for ds in a.getDataSources("/zport/dmd/Devices/rrdTemplates/ZenJMX_EAN_Hotels_7606"):
    ds.jmxPort = 7606


#list out and append 7606 to the graph definitions
for g in a.getGraphs(myt.uid):
    print g
    g.name += " 7606"
    

#add a new template to a certain device class
a.addTemplate("My New Template Name", "/zport/dmd/Devices/Server/SSH/Linux/ClickServers")



# SUPPORTED DATA SOURCE TYPES
SNMP
COMMAND
Built-In
PING
GangliaMonitor
ApacheMonitor
Cisco UCS XML API
DigMonitor
DnsMonitor
FtpMonitor
HttpMonitor
IRCDMonitor
JabberMonitor
LDAPMonitor
MySqlMonitor
NNTPMonitor
NtpMonitor
RPCMonitor
Splunk
CWMonitor
JMX 
MAILTX
SQL 
VMware
WebTx
WinPerf
vCloudStatus
vCloud

#create a new datasource specifiying:
# 1. the uid of the template to which attach the datasource to
# 2. the name/id of the template
# 3. the type of the datasource (see above)
a.addDataSource(t.uid, "myfirstautomaticjmxdatasource", "JMX")


#creating a datapoint on the previous template
a.addDataPoint(ds.uid, "howdyyall")


#looping and adding 10 datasources of type jmx to one template
for i in range(10):
    a.addDataSource(t.uid, "myfirstautomaticjmxdatasource%s" % i, "JMX")


#adding the same datapoint to the different datasource from above
for ds in a.getDataSources(t.uid):
    a.addDataPoint(ds.uid, "thisisthesamedatapointforall")

# adding a graph definition to the template
a.addGraphDefinition(t.uid, "mygraph")


#retrieve a datapoint info object to further work with (e.g. add to graphs)
from Products.Zuul.interfaces import IDataPointInfo
# access all the datapoints from the datasource (using the detour via the real object)
ds._object.getRRDDataPoints()
#this returns all the datapoints for the template as an array
[<RRDDataPoint at /zport/dmd/Devices/rrdTemplates/SimonTest/datasources/

# accessing the first object in the array and turn it into a infor object to use
dp = ds._object.getRRDDataPoints()[0]
dpi = IDataPointInfo(dp)
dpi.uid

# adding a datapoint to a graph using:
# 1. the uid of the datapoint
# 2. the uid of the graph
a.addDataPointToGraph(dpi.uid, g.uid)

def getGraphById(t, graphid):
    for g in a.getGraphs(t.uid):
        if graphid == g.id: return g


#this method combines all the previous things into one
def mystuff(t, dsname, dpname, gname, type="JMX"):
    from Products.Zuul.interfaces import IDataPointInfo, IRRDDataSourceInfo, IGraphInfo
    print "woring on %s" % dsname
    nds = IRRDDataSourceInfo(a.addDataSource(t.uid, dsname, type))
    print "created datasource"
    ndp = IDataPointInfo(a.addDataPoint(nds.uid, dpname))
    print "created data point"
    a.addGraphDefinition(t.uid, gname)
    ng = getGraphById(t, gname)
    print "created graph def."
    a.addDataPointToGraph(ndp.uid, ng.uid)
    print "done"


# reading in a file
# open the file
myfile = open("/tmp/path/tofile/blah". "r")
# read in the lines and strip the newline chart off the end
lines = [l.strip() for l in myfile.readlines()]
# create an array to hold the data
dsdata = []
#split all the lines and add them to data array
for l in lines:
    dsdata.append(l.split())
    

