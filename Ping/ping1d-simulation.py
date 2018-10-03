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
        self._profile_data_length = 200
        self.parser = PingMessage.PingParser()
        self._ping_number = 0
        self._ping_interval = 100
        self._mode_auto = True
        self._pulse_duration = 100
        self._mode_continuous = True
        ## Socket to serve on
        self.sockit = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sockit.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockit.setblocking(False)
        self.sockit.bind(('0.0.0.0', 6676))

    def periodicFn(self, amplitude = 0, offset = 0, frequency = 1.0, shift = 0):
        return amplitude * math.sin(frequency * time.time() + shift) + offset

    def periodicFnInt(self, amplitude = 0, offset = 0, frequency = 1.0, shift = 0):
        return int(self.periodicFn(amplitude, offset, frequency, shift))

    def distance(self):
        return self.periodicFnInt(self.scan_length() / 2, self.scan_start() + self.scan_length() / 2, 5)

    def confidence(self):
        return self.periodicFnInt(40, 50)

    def scan_start(self):
        if self._mode_auto:
            return 0
        return self._scan_start

    def scan_length(self):
        if self._mode_auto:
            self._scan_length = self.periodicFnInt(20000, 30000, 0.5)
        return self._scan_length

    def profile_data(self):
        return bytearray(range(0,200))

    def pcb_temperature(self):
        return self.periodicFnInt(250, 3870, 3)

    def processor_temperature(self):
        return self.periodicFnInt(340, 3400)

    def voltage_5(self):
        return self.periodicFnInt(100, 3500)

    def profile_data_length(self):
        return self._profile_data_length
    
    def gain_index(self):
        return 2
    
    def ping_number(self):
        return self._ping_number

    def pulse_duration(self):
        return self._pulse_duration

    def sendMessage(self, message_id):
            msg = PingMessage.PingMessage(message_id)
            for attr in PingMessage.payloadDict[message_id]["field_names"]:
                try:
                    setattr(msg, attr, getattr(self, attr)())
                except Exception as e:
                    try:
                        setattr(msg, attr, getattr(self, "_" + attr))
                    except AttributeError as e:
                        setattr(msg, attr, self.periodicFnInt(20, 120))

            msg.packMsgData()
            #print("sent message: %s" % msg)
            self.write(msg.msgData)

    def handleMessage(self, message):
        if message.message_id == PingMessage.PING1D_SET_MODE_AUTO:
            print(message)
        if message.payload_length == 0:
            self.sendMessage(message.message_id)
        #TODO mechanism to filter by "set"
        else:
            self.setParameters(message)

    def setParameters(self, message):
        for attr in PingMessage.payloadDict[message.message_id]["field_names"]:
            setattr(self, "_" + attr, getattr(message, attr))


    def read(self):
            try:
                data, self.client = self.sockit.recvfrom(4096)

                # digest data coming in from client
                for byte in data:
                    if self.parser.parseByte(byte) == PingMessage.PingParser.NEW_MESSAGE:
                        #print("got message from %s: %s" % (self.client, self.parser.rxMsg))
                        self.handleMessage(self.parser.rxMsg)

            except Exception as e:
                if e.errno == errno.EAGAIN:
                    pass # waiting for data
                else:
                    print("Error reading data", e)

    def write(self, data):
        if self.client is not None:
            self.sockit.sendto(data, self.client)

sim = Ping1DSimulation()
lastUpdate = 0
while True:
    sim.read()
    if time.time() > lastUpdate + sim._ping_interval / 1000.0:
        lastUpdate = time.time()
        sim._ping_number += 1
        if sim._mode_continuous:
            sim.sendMessage(PingMessage.PING1D_PROFILE)

