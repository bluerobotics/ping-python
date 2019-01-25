#!/usr/bin/python -u

#simplePingExample.py
from brping import Ping1D
import time
import argparse

from builtins import input

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=True, type=str, help="Ping device port.")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate.")
args = parser.parse_args()

#Make a new Ping
myPing = Ping1D(args.device, args.baudrate)
if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

print("------------------------------------")
print("Starting Ping..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

# Read and print distance measurements with confidence
while True:
    data = myPing.get_distance()
    if data:
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Failed to get distance data")
    time.sleep(0.1)
