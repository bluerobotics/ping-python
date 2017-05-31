#!/usr/bin/python -u
#Ping.py

import sys
import struct
import serial
import getopt
import socket

class Ping1D:
    #Metadata Format
    ############
    msg_header   = '<ccHHBB'
    msg_checksum = '<H'

    #General Messages
    ################
    gen_goto_bootloader     = {'id': 100, 'format': ''}
    gen_version             = {'id': 101, 'format': '<BBHH'}
    gen_reset               = {'id': 102, 'format': ''}
    gen_device_id           = {'id': 110, 'format': '<B'}
    gen_new_data            = {'id': 112, 'format': '<B'}
    gen_cmd_request         = {'id': 120, 'format': '<H'}
    gen_voltage             = {'id': 130, 'format': '<H'}

    #Sonar Messages
    ####################
    sonar_velocity          = {'id': 1000, 'format': '<I'}

    #EchoSounder Messages
    #####################
    es_distance_simple      = {'id': 1100, 'format': '<IB'}
    es_distance             = {'id': 1101, 'format': '<IBH4I'}
    es_profile              = {'id': 1102, 'format': '<IBH4IH200B'}
    es_range                = {'id': 1110, 'format': '<II'}
    es_mode                 = {'id': 1111, 'format': '<B'}
    es_rate                 = {'id': 1112, 'format': '<H'}
    es_gain                 = {'id': 1113, 'format': '<I'}
    es_pulse                = {'id': 1114, 'format': '<H'}

    #Message Dictionary
    #####################
    messages = {
        'gen_goto_bootloader': gen_goto_bootloader,
        'gen_version': gen_version,
        'gen_reset': gen_reset,
        'gen_device_id': gen_device_id,
        'gen_new_data': gen_new_data,
        'gen_cmd_request': gen_cmd_request,
        'gen_voltage': gen_voltage,
        'sonar_velocity': sonar_velocity,
        'es_distance_simple': es_distance_simple,
        'es_distance': es_distance,
        'es_profile': es_profile,
        'es_range': es_range,
        'es_mode': es_mode,
        'es_rate': es_rate,
        'es_gain': es_gain,
        'es_pulse': es_pulse
    }


    instructions = "Usage: python simplePingExample.py -d <device_name>"

    #UDP input
    # UDP_IP="0.0.0.0"
    # UDP_PORT=5009
    #
    # sock = socket.socket( socket.AF_INET, # Internet
    #                   socket.SOCK_DGRAM ) # UDP
    # sock.bind( (UDP_IP,UDP_PORT) )

    #Parameters

    dev_id                                    = 255
    dev_type                                  = 0
    dev_model                                 = 0
    dev_fw_version_major                      = 0
    dev_fw_version_minor                      = 0
    dev_voltage                               = 0

    dev_distance                              = 0
    dev_confidence                            = 0


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
        self.update(self.messages['gen_device_id'])
        self.update(self.messages['gen_version'])
        self.update(self.messages['gen_voltage'])

    #Read and Update
    def update(self, message):
        self.request(message['id'])
        sonarData = self.readSonar()
        if (sonarData != None):
           self.handleSonar(sonarData)

    #Update values from new sonar report
    def handleSonar(self, sonarData):
        messageID = sonarData[0]
        payloadPacked = sonarData[1]

        ##TODO make this loop through the dict of messages rather than an if/elif

        if (messageID == self.messages['gen_version']['id']):
            message = self.messages['gen_version']
            payload = struct.unpack(message['format'], payloadPacked)
            self.dev_type = payload[0]
            self.dev_model = payload[1]
            self.dev_fw_version_major = payload[2]
            self.dev_fw_version_minor = payload[3]

        elif (messageID == self.messages['gen_device_id']['id']):
            message = self.messages['gen_device_id']
            payload = struct.unpack(message['format'], payloadPacked)
            self.dev_id = payload[0]

        elif (messageID == self.messages['gen_voltage']['id']):
            message = self.messages['gen_voltage']
            payload = struct.unpack(message['format'], payloadPacked)
            self.dev_voltage = payload[0]

        elif (messageID == self.messages['es_distance_simple']['id']):
            message = self.messages['es_distance_simple']
            payload = struct.unpack(message['format'], payloadPacked)
            self.dev_distance = payload[0]
            self.dev_confidence = payload[1]

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
        self.sendMessage(self.messages['gen_cmd_request'], payloadData, self.dev_id)

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
        finalPayload = self.packPayload(m_message['format'], m_payload)

        #Needed to build header
        payloadLength = struct.calcsize(m_message['format'])

        #Create and pack header
        header = self.buildHeader(payloadLength, m_message['id'], m_destination)
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

    ##################
    #TODO: Update these to match the new Protocol
    ##################

    #Returns a string of the version number
    def getVersions(self):
        self.update(101)
        data = {
            'device_type':self.dev_type,
            'device_model': self.dev_model,
            'fw_version_major': self.dev_fw_version_major,
            'fw_version_minor': self.dev_fw_version_minor
        }

        return data

    def getDeviceID(self):
        self.update(110)
        return self.dev_id

    def getVoltage():
        self.update(130)
        return self.dev_voltage

    def getSimpleDistance():
        self.update(1100)
        return {'distance': self.dev_distance, 'confidence': self.dev_confidence}

    def getDistance():
        self.update(1101)
        data = {}
        return data

    def getProfile():
        self.update(1102)
        data = {}
        return data

    def getRange():
        self.update(1110)
        return 0

    def getMode():
        return 0

    def getRate():
        return 0

    def getGain():
        return 0

    def getPulseLength():
        return 0


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
