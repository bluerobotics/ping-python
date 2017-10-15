#!/usr/bin/python -u
from Ping import Ping1D
import sys
import getopt
from dronekit import connect
import time
import csv

address = 'localhost'
port = 9000

vehicle = connect('udpout:'+address+':'+str(port),wait_ready=False)

device = ''
instructions = "Usage: python simplePingExample.py -d <device_name>"

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
    file = "/home/pi/sonar-logs/sonar-"+time.strftime("%Y-%m-%d-%H-%M-%S")+".csv"

fout = open(str(file),'wb')
writer = csv.writer(fout,delimiter=',')

#Make a new Ping
myPing = Ping1D(device)
print()
print("------------------------------------")
print("Starting Sonar/GPS Log")
print("------------------------------------")

#Read and print distance measurements with confidence
writer.writerow(["distance","confidence","lat","lon"])
fout.close()

while True:
    myPing.getDistanceData()
    print("Current Distance: " + str(myPing.distance) + " | Confidence: " + str(myPing.confidence) + " | Lat: " + str(vehicle.location.global_frame.lat) + " | Lon: " + str(vehicle.location.global_frame.lon))
    fout = open(str(file),'a')
    writer = csv.writer(fout,delimiter=',')
    writer.writerow([str(myPing.distance),str(myPing.confidence),str(vehicle.location.global_frame.lat),str(vehicle.location.global_frame.lon)])
    fout.close()
    time.sleep(0.2)


