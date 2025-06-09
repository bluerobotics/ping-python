#!/usr/bin/env python

#simpleSurveyor240Example.py
from brping import definitions
from brping import Surveyor240
import time
import argparse

from builtins import input

import signal
import sys
import math

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Surveyor IP:Port. E.g: 192.168.2.86:62312")
parser.add_argument('--tcp', action="store", required=False, type=str, help="Surveyor IP:Port. E.g: 192.168.2.86:62312")
args = parser.parse_args()
if args.device is None and args.udp is None and args.tcp is None:
    parser.print_help()
    exit(1)

# Signal handler to stop pinging on the Surveyor240
def signal_handler(sig, frame):
    print("Stopping pinging on Surveyor240...")
    mySurveyor240.control_set_ping_parameters(ping_enable = False)
    # Close socket if open
    if mySurveyor240.iodev:
        try:
            mySurveyor240.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")

    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Make a new Surveyor240
mySurveyor240 = Surveyor240()
if args.device is not None:
    mySurveyor240.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    mySurveyor240.connect_udp(host, int(port))
elif args.tcp is not None:
    (host, port) = args.tcp.split(':')
    mySurveyor240.connect_tcp(host, int(port))

if mySurveyor240.initialize() is False:
    print("Failed to initialize Surveyor240!")
    exit(1)

data1 = mySurveyor240.get_device_information()
print("Device type: %s" % data1["device_type"])

print("------------------------------------")
print("Starting Surveyor240..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

mySurveyor240.control_set_ping_parameters(
    ping_enable = True,
    enable_yz_point_data = True,
    enable_atof_data = True,
)

print("\n---------Attitude Report---------")
while True:
    data = mySurveyor240.wait_message([definitions.SURVEYOR240_ATTITUDE_REPORT])
    if data:
        vector = (data.up_vec_x, data.up_vec_y, data.up_vec_z)
        pitch = math.asin(vector[0])
        roll = math.atan2(vector[1], vector[2])
        print(f"Pitch: {pitch}\tRoll: {roll}")
        break   # Remove to see continuous pitch and roll data
    else:
        print("Failed to get attitude report")
    time.sleep(0.1)

print("\n---------ATOF Point Data---------")
while True:
    data = mySurveyor240.wait_message([definitions.SURVEYOR240_ATOF_POINT_DATA])
    if data:
        # Use create_atof_list to get formatted atof_t[num_points] list
        atof_data = Surveyor240.create_atof_list(data)
        if len(atof_data) == 0:
            continue
        else:
            for i in range(len(atof_data)):
                distance = 0.5 * data.sos_mps * atof_data[i].tof
                y = distance * math.sin(atof_data[i].angle)
                z = -distance * math.cos(atof_data[i].angle)
                print(f"{i}.\tDistance: {distance:.3f} meters\tY: {y:.3f}\tZ: {z:.3f}\t{atof_data[i]}")
            break
    else:
        print("Failed to get atof point data")

print("\n---------YZ Point Data---------")
while True:
    data = mySurveyor240.wait_message([definitions.SURVEYOR240_YZ_POINT_DATA])
    if data:
        yz_data = Surveyor240.create_yz_point_data(data)
        print(f"Length of yz_data: {len(yz_data)}\tNum_points: {data.num_points}")
        print("Index\tY\tZ")
        for i in range(0, len(yz_data), 2):
            print(f"{i//2}\t{yz_data[i]:.2f}\t{yz_data[i+1]:.2f}")
        break
    else:
        print("Failed to get yz point data")

# Stop pinging from Surveyor
mySurveyor240.control_set_ping_parameters(ping_enable = False)
if mySurveyor240.iodev:
    try:
        mySurveyor240.iodev.close()
    except Exception as e:
        print(f"Failed to close socket: {e}")
