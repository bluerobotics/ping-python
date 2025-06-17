#!/usr/bin/env python

#simpleS500Example.py
from brping import definitions
from brping import S500
from brping import PingMessage
import time
import argparse

from builtins import input

import signal
import sys
import os
from datetime import datetime
from pathlib import Path

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
parser.add_argument('--tcp', action="store", required=False, type=str, help="Sounder IP:Port. E.g: 192.168.2.86:51200")
parser.add_argument('--range', action="store", required=False, type=str, help="Set range. E.g: 5000 or 0:5000")
parser.add_argument('--log', action="store", nargs='?', const=True, type=str, help="Log filename or foldername. Will log if it doesn't exist, or replay if it does. Blank creates new log.")
args = parser.parse_args()
if args.device is None and args.udp is None and args.tcp is None and args.log is None:
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

# Check for log argument
# If no log is specified, create one using date and time
# If a log is specified, existing log will be opened
new_log = False
new_folder_name = None
if args.log is not None:
    if args.log is True:
        new_log = True
    elif isinstance(args.log, str):
        log_path = os.path.join("logs/sounder", args.log)
        if args.log.endswith(".txt"):
            new_log = False
        elif os.path.exists(log_path):
            print(f"Replaying from existing log folder: {log_path}")
            new_log = False
        else:
            new_folder_name = args.log
            new_log = True

if args.log is None or new_log:
    if myS500.initialize() is False:
        print("Failed to initialize S500!")
        exit(1)

print("------------------------------------")
print("Starting S500..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

# Running S500 from existing log file
if args.log is not None and not new_log:
    log_path = Path("logs/sounder") / args.log
    if not log_path.exists():
        print(f"Log path does not exist: {log_path}")
        sys.exit(1)
    
    if log_path.is_dir():
        for file in sorted(log_path.iterdir()):
            if file.suffix == ".txt":
                print(f"\n---------Replaying File: {file.name}---------")
                with open(file, 'rb') as f:
                    raw_bytes = f.read()
                    data = PingMessage(msg_data=raw_bytes)
                
                if data:
                    print(data)
                else:
                    print("Failed to get report")
    elif log_path.is_file():
        print(f"\n---------Replaying File: {log_path.name}---------")
        with open(log_path, 'rb') as f:
            raw_bytes = f.read()
            data = PingMessage(msg_data=raw_bytes)
        
        if data:
            print(data)
        else:
            print("Failed to get report")
    else:
        print(f"Invalid log path: {log_path}")

# Connected to physical S500
else:
    if new_log:
        if new_folder_name is None:
            log_folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        else:
            log_folder_name = new_folder_name
        log_path = os.path.join("logs/sounder", log_folder_name)
        os.makedirs(log_path, exist_ok=True)
        print(f"Logging new files in: {log_path}")

    print("\n-------Distance2-------")
    if args.range is not None:
        parts = args.range.split(':')
        # Tell S500 to send distance 2 data
        if len(parts) == 2:
            myS500.control_set_ping_params(
                start_mm=int(parts[0]),
                length_mm=int(parts[1]),
                msec_per_ping=0,
                report_id=definitions.S500_DISTANCE2,
                chirp=1
            )
        elif len(parts) == 1:
            myS500.control_set_ping_params(
                start_mm=0,
                length_mm=int(parts[0]),
                msec_per_ping=0,
                report_id=definitions.S500_DISTANCE2,
                chirp=1
            )
        else:
            print("Invalid range input, using default range")
            myS500.control_set_ping_params(
                msec_per_ping=0,
                report_id=definitions.S500_DISTANCE2,
                chirp=1
            )   
    else:
        myS500.control_set_ping_params(
            msec_per_ping=0,
            report_id=definitions.S500_DISTANCE2,
            chirp=1
        )

    # Read and print distance2 data
    data = myS500.wait_message([definitions.S500_DISTANCE2])
    if data:
        # Create new log if specified
        if new_log:
            distance2_path = os.path.join(log_path, "Distance2.txt")
            with open(distance2_path, 'ab') as f:
                f.write(data.msg_data)

        print(f"Ping Distance: {data.ping_distance_mm} mm")
        print(f"Confidence: {data.ping_confidence}")
        print(f"Average Distance: {data.averaged_distance_mm} mm")
        print(f"Confidence of Average: {data.average_distance_confidence}")
        print(f"Timestamp: {data.timestamp}")

    print("\n-------Profile6-------")
    # Tell S500 to send profile6 data
    if args.range is not None:
        parts = args.range.split(':')
        # Tell S500 to send distance 2 data
        if len(parts) == 2:
            myS500.control_set_ping_params(
                start_mm=int(parts[0]),
                length_mm=int(parts[1]),
                msec_per_ping=0,
                report_id=definitions.S500_PROFILE6_T,
                chirp=1
            )
        elif len(parts) == 1:
            myS500.control_set_ping_params(
                start_mm=0,
                length_mm=int(parts[0]),
                msec_per_ping=0,
                report_id=definitions.S500_PROFILE6_T,
                chirp=1
            )
        else:
            print("Invalid range input, using default range")
            myS500.control_set_ping_params(
                msec_per_ping=0,
                report_id=definitions.S500_PROFILE6_T,
                chirp=1
            )   
    else:
        myS500.control_set_ping_params(
            msec_per_ping=0,
            report_id=definitions.S500_PROFILE6_T,
            chirp=1
        )

    # Read and print profile6 data
    data = myS500.wait_message([definitions.S500_PROFILE6_T])
    if data:
        # Create new log if specified
        if new_log:
            profile6_path = os.path.join(log_path, "Profile6.txt")
            with open(profile6_path, 'ab') as f:
                f.write(data.msg_data)

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