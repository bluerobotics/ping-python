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
import os
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
    print("Stopping pinging on Omniscan450...")
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
if args.log is not None:
    if args.log is True:
        # Logging to default directory
        myOmniscan450 = Omniscan450(logging=True)
        print(f"Logging to new file: {myOmniscan450.current_log}")
        new_log = True
    elif isinstance(args.log, str):
        log_path = Path(args.log).expanduser().resolve()

        if log_path.suffix == ".svlog":
            if log_path.exists() and log_path.is_file():
                # File exists, replaying
                new_log = False
                myOmniscan450 = Omniscan450(logging=False)
                replay_path = log_path
                print(f"Replaying from: {replay_path}")
            # TODO add default path logic
            else:
                raise FileNotFoundError(f"Log file not found: {log_path}")

        elif log_path.is_dir() or log_path.suffix == "":
            # Path is directory, logging to that directory
            myOmniscan450 = Omniscan450(logging=True, log_directory=log_path)
            print(f"Logging to new file: {myOmniscan450.current_log}")
            new_log = True
        
        else:
            raise ValueError(f"Invalid log argument: {args.log}")
    else:
        log_filename = None

if args.device is not None:
    myOmniscan450.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    myOmniscan450.connect_udp(host, int(port))
elif args.tcp is not None:
    (host, port) = args.tcp.split(':')
    myOmniscan450.connect_tcp(host, int(port))    

if args.log is None or new_log:
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

# Running Omniscan from existing log file
if args.log is not None and not new_log:
    with open(log_path, 'rb') as f:
        while True:
            start_bytes = f.read(2)
            if len(start_bytes) < 2:
                break   # EOF

            if start_bytes != b'BR':
                print("Invalid start bytes. Skipping...")
                continue

            header = f.read(6)
            if len(header) < 6:
                print("Incomplete header. Ending replay.")
                break

            payload_length = int.from_bytes(header[0:2], 'little')
            total_len = 2 + 2 + 2 + 2 + payload_length + 2  # BR + num payload bytes + packet id + reserved + payload + checksum 

            remaining = payload_length + 2
            rest = f.read(remaining)

            if len(rest) < remaining:
                print("Incomplete payload or checksum. Ending replay.")
            
            msg_bytes = start_bytes + header + rest
            data = PingMessage(msg_data=msg_bytes)

            # print(data)

            # Printing the same results as if directly connected to the Omniscan
            scaled_result = Omniscan450.scale_power(data)
            # for i in range(len(scaled_result)):
                # print(f"{i+1}: Raw: {data.pwr_results[i]}\tScaled: {scaled_result[i]}dB")
            print(f"Min power: {data.min_pwr_db} dB")
            print(f"Max power: {data.max_pwr_db} dB")
            print(f"Average power: {sum(scaled_result) / len(scaled_result)}")

        raw_bytes = f.read()
        data = PingMessage(msg_data=raw_bytes)

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
    while True:
        data = myOmniscan450.wait_message([definitions.OMNISCAN450_OS_MONO_PROFILE])
        if data:
            print("Message Recieved")
            # scaled_result = Omniscan450.scale_power(data)
            # for i in range(len(scaled_result)):
            #     print(f"{i+1}: Raw: {data.pwr_results[i]}\tScaled: {scaled_result[i]}dB")
            # print(f"Min power: {data.min_pwr_db} dB")
            # print(f"Max power: {data.max_pwr_db} dB")
            
        else:
            print("Failed to get report")

    # Disable pinging and close socket
    myOmniscan450.control_os_ping_params(enable=0)
    if myOmniscan450.iodev:
            try:
                myOmniscan450.iodev.close()
            except Exception as e:
                print(f"Failed to close socket: {e}")

    if new_log:
        os.makedirs("logs/omniscan", exist_ok=True)
        log_path = os.path.join("logs/omniscan", log_filename)
        with open(log_path, 'ab') as f:
            f.write(data.msg_data)