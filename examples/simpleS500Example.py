#!/usr/bin/env python

#simpleS500Example.py
from brping import definitions
from brping import S500
import time
import argparse

from builtins import input

import signal
import sys

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
parser.add_argument('--tcp', action="store", required=False, type=str, help="Sounder IP:Port. E.g: 192.168.2.86:51200")
args = parser.parse_args()
if args.device is None and args.udp is None and args.tcp is None:
    parser.print_help()
    exit(1)

# Signal handler to stop pinging on the S500
def signal_handler(sig, frame):
    print("Stopping pinging on S500...")
    myS500.control_set_ping_params(report_id=0)
    if myS500.iodev:
        try:
            myS500.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Make a new S500
myS500 = S500()
if args.device is not None:
    myS500.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    myS500.connect_udp(host, int(port))
elif args.tcp is not None:
    (host, port) = args.tcp.split(':')
    myS500.connect_tcp(host, int(port))

if myS500.initialize() is False:
    print("Failed to initialize S500!")
    exit(1)

data1 = myS500.get_device_information()
print("Device type: %s" % data1["device_type"])

print("------------------------------------")
print("Starting S500..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

print("\n-------Distance2-------")
# Tell S500 to send distance2 data
myS500.control_set_ping_params(
    msec_per_ping=0,
    report_id=definitions.S500_DISTANCE2,
    chirp=1
)

# Read and print distance2 data
data = myS500.wait_message([definitions.S500_DISTANCE2])
if data:
    print(f"Ping Distance: {data.ping_distance_mm} mm")
    print(f"Confidence: {data.ping_confidence}")
    print(f"Average Distance: {data.averaged_distance_mm} mm")
    print(f"Confidence of Average: {data.average_distance_confidence}")
    print(f"Timestamp: {data.timestamp}")

print("\n-------Profile6-------")
# Tell S500 to send profile6 data
myS500.control_set_ping_params(
    msec_per_ping=0,
    report_id=definitions.S500_PROFILE6_T,
    chirp=1,
)

# Read and print profile6 data
data = myS500.wait_message([definitions.S500_PROFILE6_T])
if data:
    scaled_result = S500.scale_power(data)

    if (data.num_results > 100):
        for i in range(5):
            print(f"{i}:\tNot Scaled: {data.pwr_results[i]}  |  Scaled: {scaled_result[i]:.2f} dB")
        print(".\n.\n.")
        for i in range(5, 0, -1):
            print(f"{data.num_results-i}:\tNot Scaled: {data.pwr_results[data.num_results-i]}  |  Scaled: {scaled_result[data.num_results-i]:.2f} dB")
    else:
        for i in range(len(scaled_result)):
            print(f"{i+1}:\tNot scaled: {data.pwr_results[i]}  |  Scaled: {scaled_result[i]:.2f} dB")

    print(f"Number of results: {data.num_results}")
    print(f"Min power: {data.min_pwr_db} dB")
    print(f"Max power: {data.max_pwr_db} dB")
    # print(data)

else:
    print("Failed to get profile6 data")

# Stop pinging
myS500.control_set_ping_params(report_id=0)
if myS500.iodev:
    try:
        myS500.iodev.close()
    except Exception as e:
        print(f"Failed to close socket: {e}")