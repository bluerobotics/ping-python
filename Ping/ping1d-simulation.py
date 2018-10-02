from Ping import PingMessage
import serial
import socket
import time
from collections import deque
import errno
import math

class Ping1DSimulation(object):




    def __init__(self):
        self.client = None

        self.parser = PingMessage.PingParser()

        ## Socket to serve on
        self.sockit = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sockit.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockit.setblocking(False)
        self.sockit.bind(('0.0.0.0', 6676))
    def distance(self):
        return 1000 * sin(time.time())

    def confidence(self):
        return 100 * cos(time.time())

    def profile(self):
        return range(0,200)

    def temperature(self):
        return 3500 * math.sin(time.time())

    def voltage(self):
        print(time.time())
        return int(3500 + 50 * math.sin(time.time()))

    def handleMessage(self, message):
        print("handling message: %s" % message)
        print("payload length: %s" % message.payload_length)

        if message.payload_length == 0:
            print("sending message: %s" % message.message_id)

            if message.message_id == PingMessage.PING1D_FIRMWARE_VERSION:
                msg = PingMessage.PingMessage(PingMessage.PING1D_FIRMWARE_VERSION)
                msg.firmware_version_minor = 6
                msg.firmware_version_major = 76
                msg.packMsgData()
                self.write(msg.msgData)
            if message.message_id == PingMessage.PING1D_VOLTAGE_5:
                msg = PingMessage.PingMessage(PingMessage.PING1D_VOLTAGE_5)
                msg.voltage_5 = self.voltage()
                msg.packMsgData()
                self.write(msg.msgData)

    def read(self):
            try:
                data, self.client = self.sockit.recvfrom(4096)

                # digest data coming in from client
                for byte in data:
                    if self.parser.parseByte(byte) == PingMessage.PingParser.NEW_MESSAGE:
                        print("got message from %s: %s" % (self.client, self.parser.rxMsg))
                        self.handleMessage(self.parser.rxMsg)

            except Exception as e:
                if e.errno == errno.EAGAIN:
                    pass # waiting for data
                else:
                    print("Error reading data", e)

    def write(self, data):
        print("client: %s" % str(self.client))

        if self.client is not None:
            print("sending message: %s" % self.parser.rxMsg)
            self.sockit.sendto(data, self.client)

sim = Ping1DSimulation()
while True:
    sim.read()
