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
parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
args = parser.parse_args()
if args.device is None and args.udp is None:
    parser.print_help()
    exit(1)

# Signal handler to stop pinging on the Surveyor240
def signal_handler(sig, frame):
    print("Stopping pinging on Surveyor240...")
    mySurveyor240.control_set_ping_parameters(
    start_mm = 5,
    end_mm = 0,
    sos_mps = 1500,
    gain_index = -1,
    msec_per_ping = 100,
    deprecated=0,
    diagnostic_injected_signal = 0,
    ping_enable = False,
    enable_channel_data = False,
    reserved_for_raw_data = False,
    enable_yz_point_data = True,
    enable_atof_data = True,
    target_ping_hz=240000,
    n_range_steps = 400,
    reserved = 0,
    pulse_len_steps = 1.5
    )
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
    start_mm = 0,
    end_mm = 0,
    sos_mps = 1500,
    gain_index = -1,
    msec_per_ping = 100,
    deprecated=0,
    diagnostic_injected_signal = 0,
    ping_enable = True,
    enable_channel_data = False,
    reserved_for_raw_data = False,
    enable_yz_point_data = True,
    enable_atof_data = True,
    target_ping_hz=240000,
    n_range_steps = 400,
    reserved = 0,
    pulse_len_steps = 1.5
)

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

while True:
    data = mySurveyor240.wait_message([definitions.SURVEYOR240_ATOF_POINT_DATA])
    if data:
        # Use create_atof_list to get formatted atof_t[num_points] list
        atof_data = Surveyor240.create_atof_list(data)
        for i in range(len(atof_data)):
            distance = 0.5 * data.sos_mps * atof_data[i].tof
            y = distance * math.sin(atof_data[i].angle)
            z = -distance * math.cos(atof_data[i].angle)
            print(f"{i}.\tDistance: {distance:.3f} meters\tY: {y:.3f}\tZ: {z:.3f}\t{atof_data[i]}")
        break

    else:
        print("Failed to get attitude report")

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
        print("Failed to get attitude report")

# Stop pinging from Surveyor
mySurveyor240.control_set_ping_parameters(
    start_mm = 5,
    end_mm = 0,
    sos_mps = 1500,
    gain_index = -1,
    msec_per_ping = 100,
    deprecated=0,
    diagnostic_injected_signal = 0,
    ping_enable = False,
    enable_channel_data = False,
    reserved_for_raw_data = False,
    enable_yz_point_data = True,
    enable_atof_data = True,
    target_ping_hz=240000,
    n_range_steps = 400,
    reserved = 0,
    pulse_len_steps = 1.5
    )