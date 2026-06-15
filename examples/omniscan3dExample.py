#!/usr/bin/env python

#omniscan3dExample.py
from brping import definitions
from brping import Omniscan3D
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
parser.add_argument('--tcp', action="store", required=False, type=str, help="Omniscan3D IP:Port. E.g: 192.168.2.86:62312")
parser.add_argument('--range', action="store", required=False, type=str, help="Set range. E.g: 5000 or 0:5000")
parser.add_argument('--log', action="store", nargs='?', const=True, type=str, help="Log filename and/or directory path. Will create new log if blank or directory is specified. Will replay if file is specified and exists.")
args = parser.parse_args()
if args.device is None and args.tcp is None and args.log is None:
    parser.print_help()
    exit(1)

# Signal handler to stop pinging on the Omniscan3D
def signal_handler(sig, frame):
    print("Stopping pinging on Omniscan3D...")
    myOmniscan3D.control_os3d_set_ping_params(ping_enable = False)
    # Close socket if open
    if myOmniscan3D.iodev:
        try:
            myOmniscan3D.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Check for log argument and make new Omniscan3D
# If no .svlog is specified, create one using default directory
# If directory specified, .svlog be created in specified directory
# If a .svlog is specified, existing log will be opened
new_log = False
log_path = ""
replay_path = None
default_dir = Path("logs/omniscan3d").resolve()
if args.log is not None:
    if args.log is True:
        # Logging to default directory
        default_dir.mkdir(parents=True, exist_ok=True)
        myOmniscan3D = Omniscan3D(logging=True, log_directory=default_dir)
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
                myOmniscan3D = Omniscan3D(logging=False)
                replay_path = log_path
                print(f"Replaying from: {replay_path}")
            else:
                raise FileNotFoundError(f"Log file not found: {log_path}")

        elif log_path.is_dir() or log_path.suffix == "":
            # Path is directory, logging to that directory
            myOmniscan3D = Omniscan3D(logging=True, log_directory=log_path)
            new_log = True
        
        else:
            raise ValueError(f"Invalid log argument: {args.log}")
else:
    myOmniscan3D = Omniscan3D()

if args.log is None or new_log:
    if args.device is not None:
        myOmniscan3D.connect_serial(args.device, args.baudrate)
    elif args.tcp is not None:
        (host, port) = args.tcp.split(':')
        try:
            myOmniscan3D.connect_tcp(host, int(port))
        except Exception as e:
            print(f"Could not connect to Omniscan3D at {host}:{port}")
            print(f"Reason: {e}")
            sys.exit(1)

    if myOmniscan3D.initialize() is False:
        print("Failed to initialize Omniscan3D!")
        exit(1)

print("------------------------------------")
print("Starting Omniscan3D..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

# Running omniscan3d.py from existing log file
if args.log is not None and not new_log:
    with open(log_path, 'rb') as f:
        while True:
            data = Omniscan3D.read_packet(f)

            if data is None:
                break   # EOF or bad packet
            
            # print(f"ID: {data.message_id}\tName: {data.name}")

            if data.message_id == definitions.OMNISCAN3D_ATTITUDE_REPORT:
                # Print pitch and roll data
                vector = (data.up_vec_x, data.up_vec_y, data.up_vec_z)
                pitch = math.asin(vector[0])
                roll = math.atan2(vector[1], vector[2])
                print(f"Pitch: {pitch}\tRoll: {roll}")
            elif data.message_id == definitions.OMNISCAN3D_OS3D_POINT_SET:
                # print out data
                print(f"ping_number        : {data.ping_number}")
                print(f"sos_mps            : {data.sos_mps}")
                print(f"num_points         : {data.num_points}")
                print(f"utc_msec           : {data.utc_msec}")
                print(f"pwr_up_msec        : {data.pwr_up_msec}")
                print(f"version            : {data.version}")
                print(f"device_number      : {data.device_number}")
                print(f"pwr_threshold_high : {data.pwr_threshold_high}")
                print(f"pwr_threshold_med  : {data.pwr_threshold_med}")
                print(f"pwr_threshold_low  : {data.pwr_threshold_low}")
            elif data.message_id == definitions.OMNISCAN3D_END_PING_INFO:
                # print out data
                print("got OS3D_END_PING_INFO packet")
                
# Connected to physical Omniscan3D
else:
    if args.range is not None:
        parts = args.range.split(':')

        if len(parts) == 2:
            myOmniscan3D.control_os3d_set_ping_params(
                start_m=int(parts[0]),
                end_m=int(parts[1]),
                ping_enable=True,
                enable_atof_data=True
            )
        elif len(parts) == 1:
            myOmniscan3D.control_os3d_set_ping_params(
                start_m=0,
                end_m=int(parts[0]),
                ping_enable=True,
                enable_atof_data=True
            )
        else:
            print("Invalid range input, using default range")
            myOmniscan3D.control_os3d_set_ping_params(
                ping_enable=True,
                enable_atof_data=True
            )
    else:
        print("start_m=0, end_m-=7, msec_per_ping=100, sos_mps=1500, ping_enable = True, enable_atof_data = True")
        myOmniscan3D.control_os3d_set_ping_params(
            start_m=0,
            end_m=7,
            msec_per_ping=200,
            diagnostic_injected_signal = 1,
            sos_mps=1500,
            ping_enable = True,
            enable_atof_data = True
        )

    if new_log:
        print("Logging...\nCTRL+C to stop logging")
    else:
        print("CTRL-C to end program...")
    try:
        while True:
            # Set multiple packets to listen for
            data = myOmniscan3D.wait_message([definitions.OMNISCAN3D_ATTITUDE_REPORT,
                                               definitions.OMNISCAN3D_OS3D_POINT_SET,
                                               definitions.OMNISCAN3D_END_PING_INFO])
            
            if data:
                ## To watch pitch and roll data in real time while recording, uncomment this block
                if data.message_id == definitions.OMNISCAN3D_ATTITUDE_REPORT:
                    # Print pitch and roll data
                    vector = (data.up_vec_x, data.up_vec_y, data.up_vec_z)
                    pitch = math.asin(vector[0])
                    roll = math.atan2(vector[1], vector[2])
                    print(f"Pitch: {pitch}\tRoll: {roll}")
                elif data.message_id == definitions.OMNISCAN3D_OS3D_POINT_SET:
                    # print out data
                    print(f"ping_number        : {data.ping_number}")
                    print(f"sos_mps            : {data.sos_mps}")
                    print(f"num_points         : {data.num_points}")
                    print(f"utc_msec           : {data.utc_msec}")
                    print(f"pwr_up_msec        : {data.pwr_up_msec}")
                    print(f"version            : {data.version}")
                    print(f"device_number      : {data.device_number}")
                    print(f"pwr_threshold_high : {data.pwr_threshold_high}")
                    print(f"pwr_threshold_med  : {data.pwr_threshold_med}")
                    print(f"pwr_threshold_low  : {data.pwr_threshold_low}")
 
    except KeyboardInterrupt:
        if new_log:
            print("Stopping logging...")
        

    # Stop pinging from Omniscan3D
    myOmniscan3D.control_os3d_set_ping_params(ping_enable = False)
    if myOmniscan3D.iodev:
        try:
            myOmniscan3D.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")
