import numpy
import sys

data = sys.argv[1]

if (len(sys.argv)>2):
    for i in range(len(sys.argv)-2):
        data = data+"-"+sys.argv[i+2]


for i in range(30):
    print(data)