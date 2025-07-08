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

# Check for log argument and make new S500
# If no .svlog is specified, create one using default directory
# If directory specified, .svlog be created in specified directory
# If a .svlog is specified, existing log will be opened
new_log = False
log_path = ""
replay_path = None
default_dir = Path("logs/s500").resolve()
if args.log is not None:
    if args.log is True:
        # Logging to default directory
        default_dir.mkdir(parents=True, exist_ok=True)
        myS500 = S500(logging=True, log_directory=default_dir)
        # print(f"Logging to new file in: {default_dir}")
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
                myS500 = S500(logging=False)
                replay_path = log_path
                print(f"Replaying from: {replay_path}")
            else:
                raise FileNotFoundError(f"Log file not found: {log_path}")

        elif log_path.is_dir() or log_path.suffix == "":
            # Path is directory, logging to that directory
            myS500 = S500(logging=True, log_directory=log_path)
            # print(f"Logging to new file: {S500.current_log}")
            new_log = True
        
        else:
            raise ValueError(f"Invalid log argument: {args.log}")
else:
    myS500 = S500()

if args.log is None or new_log:
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

print("------------------------------------")
print("Starting S500..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

# Running s500Example.py from existing log file
if args.log is not None and not new_log:
    with open(log_path, 'rb') as f:
        while True:
            data = S500.read_packet(f)

            if data is None:
                break   # EOF or bad packet

            # Uncomment to print out all packets contained in log file
            # print(f"ID: {data.message_id}\tName: {data.name}")

            if data.message_id == definitions.S500_PROFILE6_T:
                scaled_result = S500.scale_power(data)
                try:
                    print(f"Average power: {sum(scaled_result) / len(scaled_result)}")
                except ZeroDivisionError:
                    print("Length of scaled_result is 0")

# Connected to physical S500
else:
    # Tell S500 to send profile6 data
    if args.range is not None:
        parts = args.range.split(':')
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

    if new_log:
        print("Logging...\nCTRL+C to stop logging")
    else:
        print("CTRL-C to end program...")
    try:
        while True:
            # Read and print profile6 data
            data = myS500.wait_message([definitions.S500_PROFILE6_T,
                                        definitions.S500_DISTANCE2])
            if data:
                scaled_result = S500.scale_power(data)
                try:
                    print(f"Average power: {sum(scaled_result) / len(scaled_result)}")
                except ZeroDivisionError:
                    print("Length of scaled_result is 0")
            elif not data:
                print("Failed to get message")
    except KeyboardInterrupt:
        print("Stopping logging...")

    # Stop pinging
    myS500.control_set_ping_params(report_id=0)
    if myS500.iodev:
        try:
            myS500.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")