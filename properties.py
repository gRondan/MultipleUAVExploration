import sys
from importlib import import_module

valor = ''
try:
    valor = int(sys.argv[1])
except:
    pass

if valor:
    props = import_module('testCases.properties' + sys.argv[1])
    for i in dir(props):
        globals()[i] = getattr(props, i)
else:
    from baseProperties import *
