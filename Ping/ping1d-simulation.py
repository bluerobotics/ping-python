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

    def periodicFn(self, amplitude = 0, offset = 0, frequency = 1.0, shift = 0):
        return amplitude * math.sin(time.time() + shift) + offset

    def periodicFnInt(self, amplitude = 0, offset = 0, frequency = 1.0, shift = 0):
        return int(self.periodicFn(amplitude, offset, frequency, shift))

    def distance(self):
        return self.periodicFnInt(500, 15000)

    def confidence(self):
        return self.periodicFnInt(500, 15000)

    def profile(self):
        return range(0,200)

    def pcb_temperature(self):
        return self.periodicFnInt(250, 3870, 3)

    def processor_temperature(self):
        return self.periodicFnInt(340, 3400)

    def voltage_5(self):
        return self.periodicFnInt(100, 3500)

    def handleMessage(self, message):
        if message.payload_length == 0:
            msg = PingMessage.PingMessage(message.message_id)
            for attr in PingMessage.payloadDict[message.message_id]["field_names"]:
                try:
                    setattr(msg, attr, getattr(self, attr)())
                except Exception as e:
                    print(e)
                    setattr(msg, attr, self.periodicFnInt(120, 128))
            msg.packMsgData()
            print("sent message: %s" % msg)
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
