#!/usr/bin/env python

from brping import Ping1D
import time
import argparse

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=True, type=str, help="Ping device port.")
args = parser.parse_args()

#Make a new Ping
myPing = Ping1D(args.device)

baudrates = [9600, 115200]

while (True):
    for baudrate in baudrates:
        if not myPing.initialize(baudrate):
            print("failed to initialize at %d bps", baudrate)
            exit(1)
        print("ok")
    time.sleep(0.01)
