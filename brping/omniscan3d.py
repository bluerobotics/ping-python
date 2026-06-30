#!/usr/bin/env python3

# omniscan3d.py
# A device API for the Cerulean Sonar Omniscan3D scanning sonar

# This is a source template used to generate omniscan3d.py.
# Edit this file, not the generated omniscan3d.py.

from brping import definitions
from brping import PingDevice
from brping import pingmessage
import math
import time
import struct
import socket
from datetime import datetime, timezone
from pathlib import Path

# Imports for svlog header
import json
import os
import sys
import platform

MAX_LOG_SIZE_MB = 500

class Omniscan3D(PingDevice):
    def __init__(self, logging = False, log_directory = None):
        super().__init__(payload_dict=definitions.payload_dict_omniscan3d)

        self.logging = logging
        self.log_directory = log_directory
        self.bytes_written = None
        self.current_log = None

    def initialize(self):
        if (self.readDeviceInformation() is None):
            return False
        if self.logging:
            self.new_log(self.log_directory)
        return True

    ##
    # @brief Get a attitude_report message from the device\n
    # Message description:\n
    # 
    #
    # @return None if there is no reply from the device, otherwise a dictionary with the following keys:\n
    # up_vec_x: World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)\n
    # up_vec_y: World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)\n
    # up_vec_z: World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)\n
    # reserved_1: reserved for future magnetic field vector\n
    # reserved_2: reserved for future magnetic field vector\n
    # reserved_3: reserved for future magnetic field vector\n
    # utc_msec: Units: ms; utc msec (1970 epoch). Will be 0 if not available.\n
    # pwr_up_msec: Units: ms; msec since power up\n
    # channel_number: assigned sequentially from 0. typically 0 for a single channel system and 0 or 1 for port/stb setup.\n
    def get_attitude_report(self):
        if self.request(definitions.OMNISCAN3D_ATTITUDE_REPORT) is None:
            return None
        data = ({
            "up_vec_x": self._up_vec_x,  # World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)
            "up_vec_y": self._up_vec_y,  # World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)
            "up_vec_z": self._up_vec_z,  # World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)
            "reserved_1": self._reserved_1,  # reserved for future magnetic field vector
            "reserved_2": self._reserved_2,  # reserved for future magnetic field vector
            "reserved_3": self._reserved_3,  # reserved for future magnetic field vector
            "utc_msec": self._utc_msec,  # Units: ms; utc msec (1970 epoch). Will be 0 if not available.
            "pwr_up_msec": self._pwr_up_msec,  # Units: ms; msec since power up
            "channel_number": self._channel_number,  # assigned sequentially from 0. typically 0 for a single channel system and 0 or 1 for port/stb setup.
        })
        return data

    ##
    # @brief Get a end_ping_info message from the device\n
    # Message description:\n
    # <b>Payload Definition</b>
    #
    # @return None if there is no reply from the device, otherwise a dictionary with the following keys:\n
    # reserved1: deprecated, may be repurposed in future\n
    # range_start_m: Units: m; range where sampling begins\n
    # range_end_m: Units: m; range where sampling ends\n
    # up_vec_x: World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)\n
    # up_vec_y: World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)\n
    # up_vec_z: World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)\n
    # ping_number: assigned sequentially from power on\n
    # water_degC: -1000 if no sensor present\n
    # water_bar: -1000 if no sensor present\n
    # heave_m: 0, not yet implemented\n
    # mag_vec_x: reserved for future implementation\n
    # mag_vec_y: reserved for future implementation\n
    # mag_vec_z: reserved for future implementation\n
    # ping_hz_realized: actual ping hz (may differ from requested)\n
    # gain_index: gain index used for this ping\n
    # pulse_usec: length of the pulse used in this ping in usec\n
    # n_range_bins: number of range bins processed for this ping\n
    # samples_per_range_bin: number of adc samples in each range bin\n
    # device_number: must be < number of devices, so 0 for single device\n
    # unused: 0\n
    # pwr_up_msec: msec since pwr up at start of ping\n
    # utc_msec: utc msec at start of ping\n
    def get_end_ping_info(self):
        if self.request(definitions.OMNISCAN3D_END_PING_INFO) is None:
            return None
        data = ({
            "reserved1": self._reserved1,  # deprecated, may be repurposed in future
            "range_start_m": self._range_start_m,  # Units: m; range where sampling begins
            "range_end_m": self._range_end_m,  # Units: m; range where sampling ends
            "up_vec_x": self._up_vec_x,  # World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)
            "up_vec_y": self._up_vec_y,  # World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)
            "up_vec_z": self._up_vec_z,  # World up vector (x, y, z) in the device coordinate system (x forward, y port, z up)
            "ping_number": self._ping_number,  # assigned sequentially from power on
            "water_degC": self._water_degC,  # -1000 if no sensor present
            "water_bar": self._water_bar,  # -1000 if no sensor present
            "heave_m": self._heave_m,  # 0, not yet implemented
            "mag_vec_x": self._mag_vec_x,  # reserved for future implementation
            "mag_vec_y": self._mag_vec_y,  # reserved for future implementation
            "mag_vec_z": self._mag_vec_z,  # reserved for future implementation
            "ping_hz_realized": self._ping_hz_realized,  # actual ping hz (may differ from requested)
            "gain_index": self._gain_index,  # gain index used for this ping
            "pulse_usec": self._pulse_usec,  # length of the pulse used in this ping in usec
            "n_range_bins": self._n_range_bins,  # number of range bins processed for this ping
            "samples_per_range_bin": self._samples_per_range_bin,  # number of adc samples in each range bin
            "device_number": self._device_number,  # must be < number of devices, so 0 for single device
            "unused": self._unused,  # 0
            "pwr_up_msec": self._pwr_up_msec,  # msec since pwr up at start of ping
            "utc_msec": self._utc_msec,  # utc msec at start of ping
        })
        return data

    ##
    # @brief Get a os3d_point_set message from the device\n
    # Message description:\n
    # 
    #
    # @return None if there is no reply from the device, otherwise a dictionary with the following keys:\n
    # ping_number: assigned sequentially from power on\n
    # sos_mps: speed of sound (meters per second) used in angle calculations\n
    # num_points: number of points reported in the points field\n
    # unused_1: 0\n
    # unused_2: 0\n
    # utc_msec: Units: ms; time at start of ping, UTC milliseconds (1970 epoch). Will be 0 if not available.\n
    # pwr_up_msec: Units: ms; time at start of ping from power on\n
    # version: 1. There was a previous version (0), see note below\n
    # device_number: must be < number of devices (so it will be 0 for a single device)\n
    # unused_3: 0\n
    # reserved_1: 0\n
    # pwr_threshold_high: Points with pwr higher than this are quite strong. This was the level used in all version 0 point sets. Seemed to be overly conservative.\n
    # pwr_threshold_med: This is a reasonable cutoff level for most applications.\n
    # pwr_threshold_low: This is a more liberal power level. If point_data is filtered with this threshold\n
    # reserved2_0: reserved for future\n
    # reserved2_1: reserved for future\n
    # reserved2_2: reserved for future\n
    # reserved2_3: reserved for future\n
    # reserved2_4: reserved for future\n
    # reserved2_5: reserved for future\n
    # reserved2_6: reserved for future\n
    # reserved2_7: reserved for future\n
    # reserved2_8: reserved for future\n
    # atof_point_data: see below for atof_t definition\n
    def get_os3d_point_set(self):
        if self.request(definitions.OMNISCAN3D_OS3D_POINT_SET) is None:
            return None
        data = ({
            "ping_number": self._ping_number,  # assigned sequentially from power on
            "sos_mps": self._sos_mps,  # speed of sound (meters per second) used in angle calculations
            "num_points": self._num_points,  # number of points reported in the points field
            "unused_1": self._unused_1,  # 0
            "unused_2": self._unused_2,  # 0
            "utc_msec": self._utc_msec,  # Units: ms; time at start of ping, UTC milliseconds (1970 epoch). Will be 0 if not available.
            "pwr_up_msec": self._pwr_up_msec,  # Units: ms; time at start of ping from power on
            "version": self._version,  # 1. There was a previous version (0), see note below
            "device_number": self._device_number,  # must be < number of devices (so it will be 0 for a single device)
            "unused_3": self._unused_3,  # 0
            "reserved_1": self._reserved_1,  # 0
            "pwr_threshold_high": self._pwr_threshold_high,  # Points with pwr higher than this are quite strong. This was the level used in all version 0 point sets. Seemed to be overly conservative.
            "pwr_threshold_med": self._pwr_threshold_med,  # This is a reasonable cutoff level for most applications.
            "pwr_threshold_low": self._pwr_threshold_low,  # This is a more liberal power level. If point_data is filtered with this threshold
            "reserved2_0": self._reserved2_0,  # reserved for future
            "reserved2_1": self._reserved2_1,  # reserved for future
            "reserved2_2": self._reserved2_2,  # reserved for future
            "reserved2_3": self._reserved2_3,  # reserved for future
            "reserved2_4": self._reserved2_4,  # reserved for future
            "reserved2_5": self._reserved2_5,  # reserved for future
            "reserved2_6": self._reserved2_6,  # reserved for future
            "reserved2_7": self._reserved2_7,  # reserved for future
            "reserved2_8": self._reserved2_8,  # reserved for future
            "atof_point_data": self._atof_point_data,  # see below for atof_t definition
        })
        return data


    def control_os3d_set_ping_params(self, start_m=0, end_m=0, sos_mps=1500, gain_index=-1, msec_per_ping=100, reserved1=0, diagnostic_injected_signal=0, ping_enable=False, enable_channel_data=False, reserved_for_raw_data=False, reserved2=False, enable_atof_data=False, target_ping_hz=450000, n_range_steps=1000, reserved3=0, pulse_len_steps=1.5):
        m = pingmessage.PingMessage(definitions.OMNISCAN3D_OS3D_SET_PING_PARAMS,payload_dict=definitions.payload_dict_omniscan3d)
        m.start_m = start_m
        m.end_m = end_m
        m.sos_mps = sos_mps
        m.gain_index = gain_index
        m.msec_per_ping = msec_per_ping
        m.reserved1 = reserved1
        m.diagnostic_injected_signal = diagnostic_injected_signal
        m.ping_enable = ping_enable
        m.enable_channel_data = enable_channel_data
        m.reserved_for_raw_data = reserved_for_raw_data
        m.reserved2 = reserved2
        m.enable_atof_data = enable_atof_data
        m.target_ping_hz = target_ping_hz
        m.n_range_steps = n_range_steps
        m.reserved3 = reserved3
        m.pulse_len_steps = pulse_len_steps
        m.pack_msg_data()
        self.write(m.msg_data)


    def readDeviceInformation(self):
        return self.request(definitions.COMMON_DEVICE_INFORMATION)

    # Calculate the milliseconds per ping from a ping rate
    @staticmethod
    def calc_msec_per_ping(ping_rate):
        return math.floor(1000.0 / ping_rate)

    def get_utc_time(self):
        clock_offset = 0
        round_trip_delay = 5000

        local_now = datetime.now(timezone.utc)
        corrected_time = local_now.timestamp() * 1000 + clock_offset / 2
        accuracy = round_trip_delay / 2

        utc_msec_u64 = int(corrected_time) & 0xFFFFFFFFFFFFFFFF
        accuracy_msec = int(accuracy) & 0xFFFFFFFF

        return utc_msec_u64, accuracy_msec

    # Reads a single packet from a file
    @staticmethod
    def read_packet(file):
        sync = file.read(2)
        if sync != b'BR':
            return None

        payload_len_bytes = file.read(2)
        if len(payload_len_bytes) < 2:
            return None
        payload_len = int.from_bytes(payload_len_bytes, 'little')

        msg_id = file.read(2)
        if len(msg_id) < 2:
            return None

        remaining = 2 + payload_len + 2
        rest = file.read(remaining)
        if len(rest) < remaining:
            return None

        msg_bytes = sync + payload_len_bytes + msg_id + rest
        return pingmessage.PingMessage(msg_data=msg_bytes,payload_dict=definitions.payload_dict_omniscan3d)

    # Builds the packet containing metadata for the beginning of .svlog
    def build_metadata_packet(self):
        protocol = "tcp" # default fallback
        if self.iodev:
            if self.iodev.type == socket.SOCK_STREAM:
                protocol = "tcp"
            elif self.iodev.type == socket.SOCK_DGRAM:
                protocol = "udp"

        if self.server_address:
            url = f"{protocol}://{self.server_address[0]}:{self.server_address[1]}"
        else:
            url = f"{protocol}://unknown"

        content = {
            "session_id": 1,
            "session_uptime": 0.0,
            "session_devices": [
                {
                    "url": url,
                    "product_id": "os3d45016"
                }
            ],
            "session_platform": None,
            "session_clients": [],
            "session_plan_name": None,

            "is_recording": True,
            "sonarlink_version": "",
            "os_hostname": platform.node(),
            "os_uptime": None,
            "os_version": platform.version(),
            "os_platform": platform.system().lower(),
            "os_release": platform.release(),

            "process_path": sys.executable,
            "process_version": f"v{platform.python_version()}",
            "process_uptime": time.process_time(),
            "process_arch": platform.machine(),

            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timestamp_timezone_offset": datetime.now().astimezone().utcoffset().total_seconds() // 60
        }

        json_bytes = json.dumps(content, indent=2).encode("utf-8")

        m = pingmessage.PingMessage(definitions.OMNISCAN3D_JSON_WRAPPER,payload_dict=definitions.payload_dict_omniscan3d)
        m.payload = json_bytes
        m.payload_length = len(json_bytes)

        msg_data = bytearray()
        msg_data += b"BR"
        msg_data += m.payload_length.to_bytes(2, "little")
        msg_data += m.message_id.to_bytes(2, "little")
        msg_data += m.dst_device_id.to_bytes(1, "little")
        msg_data += m.src_device_id.to_bytes(1, "little")
        msg_data += m.payload

        checksum = sum(msg_data) & 0xFFFF
        msg_data += bytearray(struct.pack(pingmessage.PingMessage.endianess + pingmessage.PingMessage.checksum_format, checksum))

        m.msg_data = msg_data
        m.checksum = checksum

        return m

    # Enable logging
    def start_logging(self, new_log = False, log_directory = None):
        if self.logging:
            return

        self.logging = True

        if self.current_log is None or new_log:
            self.new_log(log_directory)

    def stop_logging(self):
        self.logging = False

    # Creates a new log file
    def new_log(self, log_directory=None):
        dt = datetime.now()
        save_name = dt.strftime("%Y-%m-%d-%H-%M")

        if log_directory is None:
            project_root = Path.cwd().parent
            self.log_directory = project_root / "logs/omniscan3d"
        else:
            self.log_directory = Path(log_directory)

        self.log_directory.mkdir(parents=True, exist_ok=True)

        log_path = self.log_directory / f"{save_name}.svlog"

        if log_path.exists():
            log_path.unlink() # delete existing file (program was restarted quickly)

        self.current_log = log_path
        self.logging = True
        self.bytes_written = 0

        print(f"Logging to {self.current_log}")

        self.write_data(self.build_metadata_packet())

    # Write data to .svlog file
    def write_data(self, msg):
        if not self.logging or not self.current_log:
            return

        try:
            if self.bytes_written > MAX_LOG_SIZE_MB * 1000000:
                self.new_log(log_directory=self.log_directory)

            with open(self.current_log, 'ab') as f:
                f.write(msg.msg_data)
                self.bytes_written += len(msg.msg_data)

        except (OSError, IOError) as e:
            print(f"[LOGGING ERROR] Failed to write to log file {self.current_log}: {e}")
            self.stop_logging()

        except Exception as e:
            print(f"[LOGGING ERROR] Unexpected error: {e}")
            self.stop_logging()

    # Override wait_message to also handle point set requests from Omniscan3D and for creating atof_t data
    def wait_message(self, message_ids, timeout=0.5):
        tstart = time.time()
        while time.time() < tstart + timeout:
            msg = self.read()
            if msg is not None:
                if msg.message_id == definitions.OMNISCAN3D_OS3D_POINT_SET:
                    atof_byte_array = bytearray(msg.atof_point_data)
                    formatted_atof_array = struct.unpack('<' + 'I' * (4*int(msg.num_points)), atof_byte_array)
                    msg.atof_point_data = formatted_atof_array

                if msg.message_id in message_ids:
                    if self.logging:
                        self.write_data(msg)
                    return msg
            time.sleep(0.005)
        return None

    ##
    # @brief Do the connection via an TCP link
    #
    # @param host: TCP server address (IPV4) or name
    # @param port: port used to connect with server
    #
    def connect_tcp(self, host: str = None, port: int = 12345, timeout: float = 5.0):
        if host is None:
            host = '0.0.0.0'

        self.server_address = (host, port)
        try:
            print("Opening %s:%d" % self.server_address)
            self.iodev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.iodev.settimeout(timeout)
            self.iodev.connect(self.server_address)
            self.iodev.setblocking(0)

        except socket.timeout:
            print("Unable to connect to device")
            raise Exception("Connection timed out after {0} seconds".format(timeout))
        except Exception as exception:
            raise Exception("Failed to open the given TCP port: {0}".format(exception))

    ##
    # @brief Read available data from the io device
    def read_io(self):
        if self.iodev == None:
            raise Exception("IO device is null, please configure a connection before using the class.")
        elif type(self.iodev).__name__ == 'Serial':
            bytes = self.iodev.read(self.iodev.in_waiting)
            self._input_buffer.extendleft(bytes)
        else: # Socket
            buffer_size = 4096
            while True:
                try: # Check if we are reading before closing a connection
                    bytes = self.iodev.recv(buffer_size)

                    if not bytes:
                        # if recv() returns empty, connection is closed (TCP)
                        if self.iodev.type == socket.SOCK_STREAM:
                            raise ConnectionError("TCP connection closed by peer.")

                    self._input_buffer.extendleft(bytes)

                    if len(bytes) < buffer_size:
                        break

                except BlockingIOError as exception:
                    pass # Ignore exceptions related to read before connection, a result of UDP nature

                except ConnectionResetError as e:
                    raise ConnectionError("Socket connection was reset: %s" % str(e))

# Class to represent the OmniScan3D atof_t struct
class atof_t:
    def __init__(self, angle=0.0, tof=0.0, pwr=0.0, pt_type=0, reserved=(0, 0, 0)):
        self.angle = angle
        self.tof = tof
        self.pwr = pwr
        self.pt_type = pt_type
        self.reserved = reserved

    def __repr__(self):
        return (
            f"angle: {self.angle}, "
            f"tof: {self.tof}, "
            f"pwr: {self.pwr}, "
            f"pt_type: {self.pt_type}"
        )

# Creates atof_point_t[] from the dynamic byte payload
@staticmethod
def create_atof_list(msg):
    raw_bytes = msg.atof_point_data

    point_size = struct.calcsize('<fffB3B')
    atof_list = []

    for i in range(msg.num_points):
        offset = i * point_size
        chunk = raw_bytes[offset:offset + point_size]

        angle, tof, pwr, pt_type, r0, r1, r2 = struct.unpack('<fffB3B', chunk)

        point = Omniscan3D.atof_t(
            angle=angle,
            tof=tof,
            pwr=pwr,
            pt_type=pt_type,
            reserved=(r0, r1, r2),
        )
        atof_list.append(point)

    return tuple(atof_list)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ping python library example.")
    parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
    parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
    parser.add_argument('--tcp', action="store", required=False, type=str, help="Omniscan3d IP:Port. E.g: 192.168.2.21:62312")
    args = parser.parse_args()
    if args.device is None and args.tcp is None:
        parser.print_help()
        exit(1)

    p = Omniscan3D()
    if args.device is not None:
        p.connect_serial(args.device, args.baudrate)
    elif args.tcp is not None:
        (host, port) = args.tcp.split(':')
        p.connect_tcp(host, int(port))

    print("Initialized: %s" % p.initialize())
    if p.iodev:
        try:
            p.iodev.close()
        except Exception as e:
            print(f"Failed to close socket: {e}")