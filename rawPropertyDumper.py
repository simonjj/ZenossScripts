from Products.ZenModel.DeviceHW import Hardware
from Products.ZenModel.Device import Device
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.zendmd import ZenCompleter

def ignore(name):
    if name in ZenCompleter.ignored_names:
        return True
    for p in ZenCompleter.ignored_prefixes:
        if name.startswith(p):
            return True
    return False

def processClass(mclass, ofile):
    ofile.write("Class %r\n" % mclass)
    ofile.write("  Properties:\n")
    for p in mclass._properties:
        if not ignore(p['id']): ofile.write("    " + p['id'] + "\n")
    #TODO: enable listing of methods as well
    #for m in dir(mclass):
    #    print m
    #    if not ignore(m): print m
    
    
mf = open("/tmp/allprops.txt", "w")
for mc in [Hardware, Device, OperatingSystem, DeviceComponent]:
    for c in mc.__subclasses__(): processClass(c, mf)
