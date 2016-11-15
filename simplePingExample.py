#!/usr/bin/python -u
#simplePingExample.py
from Ping import Ping1D

#Make a new Ping
myPing = Ping1D()

print("Starting Ping..")
print("Press CTRL+Z to exit. CMD+Z on Mac")
print("------------------------------------")

#Read and print depth measurements with confidence
while True:
    myPing.updateSonar()
    print("Current Depth: " + str(myPing.getDepth()) + " | Confidence: " str(myPing.getConfidence()))
