#!/usr/bin/env python3

# PingProxy.py
# Connect multiple udp clients to a single serial device

from brping import PingParser
import serial
import socket
import time
from collections import deque
import errno


class PingClient(object):
    def __init__(self):
        ## Queued messages received from client
        self.rx_msgs = deque([])

        ## Parser to verify client comms
        self.parser = PingParser()

    ## Digest incoming client data
    # @return None
    def parse(self, data):
        for b in bytearray(data):
            if self.parser.parse_byte(b) == PingParser.NEW_MESSAGE:
                self.rx_msgs.append(self.parser.rx_msg)

    ## Dequeue a message received from client
    # @return None: if there are no comms in the queue
    # @return PingMessage: the next ping message in the queue
    def dequeue(self):
        if len(self.rx_msgs) == 0:
            return None
        return self.rx_msgs.popleft()


class PingProxy(object):
    def __init__(self, device=None, port=None):
        ## A serial object for ping device comms
        self.device = device

        ## UDP port number for server
        self.port = port

        if self.device is None:
            raise Exception("A device is required")

        if self.port is None:
            raise Exception("A port is required")

        ## Connected client dictionary
        self.clients = {}

        ## Socket to serve on
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind(('0.0.0.0', self.port))

    ## Run proxy tasks
    # @return None
    def run(self):
        try:
            data, address = self.socket.recvfrom(4096)

            # new client
            if address not in self.clients:
                self.clients[address] = PingClient()

            # digest data coming in from client
            self.clients[address].parse(data)

        except Exception as e:
            if e.errno == errno.EAGAIN:
                pass  # waiting for data
            else:
                print("Error reading data", e)

        # read ping device
        device_data = self.device.read(self.device.in_waiting)

        # send ping device data to all clients
        if device_data:  # don't write empty data
            for client in self.clients:
                # print("writing to client", client)
                self.socket.sendto(device_data, client)

        # send all client comms to ping device
        for client in self.clients:
            c = self.clients[client]
            msg = c.dequeue()
            while msg is not None:
                self.device.write(msg.msg_data)
                msg = c.dequeue()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Ping udp proxy server.")
    parser.add_argument('--device', action="store", required=True, type=str, help="Ping device serial port.")
    parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate.")
    parser.add_argument('--port', action="store", type=int, default=9090, help="Server udp port.")
    args = parser.parse_args()

    s = serial.Serial(args.device, args.baudrate, exclusive=True)
    proxy = PingProxy(s, args.port)

    while True:
        proxy.run()
        time.sleep(0.001)
