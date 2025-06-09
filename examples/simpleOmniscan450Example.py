#!/usr/bin/env python

#simpleOmniscan450Example.py
from brping import definitions
from brping import Omniscan450
import time
import argparse

from builtins import input

import signal
import sys
import struct

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
args = parser.parse_args()
if args.device is None and args.udp is None:
    parser.print_help()
    exit(1)

# Signal handler to stop pinging on the Omniscan450
def signal_handler(sig, frame):
    print("Stopping pinging on Omniscan450...")
    myOmniscan450.control_os_ping_params(
    start_mm=0,
    length_mm=0,
    msec_per_ping=0,
    reserved_1=0,
    reserved_2=0,
    pulse_len_percent=0.002,
    filter_duration_percent=0.0015,
    gain_index=-1,
    num_results=600,
    enable=0,
    reserved_3=0
    )
    if myOmniscan450.iodev:
        try:
            myOmniscan450.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Make a new Surveyor240
myOmniscan450 = Omniscan450()
if args.device is not None:
    myOmniscan450.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    myOmniscan450.connect_udp(host, int(port))

if myOmniscan450.initialize() is False:
    print("Failed to initialize Omniscan450!")
    exit(1)

data1 = myOmniscan450.get_device_information()
print("Device type: %s" % data1["device_type"])

print("------------------------------------")
print("Starting Omniscan450..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

myOmniscan450.control_os_ping_params(
    start_mm=0,
    length_mm=0,
    msec_per_ping=0,
    reserved_1=0,
    reserved_2=0,
    pulse_len_percent=0.002,
    filter_duration_percent=0.0015,
    gain_index=-1,
    num_results=600,
    enable=1,
    reserved_3=0
)

# View power results
data = myOmniscan450.wait_message([definitions.OMNISCAN450_OS_MONO_PROFILE])
if data:
    scaled_result = Omniscan450.scale_power(data)
    for i in range(len(scaled_result)):
        print(f"{i+1}: Raw: {data.pwr_results[i]}\tScaled: {scaled_result[i]}dB")
    print(f"Min power: {data.min_pwr_db} dB")
    print(f"Max power: {data.max_pwr_db} dB")
else:
    print("Failed to get report")
