#!/usr/bin/python -u

#simplePingExample.py
from Ping import Ping1D
import sys
import getopt
import time
import argparse

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Driver for the Water Linked Underwater GPS system.")
parser.add_argument('--device', action="store", required=True, type=str, help="Ping device port.")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate.")
args = parser.parse_args()

#Make a new Ping
myPing = Ping1D(args.device, args.baudrate)
if myPing.initialize() is False:
    print "Failed to initialize Ping!"
    exit(1)

print("------------------------------------")
print("Starting Ping..")
print("Press CTRL+Z to exit")
print("------------------------------------")

raw_input("Press Enter to continue...")

# Read and print distance measurements with confidence
while True:
    myPing.getDistanceData()
    print("Distance: " + str(myPing.distance) + " Confidence: " + str(myPing.confidence))
    time.sleep(0.1)
