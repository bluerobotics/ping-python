#!/usr/bin/env python

#simpleOmniscan450Example.py
from brping import definitions
from brping import Omniscan450
from brping import PingMessage
import time
import argparse

from builtins import input

import signal
import sys
from pathlib import Path
from datetime import datetime

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
parser.add_argument('--udp', action="store", required=False, type=str, help="Omniscan IP:Port. E.g: 192.168.2.92:51200")
parser.add_argument('--tcp', action="store", required=False, type=str, help="Omniscan IP:Port. E.g: 192.168.2.92:51200")
parser.add_argument('--range', action="store", required=False, type=str, help="Set range. E.g: 5000 or 0:5000")
parser.add_argument('--log', action="store", nargs='?', const=True, type=str, help="Log filename and/or directory path. Will create new log if blank or directory is specified. Will replay if file is specified and exists.")
args = parser.parse_args()
if args.device is None and args.udp is None and args.tcp is None and args.log is None:
    parser.print_help()
    exit(1)

# Signal handler to stop pinging on the Omniscan450
def signal_handler(sig, frame):
    print("\nStopping pinging on Omniscan450...")
    myOmniscan450.control_os_ping_params(enable=0)
    if myOmniscan450.iodev:
        try:
            myOmniscan450.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Check for log argument and make new Omniscan450
# If no .svlog is specified, create one using default directory
# If directory specified, .svlog be created in specified directory
# If a .svlog is specified, existing log will be opened
new_log = False
log_path = ""
replay_path = None
default_dir = Path("logs/omniscan").resolve()
if args.log is not None:
    if args.log is True:
        # Logging to default directory
        default_dir.mkdir(parents=True, exist_ok=True)
        myOmniscan450 = Omniscan450(logging=True, log_directory=default_dir)
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
                myOmniscan450 = Omniscan450(logging=False)
                replay_path = log_path
                print(f"Replaying from: {replay_path}")
            else:
                raise FileNotFoundError(f"Log file not found: {log_path}")

        elif log_path.is_dir() or log_path.suffix == "":
            # Path is directory, logging to that directory
            myOmniscan450 = Omniscan450(logging=True, log_directory=log_path)
            new_log = True
        
        else:
            raise ValueError(f"Invalid log argument: {args.log}")
else:
    myOmniscan450 = Omniscan450()

if args.log is None or new_log:
    if args.device is not None:
        myOmniscan450.connect_serial(args.device, args.baudrate)
    elif args.udp is not None:
        (host, port) = args.udp.split(':')
        myOmniscan450.connect_udp(host, int(port))
    elif args.tcp is not None:
        (host, port) = args.tcp.split(':')
        myOmniscan450.connect_tcp(host, int(port))    

    if myOmniscan450.initialize() is False:
        print("Failed to initialize Omniscan450!")
        exit(1)

    data1 = myOmniscan450.readDeviceInformation()
    print("Device type: %s" % data1.device_type)

print("------------------------------------")
print("Starting Omniscan450..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

# Running omniscan450Example.py from existing log file
if args.log is not None and not new_log:
    with open(log_path, 'rb') as f:
        while True:
            data = Omniscan450.read_packet(f)

            if data is None:
                break # EOF or bad packet

            print(f"ID: {data.message_id}\tName: {data.name}")
            if data.message_id == definitions.OMNISCAN450_OS_MONO_PROFILE:
            #     # print(data)

                # Printing the same results as if directly connected to the Omniscan
                scaled_result = Omniscan450.scale_power(data)
                print(f"Average power: {sum(scaled_result) / len(scaled_result)}")

# Connected to physical omniscan
else:
    if args.range is not None:
        parts = args.range.split(':')

        if len(parts) == 2:
            myOmniscan450.control_os_ping_params(
            start_mm=int(parts[0]),
            length_mm=int(parts[1]),
            enable=1
        )
        elif len(parts) == 1:
            myOmniscan450.control_os_ping_params(
                start_mm=0,
                length_mm=int(parts[0]),
                enable=1
            )
        else:
            print("Invalid range input, using default range")
            myOmniscan450.control_os_ping_params(enable=1)
    else: 
        # For default settings, just set enable pinging
        myOmniscan450.control_os_ping_params(enable=1)

    # For a custom ping rate
    custom_msec_per_ping = Omniscan450.calc_msec_per_ping(1000)    # 1000 Hz

    # To find pulse length percent
    custom_pulse_length = Omniscan450.calc_pulse_length_pc(0.2)    # 0.2%

    ## Set these attributes like this
    # myOmniscan450.control_os_ping_params(
    #     msec_per_ping=custom_msec_per_ping,
    #     pulse_len_percent=custom_pulse_length,
    #     num_results=200,
    #     enable=1
    # )

    # View power results
    if new_log:
        print("Logging...\nCTRL+C to stop logging")
    else:
        print("CTRL-C to end program...")
    try:
        while True:
            data = myOmniscan450.wait_message([definitions.OMNISCAN450_OS_MONO_PROFILE])
            if data:
                scaled_result = Omniscan450.scale_power(data)
                try:
                    print(f"Average power: {sum(scaled_result) / len(scaled_result)}")
                except ZeroDivisionError:
                    print("Length of scaled_result is 0")
            elif not data:
                print("Failed to get message")
    except KeyboardInterrupt:
        print("Stopping logging...")

    # Disable pinging and close socket
    myOmniscan450.control_os_ping_params(enable=0)
    if myOmniscan450.iodev:
            try:
                myOmniscan450.iodev.close()
            except Exception as e:
                print(f"Failed to close socket: {e}")
