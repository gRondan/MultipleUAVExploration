import sys
from importlib import import_module
if(len(sys.argv) > 1):
    props = import_module('testCases.properties' + sys.argv[1])
    for i in dir(props):
        globals()[i] = getattr(props, i)
else:
    from baseProperties import *
