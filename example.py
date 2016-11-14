#!/usr/bin/python -u
#example.py
from Ping import Ping1D

#Make a new Ping
myPing = Ping1D()

#Read and print three depth measurements
for x in range(0,3):
    myPing.updateSonar()
    print(myPing.getDepth())

#This prints the values in the depth profile
#print(myPing.getResults())
