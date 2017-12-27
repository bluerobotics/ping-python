#!/usr/bin/python -u
from Ping import Ping1D
import Message

import sys
import getopt
#from dronekit import connect
import time
import csv

import os
from os.path import expanduser

#2to3
from builtins import bytes

#address = 'localhost'
#port = 9000
#vehicle = connect('udpout:'+address+':'+str(port),wait_ready=False)

device = ''
instructions = "Usage: python rawSurvey.py -d <device_name>"

##Parse Command line options
############################
try:
    options, remainder = getopt.getopt(sys.argv[1:],"hd:f:",["help", "device=", "file="])
except:
    print(instructions)
    exit(1)

file = ''

for opt, arg in options:
    if opt in ('-h', '--help'):
        print(instructions)
        exit(1)
    elif opt in ('-d', '--device'):
        if (arg != ''):
            device = arg
    elif opt in ('-f', '--file'):
	if (arg != ''):
	    file = arg
    else:
        print(instructions)
        exit(1)

if (file is ''):
    path = "{0}/sonar-logs/".format(expanduser("~"))
    filename = "raw-{0}.ping_packets1".format(time.strftime("%Y-%m-%d-%H-%M-%S"))
    #Check if path exist and create it
    if not os.path.exists(path):
        os.makedirs(path)
    file = path + filename

fout = open(str(file),'wb')
writer = csv.writer(fout,delimiter=',')

#Make a new Ping
myPing = Ping1D(device)
myPing.initialize()

print()
print("------------------------------------")
print("Starting Raw Data Log")
print("------------------------------------")

#Read and print distance measurements with confidence
#writer.writerow(["distance","confidence","lat","lon"])
fout.close()

while True:
    myPing.getRawData()
    rawHeader   = myPing.raw_header
    rawData     = myPing.raw_data
    rawChecksum = myPing.raw_checksum
    print()
    print("Recording Raw Data Sample")
    print(bytes(rawHeader))
    print(bytes(rawData))
    print(bytes(rawChecksum))
    print()
    #print("Current Distance: " + str(myPing.distance) + " | Confidence: " + str(myPing.confidence) + " | Lat: " + str(vehicle.location.global_frame.lat) + " | Lon: " + str(vehicle.location.global_frame.lon))
    fout = open(str(file),'ab')
    fout.write(rawHeader)
    fout.write(rawData)
    fout.write(rawChecksum)
    #writer = csv.writer(fout,delimiter=',')
    #writer.writerow([str(myPing.distance),str(myPing.confidence),str(vehicle.location.global_frame.lat),str(vehicle.location.global_frame.lon)])
    #writer.writerow([rawData])
    fout.close()
    time.sleep(1)


