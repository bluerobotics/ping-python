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
parser.add_argument('--log', action="store", nargs='?', const=True, type=str, help="Log filename and/or directory path. Will create new log if blank or directory is specified. Will replay if file is specified and exists.")
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

# Check for log argument and make new Surveyor240
# If no .svlog is specified, create one using default directory
# If directory specified, .svlog be created in specified directory
# If a .svlog is specified, existing log will be opened
new_log = False
log_path = ""
replay_path = None
default_dir = Path("logs/surveyor").resolve()
if args.log is not None:
    if args.log is True:
        # Logging to default directory
        default_dir.mkdir(parents=True, exist_ok=True)
        mySurveyor240 = Surveyor240(logging=True, log_directory=default_dir)
        new_log = True
    elif isinstance(args.log, str):
        log_path = Path(args.log).expanduser()

        if log_path.suffix == ".svlog" and log_path.parent == Path("."):
            log_path = default_dir / log_path.name

        log_path = log_path.resolve()

        if log_path.suffix == ".svlog":
            if log_path.exists() and log_path.is_file():
                # File exists, replaying
                new_log = False
                mySurveyor240 = Surveyor240(logging=False)
                replay_path = log_path
                print(f"Replaying from: {replay_path}")
            else:
                raise FileNotFoundError(f"Log file not found: {log_path}")

        elif log_path.is_dir() or log_path.suffix == "":
            # Path is directory, logging to that directory
            mySurveyor240 = Surveyor240(logging=True, log_directory=log_path)
            new_log = True
        
        else:
            raise ValueError(f"Invalid log argument: {args.log}")
else:
    mySurveyor240 = Surveyor240()

if args.log is None or new_log:
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

print("------------------------------------")
print("Starting Surveyor240..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

# Running surveyor240Example.py from existing log file
if args.log is not None and not new_log:
    with open(log_path, 'rb') as f:
        while True:
            data = Surveyor240.read_packet(f)

            if data is None:
                break   # EOF or bad packet
            
            # print(f"ID: {data.message_id}\tName: {data.name}")

            ## Surveyor will report the Water Stats packet if temperature and/or pressure sensor is connected
            # if data.message_id == definitions.SURVEYOR240_WATER_STATS:
            #     print(f"Temperature: {(data.temperature * 9/5) + 32} F")
            #     print(f"Temperature: {data.temperature} C")
            #     print(f"Pressure: {data.pressure} bar")

            if data.message_id == definitions.SURVEYOR240_ATTITUDE_REPORT:
                # Print pitch and roll data
                vector = (data.up_vec_x, data.up_vec_y, data.up_vec_z)
                pitch = math.asin(vector[0])
                roll = math.atan2(vector[1], vector[2])
                print(f"Pitch: {pitch}\tRoll: {roll}")

            # if data.message_id == definitions.SURVEYOR240_YZ_POINT_DATA:
            #      # Display YZ point data in a table
            #     yz_data = Surveyor240.create_yz_point_data(data)
            #     print(f"Length of yz_data: {len(yz_data)}\tNum_points: {data.num_points}")
            #     print("Index\tY\tZ")
            #     for i in range(0, len(yz_data), 2):
            #         print(f"{i//2}\t{yz_data[i]:.2f}\t{yz_data[i+1]:.2f}")
            #     print(f"Temperature: {(data.water_degC * 9/5) + 32} F")
            #     print(f"Temperature: {data.water_degC} C")
            #     print(f"Pressure: {data.water_bar} Bar")

            # if data.message_id == definitions.SURVEYOR240_ATOF_POINT_DATA:
            #     # Just an example packet, could check for other packet types and 
            #     # show results from those too

            #     # Use create_atof_list to get formatted atof_t[num_points] list
            #     atof_data = Surveyor240.create_atof_list(data)
            #     if len(atof_data) == 0:
            #         continue
            #     else:
            #         # Just the first data point in atof[]
            #         distance = 0.5 * data.sos_mps * atof_data[0].tof
            #         y = distance * math.sin(atof_data[0].angle)
            #         z = -distance * math.cos(atof_data[0].angle)
            #         print(f"Distance: {distance:.3f} meters\tY: {y:.3f}\tZ: {z:.3f}\t{atof_data[0]}")

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
        print("Logging...\nCTRL+C to stop logging")
    else:
        print("CTRL-C to end program...")
    try:
        while True:
            # Set multiple packets to listen for
            data = mySurveyor240.wait_message([definitions.SURVEYOR240_ATOF_POINT_DATA,
                                               definitions.SURVEYOR240_ATTITUDE_REPORT,
                                               definitions.SURVEYOR240_YZ_POINT_DATA,
                                               definitions.SURVEYOR240_WATER_STATS])
            
            if data:
                ## To watch pitch and roll data in real time while recording, uncomment this block
                if data.message_id == definitions.SURVEYOR240_ATTITUDE_REPORT:
                    # Print pitch and roll data
                    vector = (data.up_vec_x, data.up_vec_y, data.up_vec_z)
                    pitch = math.asin(vector[0])
                    roll = math.atan2(vector[1], vector[2])
                    print(f"Pitch: {pitch}\tRoll: {roll}")

    except KeyboardInterrupt:
        if new_log:
            print("Stopping logging...")
        

    # Stop pinging from Surveyor
    mySurveyor240.control_set_ping_parameters(ping_enable = False)
    if mySurveyor240.iodev:
        try:
            mySurveyor240.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")
