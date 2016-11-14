#!/usr/bin/python -u
#example.py
from Ping import Ping1D

#Make a new Ping
myPing = Ping1D()

#Read and print three depth measurements
while True:
    myPing.updateSonar()
    print("Current Depth: " + str(myPing.getDepth()))


#This prints the values in the depth profile
#print(myPing.getResults())
