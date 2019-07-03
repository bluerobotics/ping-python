#!/usr/bin/env python

# This script simulates a Blue Robotics Ping Echosounder device
# A client may connect to the device simulation on local UDP port 6676
 
from brping import PingMessage, PingParser, PING1D_PROFILE, payload_dict
import socket
import time
import errno
import math

class Ping1DSimulation(object):
    def __init__(self):
        self.client = None # (ip address, port) of connected client (if any)
        self.parser = PingParser() # used to parse incoming client comunications


        # Socket to serve on
        self.sockit = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockit.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockit.setblocking(False)
        self.sockit.bind(('0.0.0.0', 6676))

        self._profile_data_length = 200 # number of data points in profile messages (constant for now)
        self._pulse_duration = 100 # length of acoustic pulse (constant for now)
        self._ping_number = 0 # count the total measurements taken since boot
        self._ping_interval = 100 # milliseconds between measurements
        self._mode_auto = True # automatic gain and range selection
        self._mode_continuous = True # automatic continuous output of profile messages

    # read incoming client data
    def read(self):
        try:
            data, self.client = self.sockit.recvfrom(4096)

            # digest data coming in from client
            for byte in data:
                if self.parser.parse_byte(byte) == PingParser.NEW_MESSAGE:
                    # we decoded a message from the client
                    self.handleMessage(self.parser.rx_msg)

        except Exception as e:
            if e.errno == errno.EAGAIN:
                pass # waiting for data
            else:
                print("Error reading data", e)

    # write data to client
    def write(self, data):
        if self.client is not None:
            print("sending data to client")
            self.sockit.sendto(data, self.client)

    # Send a message to the client, the message fields are populated by the
    # attributes of this object (either variable or method) with names matching
    # the message field names
    def sendMessage(self, message_id):
        msg = PingMessage(message_id)

        # pull attributes of this class into the message fields (they are named the same)
        for attr in payload_dict[message_id]["field_names"]:
            try:
                # see if we have a function for this attribute (dynamic data)
                # if so, call it and put the result in the message field
                setattr(msg, attr, getattr(self, attr)())
            except AttributeError as e:
                try:
                    # if we don't have a function for this attribute, check for a _<field_name> member
                    # these are static values (or no function implemented yet)
                    setattr(msg, attr, getattr(self, "_" + attr))
                except AttributeError as e:
                    # anything else we haven't implemented yet, just send a sine wave
                    setattr(msg, attr, self.periodicFnInt(20, 120))

        # send the message to the client
        msg.pack_msg_data()
        self.write(msg.msg_data)

    # handle an incoming client message
    def handleMessage(self, message):
        if message.payload_length == 0:
            # the client is requesting a message from us
            self.sendMessage(message.message_id)
        else:
            # the client is controlling some parameter of the device
            self.setParameters(message)

    # Extract message fields into attribute values
    # This should only be performed with the 'set' category of messages
    # TODO: mechanism to filter by "set"
    def setParameters(self, message):
        for attr in payload_dict[message.message_id]["field_names"]:
            setattr(self, "_" + attr, getattr(message, attr))

    ###########
    # Helpers for generating periodic data
    ###########
    def periodicFn(self, amplitude = 0, offset = 0, frequency = 1.0, shift = 0):
        return amplitude * math.sin(frequency * time.time() + shift) + offset

    def periodicFnInt(self, amplitude = 0, offset = 0, frequency = 1.0, shift = 0):
        return int(self.periodicFn(amplitude, offset, frequency, shift))

    ###########
    # Device properties/state
    ###########
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
            self._scan_length = self.periodicFnInt(2000, 3000, 0.2)
        return self._scan_length

    def profile_data(self):
        stops = 20
        len = int(200/stops)
        data = []
        for x in range(stops):
            data = data + [int(x*255/stops)]*len
        return bytearray(data) # stepwise change in signal strength
        #return bytearray(range(0,200)) # linear change in signal strength

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

# The simulation to use
sim = Ping1DSimulation()

# Last measurement time
lastUpdate = 0

while True:
    # read any incoming client communications
    sim.read()

    # Update background ping count and continuous output
    if time.time() > lastUpdate + sim._ping_interval / 1000.0:
        lastUpdate = time.time()
        sim._ping_number += 1
        if sim._mode_continuous:
            sim.sendMessage(PING1D_PROFILE)

    # don't max cpu
    time.sleep(0.01)
