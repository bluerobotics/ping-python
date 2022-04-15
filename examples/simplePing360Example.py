#!/usr/bin/env python

#simplePing360Example.py
from brping import Ping360
import time
import argparse

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example (Ping360).",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--device', help="Ping360 device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', type=int, default=115200, help="Ping360 device baudrate. E.g: 115200")
parser.add_argument('--udp', help="Ping360 UDP server. E.g: 192.168.2.2:9092")
args = parser.parse_args()
if args.device is None and args.udp is None:
    parser.print_help()
    exit(1)

# Make a new Ping
device = Ping360()
if args.device is not None:
    device.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    device.connect_udp(host, int(port))

with device:
    line = "-" * 40
    print(line)
    print("Starting Ping360...")
    print("Press CTRL+C to exit")
    print(line)
    
    input("Press Enter to continue...")

    # Read and print 
    while "user hasn't quit":
        
# Read and print distance measurements with confidence
while True:
    data = myPing.get_distance()
    if data:
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Failed to get distance data")
    time.sleep(0.1)
