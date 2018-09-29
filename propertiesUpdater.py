import re
import sys
from random import randint, sample, choice
from utils import convertTupleListToString, convertListToString
from itertools import product
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/testCases/'

for filename in os.listdir(path):
    content = ''
    with open('testCases/' + filename, 'r') as f:
        content = f.read()
    with open('testCases/' + filename, 'w') as f:
        new_content = re.sub(sys.argv[1] + r'.*', sys.argv[1] + '=' + sys.argv[2], content)
        f.write(new_content)
