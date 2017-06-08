#!/usr/bin/python -u
#Ping.py

import sys
import struct
import serial
import getopt
import socket
import Message

class Ping1D:
    instructions = "Usage: python simplePingExample.py -d <device_name>"

    #Parameters
    ###########
    #General
    device_id                             = 255
    device_type                           = 0
    device_model                          = 0
    is_new_data                           = 0
    fw_version_major                      = 0
    fw_version_minor                      = 0
    voltage                               = 0

    #Sonar
    c_water                               = 0

    #EchoSounder
    distance                              = 0
    confidence                            = 0
    pulse_usec                            = 0
    ping_number                           = 0
    start_mm                              = 0
    length_mm                             = 0
    gain_index                            = 0
    num_points                            = 0
    points                                = [None] * 200
    auto_manual                           = 0
    msec_per_ping                         = 0
    gain_index                            = 0

    #Start Signal
    validation_1 = b'B'
    validation_2 = b'R'
    test_1 = ''
    test_2 = ''

    def __init__(self, deviceName):
        #Open the serial port
        if (deviceName == ''):
            print(self.instructions)
            exit(1)
        try:
            self.ser = serial.Serial(deviceName, 115200)
        except:
            print("Failed to open the given serial port")
            exit(1)

    def initialize(self):
        self.update(Message.gen_device_id)
        self.update(Message.gen_version)
        self.update(Message.gen_voltage)

    #Read and Update
    def update(self, message):
        self.request(message.id)
        sonarData = self.readSonar()
        if (sonarData != None):
           self.handleMessage(sonarData)

    #Update values from new sonar report
    def handleMessage(self, sonarData):
        messageID = sonarData[0]
        payloadPacked = sonarData[1]

        new_message = self.messages[messageID]
        payload = struct.unpack(new_message.format, payloadPacked)

        for i,attr in enumerate(new_message.payload_fields):
            #Have to have a separate handling for lists / arrays
            if (attr == "points"):
                self.points = (payload[((len(payload) - self.num_points)):(len(payloadPacked))])
            else:
                setattr(self, attr, payload[i])


    def readSonar(self):
        timeout = 10000
        readCount = 0

        headerRaw = ""
        payloadRaw = ""
        checksumRaw = ""

        start_signal_found = False

        try:
            #Burn through data until start signal
            while(not start_signal_found):
                #Put new byte in second index
                self.test_2 = self.ser.read()

                #Check if start signal
                if((self.test_1 == self.validation_1) and (self.test_2 == self.validation_2)):
                    start_signal_found = True
                else:
                    #Move second byte to first byte
                    self.test_1 = self.test_2

                    #Check if timeout has been reached
                    readCount += 1
                    if (readCount > timeout):
                        print("Serial Read Timeout. Check device and connections")
                        return None

            #Add start signal to buffer, since we have a valid message
            headerRaw += struct.pack('<c', self.validation_1)
            headerRaw += struct.pack('<c', self.validation_2)

            #Get the header
            for i in range(2, 8):
                byte = self.ser.read()
                headerRaw += struct.pack("<c", byte)

            #Decode Header
            header = struct.unpack(self.msg_header, headerRaw)

            #Look at header metadata
            payloadLength = header[2]
            messageID     = header[3]
            sourceID      = header[4]
            destinationID = header[5]

            messageForHost = False

            if(destinationID != 0):
                messageForHost = False
            else:
                messageForHost = True

            #Get the message body
            for i in range(0, payloadLength):
                byte = self.ser.read()
                payloadRaw += struct.pack("<c", byte)

            #Get the Checksum
            for i in range(0, 2):
                byte = self.ser.read()
                checksumRaw += struct.pack("<c", byte)

            #Ignore message if it was not directed at the host
            if (not messageForHost):
                return None

            #Decode the checksum
            checksum = struct.unpack(self.msg_checksum, checksumRaw)[0]
            checksumMatch = self.evaluateChecksum(headerRaw, payloadRaw, checksum)

            #Return None if there is a checksum error
            if (not checksumMatch):
                print("Checksum mismatch!")
                return None

            return (messageID, payloadRaw)

        except Exception as e:
            print "Error: "+str(e)
            pass

    #Control Methods
    ###################

    #Request the given message ID
    def request(self, m_id):
        payloadData = [m_id]
        self.sendMessage(Message.gen_cmd_request, payloadData, self.device_id)

    #Manually set the scanning range
    def setRange(self, auto, start, range):
        #TODO implement
        return false

    #Set special debug options
    def setDebugOptions(self, raw, auto, gain, c):
        #TODO implement
        return false

    #Used for sending of all messages
    def sendMessage(self, m_message, m_payload, m_destination):
        #Pack payload first, because metadata is required for the header
        finalPayload = self.packPayload(m_message.format, m_payload)

        #Needed to build header
        payloadLength = struct.calcsize(m_message.format)

        #Create and pack header
        header = self.buildHeader(payloadLength, m_message.id, m_destination)
        finalHeader = self.packHeader(header)

        #Create Checksum
        checksum = self.buildChecksum(finalHeader, finalPayload)
        finalChecksum = self.packChecksum(checksum)

        #Send it!
        self.ser.write(finalHeader)
        self.ser.write(finalPayload)
        self.ser.write(finalChecksum)

    #Accessor Methods
    ################

    #Returns a string of the version number
    def getVersion(self):
        self.update(Message.gen_version)
        data = {
            'device_type':self.device_type,
            'device_model': self.device_model,
            'fw_version_major': self.fw_version_major,
            'fw_version_minor': self.fw_version_minor
        }

        return data

    def getDeviceID(self):
        self.update(Message.gen_device_id)
        return self.device_id

    def getVoltage(self):
        self.update(Message.gen_voltage)
        return self.voltage

    def getSimpleDistanceData(self):
        self.update(Message.es_distance_simple)
        data = {
            'distance': self.distance,
            'confidence': self.confidence
        }
        return data


    def getDistanceData(self):
        self.update(Message.es_distance)
        data = {
                'distance': self.distance,
                'confidence': self.confidence,
                'pulse_usec': self.pulse_usec,
                'ping_number': self.ping_number,
                'start_mm': self.start_mm,
                'length_mm': self.length_mm,
                'gain_index': self.gain_index
        }
        return data

    def getProfile(self):
        self.update(Message.es_profile)
        data = {
                'distance': self.distance,
                'confidence': self.confidence,
                'pulse_usec': self.pulse_usec,
                'ping_number': self.ping_number,
                'start_mm': self.start_mm,
                'length_mm': self.length_mm,
                'gain_index': self.gain_index,
                'num_points': self.num_points,
                'points': self.points
        }
        return data

    def getRange(self):
        self.update(Message.es_range)
        data = {
            'start_mm':self.start_mm,
            'length_mm': self.length_mm
        }
        return data

    def getMode(self):
        self.update(Message.es_mode)
        return self.auto_manual

    def getRate(self):
        self.update(Message.es_rate)
        return self.pulse_usec

    def getGain(self):
        self.update(Message.es_gain)
        return self.gain_index

    def getPulseLength(self):
        self.update(Message.es_pulse)
        return self.pulse_usec


    #Internal
    #########

    #This will create a CRC of the message and check it against the sent one
    def validateChecksum(self, message, claimedChecksum):
        checksum = evaluateChecksum(message)
        return (checksum == claimedChecksum)

    #Return a list of the data in the header
    def buildHeader(self, length, messageID, destinationID):
        headerData = [self.validation_1, self.validation_2, length, messageID, 0, destinationID]
        return headerData

    #Pack the header so it can be sent
    def packHeader(self, headerData):
        headerPacked = struct.pack(self.msg_header, *headerData)
        return headerPacked

    #Pack the payload so it can be sent
    def packPayload(self, payloadFormat, payloadRaw):
        if (payloadRaw == []):
            return
        payloadPacked = struct.pack(payloadFormat, *payloadRaw)
        return payloadPacked

    #Checksum = sum(0 -> n) & 0xffff
    #Returns true if checksum match
    def evaluateChecksum(self, h, p, c):
        hUnpacked = struct.unpack("<BBBBBBBB", h)
        pFormat = '<' + (len(p) * 'B')
        pUnpacked = struct.unpack(pFormat, p)

        sumOfBytes = 0
        for i in range(0, len(h)):
            sumOfBytes += hUnpacked[i]
        for i in range(0, len(p)):
            sumOfBytes += pUnpacked[i]

        checksum = sumOfBytes & 0xffff
        return checksum == c

    #Checksum = sum(0 -> n) & 0xffff
    def buildChecksum(self, h, p):
        hUnpacked = struct.unpack("<BBBBBBBB", h)
        pFormat = '<' + (len(p) * 'B')
        pUnpacked = struct.unpack(pFormat, p)

        hSize = len(h)
        pSize = len(p)
        sumOfBytes = 0
        for i in range(0, hSize):
            sumOfBytes += hUnpacked[i]
        for i in range(0, pSize):
            sumOfBytes += pUnpacked[i]

        checksum = sumOfBytes & 0xffff
        return checksum

    def packChecksum(self, c):
        return struct.pack(self.msg_checksum, c)

    #Metadata Format
    msg_header   = '<ccHHBB'
    msg_checksum = '<H'

    #Message Dictionary
    messages = {
        Message.gen_goto_bootloader.id: Message.gen_goto_bootloader,
        Message.gen_version.id: Message.gen_version,
        Message.gen_reset.id: Message.gen_reset,
        Message.gen_device_id.id: Message.gen_device_id,
        Message.gen_new_data.id: Message.gen_new_data,
        Message.gen_cmd_request.id: Message.gen_cmd_request,
        Message.gen_voltage.id: Message.gen_voltage,
        Message.sonar_velocity.id: Message.sonar_velocity,
        Message.es_distance_simple.id: Message.es_distance_simple,
        Message.es_distance.id: Message.es_distance,
        Message.es_profile.id: Message.es_profile,
        Message.es_range.id: Message.es_range,
        Message.es_mode.id: Message.es_mode,
        Message.es_rate.id: Message.es_rate,
        Message.es_gain.id: Message.es_gain,
        Message.es_pulse.id: Message.es_pulse
    }
