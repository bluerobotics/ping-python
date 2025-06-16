#!/usr/bin/env python

#simpleSurveyor240Example.py
from brping import definitions
from brping import Surveyor240
from brping import PingMessage
import time
import argparse

from builtins import input

import signal
import sys
import math
import os
from datetime import datetime
from pathlib import Path

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Surveyor IP:Port. E.g: 192.168.2.86:62312")
parser.add_argument('--tcp', action="store", required=False, type=str, help="Surveyor IP:Port. E.g: 192.168.2.86:62312")
parser.add_argument('--range', action="store", required=False, type=str, help="Set range. E.g: 5000 or 0:5000")
parser.add_argument('--log', action="store", nargs='?', const=True, type=str, help="Log filename or folder name. Will log if it doesn't exist, or replay all packets inside directory if it does. Left blank creates new log.")
args = parser.parse_args()
if args.device is None and args.udp is None and args.tcp is None and args.log is None:
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

# Check for log argument
# If no log is specified, create one using date and time
# If a log is specified, existing log will be opened
new_log = False
new_folder_name = None
if args.log is not None:
    if args.log is True:
        new_log = True
    elif isinstance(args.log, str):
        log_path = os.path.join("logs/surveyor", args.log)
        if args.log.endswith(".txt"):
            new_log = False
        elif os.path.exists(log_path):
            print(f"Replaying from existing log folder: {log_path}")
            new_log = False
        else:
            new_folder_name = args.log
            new_log = True

if args.log is None or new_log:
    if mySurveyor240.initialize() is False:
        print("Failed to initialize Surveyor240!")
        exit(1)

print("------------------------------------")
print("Starting Surveyor240..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

# Running Surveyor240 from existing log file
if args.log is not None and not new_log:
    log_path = Path("logs/surveyor") / args.log
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

# Connected to physical Surveyor
else:
    if args.range is not None:
        parts = args.range.split(':')

        if len(parts) == 2:
            mySurveyor240.control_set_ping_parameters(
                start_mm=int(parts[0]),
                end_mm=int(parts[1]),
                ping_enable=True,
                enable_yz_point_data=True,
                enable_atof_data=True
            )
        elif len(parts) == 1:
            mySurveyor240.control_set_ping_parameters(
                start_mm=0,
                end_mm=int(parts[0]),
                ping_enable=True,
                enable_yz_point_data=True,
                enable_atof_data=True
            )
        else:
            print("Invalid range input, using default range")
            mySurveyor240.control_set_ping_parameters(
                ping_enable=True,
                enable_yz_point_data=True,
                enable_atof_data=True
            )
    else: 
        mySurveyor240.control_set_ping_parameters(
            ping_enable = True,
            enable_yz_point_data = True,
            enable_atof_data = True,
        )

    if new_log:
        if new_folder_name is None:
            log_folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        else:
            log_folder_name = new_folder_name
        log_path = os.path.join("logs/surveyor", log_folder_name)
        os.makedirs(log_path, exist_ok=True)
        print(f"Logging new files in: {log_path}")

    print("\n---------Attitude Report---------")
    while True:
        data = mySurveyor240.wait_message([definitions.SURVEYOR240_ATTITUDE_REPORT])
        if data:
            # Create new log if specified
            if new_log:
                attitude_data_path = os.path.join(log_path, "Attitude_Report.txt")
                with open(attitude_data_path, 'ab') as f:
                    f.write(data.msg_data)

            # Print pitch and roll data
            vector = (data.up_vec_x, data.up_vec_y, data.up_vec_z)
            pitch = math.asin(vector[0])
            roll = math.atan2(vector[1], vector[2])
            print(f"Pitch: {pitch}\tRoll: {roll}")
            break 
        else:
            print("Failed to get attitude report")
        time.sleep(0.1)

    print("\n---------ATOF Point Data---------")
    while True:
        data = mySurveyor240.wait_message([definitions.SURVEYOR240_ATOF_POINT_DATA])
        if data:
            if new_log:
                atof_data_path = os.path.join(log_path, "ATOF_Point_Data.txt")
                with open(atof_data_path, 'ab') as f:
                    f.write(data.msg_data)

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
            if new_log:
                yz_data_path = os.path.join(log_path, "YZ_Point_Data.txt")
                with open(yz_data_path, 'ab') as f:
                    f.write(data.msg_data)

            # Display YZ point data in a table
            yz_data = Surveyor240.create_yz_point_data(data)
            print(f"Length of yz_data: {len(yz_data)}\tNum_points: {data.num_points}")
            print("Index\tY\tZ")
            for i in range(0, len(yz_data), 2):
                print(f"{i//2}\t{yz_data[i]:.2f}\t{yz_data[i+1]:.2f}")
            print(f"Temperature: {(data.water_degC * 9/5) + 32} F")
            print(f"Temperature: {data.water_degC} C")
            print(f"Pressure: {data.water_bar} Bar")
            break
        else:
            print("Failed to get yz point data")

    print("\n---------Water Stats---------")
    while True:
        data = mySurveyor240.wait_message([definitions.SURVEYOR240_WATER_STATS])
        if data:
            if new_log:
                water_stats_path = os.path.join(log_path, "Water_Stats.txt")
                with open(water_stats_path, 'ab') as f:
                    f.write(data.msg_data)

            print(f"Temperature: {(data.temperature * 9/5) + 32} F")
            print(f"Temperature: {data.temperature} C")
            print(f"Pressure: {data.pressure} bar")
            break
        else:
            print("Failed to get water stats data")

    # Stop pinging from Surveyor
    mySurveyor240.control_set_ping_parameters(ping_enable = False)
    if mySurveyor240.iodev:
        try:
            mySurveyor240.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")
