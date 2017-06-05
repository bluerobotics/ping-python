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
    device_id                                    = 255
    device_type                                  = 0
    device_model                                 = 0
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
    #TODO store profile points
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

    #####################
    #TODO: Update these to match the new Protocol
    #####################

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

    def getSimpleDistance(self):
        self.update(Message.es_distance_simple)
        data = {
            'distance': self.distance,
            'confidence': self.confidence
        }
        return data


    def getDistance(self):
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

    #TODO Add returning of points
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

    # def initUDP(self, ip, port):
    #     UDP_IP="0.0.0.0"
    #     UDP_PORT="5009"
    #     self.sock = socket.socket( socket.AF_INET, # Internet
    #                   socket.SOCK_DGRAM ) # UDP
    #
    #     self.sock.bind( (UDP_IP,UDP_PORT) )

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

        hSize = len(h)
        pSize = len(p)
        sumOfBytes = 0
        for i in range(0, hSize):
            sumOfBytes += hUnpacked[i]
        for i in range(0, pSize):
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



    #Message Handling
    #################

    #def handle_payload(self, msg, payload):

            #self.__settattr__(attr,payload[i])


    #General Messages
    # def p_goto_bootloader(self, payload):
    #     print("Received Goto Bootloader Message")
    #
    # def p_gen_version(self, payload):
    #     self.dev_type             = payload[0]
    #     self.dev_model            = payload[1]
    #     self.dev_fw_version_major = payload[2]
    #     self.dev_fw_version_minor = payload[3]
    #
    # def p_gen_reset(self, payload):
    #     #TODO Figure out what this should do
    #     print("Received Reset Message")
    #
    # def p_gen_device_id(self, payload):
    #     self.dev_id               = payload[0]
    #
    # def p_gen_new_data(self, payload):
    #     print("Received New Data Message")
    #
    # def p_gen_cmd_request(self, payload):
    #     print("Received Request Message")
    #
    # def p_gen_voltage(self, payload):
    #     self.dev_voltage          = payload[0]
    #
    # #Sonar Messages
    # def p_sonar_velocity(self, payload):
    #     self.dev_c_water          = payload[0]
    #
    # #EchoSounder Messages
    # def p_es_distance_simple(self, payload):
    #     self.dev_distance         = payload[0]
    #     self.dev_confidence       = payload[1]
    # def p_es_distance(self, payload):
    #     self.dev_distance         = payload[0]
    #     self.dev_confidence       = payload[1]
    #     self.dev_pulse_usec       = payload[2]
    #     self.dev_ping_number      = payload[3]
    #     self.dev_start_mm         = payload[4]
    #     self.dev_length_mm        = payload[5]
    #     self.dev_gain_index       = payload[6]
    # def p_es_profile(self, payload):
    #     self.dev_distance         = payload[0]
    #     self.dev_confidence       = payload[1]
    #     self.dev_pulse_usec       = payload[2]
    #     self.dev_ping_number      = payload[3]
    #     self.dev_start_mm         = payload[4]
    #     self.dev_length_mm        = payload[5]
    #     self.dev_gain_index       = payload[6]
    #     self.dev_num_points       = payload[7]
    #     #TODO Store the profile data
    # def p_range(self, payload):
    #     self.dev_start_mm         = payload[0]
    #     self.dev_length_mm        = payload[1]
    # def p_mode(self, payload):
    #     self.dev_auto_manual      = payload[0]
    # def p_rate(self, payload):
    #     self.dev_msec_per_ping    = payload[0]
    # def p_gain(self, payload):
    #     self.dev_gain_index       = payload[0]
    # def p_pulse(self, payload):
    #     self.dev_pulse_usec       = payload[0]
    #

    #Metadata Format
    msg_header   = '<ccHHBB'
    msg_checksum = '<H'

    #General Messages
    # gen_goto_bootloader     = {'id': 100, 'format': '<'}
    # gen_version             = {'id': 101, 'format': '<BBHH', 'processor': p_gen_version}
    # gen_reset               = {'id': 102, 'format': '<'}
    # gen_device_id           = {'id': 110, 'format': '<B', 'processor': p_gen_device_id}
    # gen_new_data            = {'id': 112, 'format': '<B'}
    # gen_cmd_request         = {'id': 120, 'format': '<H'}
    # gen_voltage             = {'id': 130, 'format': '<H', 'processor': p_gen_voltage}
    #
    # #Sonar Messages
    # sonar_velocity          = {'id': 1000, 'format': '<I'}
    #
    # #EchoSounder Messages
    # es_distance_simple      = {'id': 1100, 'format': '<IB', 'processor': p_es_distance_simple}
    # es_distance             = {'id': 1101, 'format': '<IBH4I'}
    # es_profile              = {'id': 1102, 'format': '<IBH4IH200B'}
    # es_range                = {'id': 1110, 'format': '<II'}
    # es_mode                 = {'id': 1111, 'format': '<B'}
    # es_rate                 = {'id': 1112, 'format': '<H'}
    # es_gain                 = {'id': 1113, 'format': '<I'}
    # es_pulse                = {'id': 1114, 'format': '<H'}

    #Message Dictionary
    messages = {
        100: Message.gen_goto_bootloader,
        101: Message.gen_version,
        102: Message.gen_reset,
        110: Message.gen_device_id,
        112: Message.gen_new_data,
        120: Message.gen_cmd_request,
        130: Message.gen_voltage,
        1000: Message.sonar_velocity,
        1100: Message.es_distance_simple,
        1101: Message.es_distance,
        1102: Message.es_profile,
        1110: Message.es_range,
        1111: Message.es_mode,
        1112: Message.es_rate,
        1113: Message.es_gain,
        1114: Message.es_pulse,
    }
