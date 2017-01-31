#!/usr/bin/python -u
#Ping.py

import sys
import struct
import serial
import getopt
import socket


class Ping1D:
    #Metadata Formats
    ############
    #Header
    headerFormat = '<ccHHH'
    #Checksum
    checksumFormat = '<H'

    #Message Formats
    ################
    msgACKFormat = '<H'                                           #ACK
    msgNACKFormat = '<Hs'                                         #NACK
    msgAltitudeMessageFormat = '<IIB'                             #Altitude
    msgFullProfileFormat = '<IIHHIIIhhHIIHH200B'                  #Full Profile
    msgGeneralInfoFormat = '<HHHH'                                #General Info
    msgAsciiTextFormat = '<B'                                     #ASCII Text
    msgConfigFormat = ''                                          #Config
    msgRequestFormat = '<HH'                                      #Request
    msgRangeFormat = '<HH'                                        #Range
    msgDebugFormat = '<BBHH'                                      #Debug
    msgSetSpeedFormat = '<I'                                      #Set C

    #Profile Message
    #200 Points
    profileMessageFormat = '<BIIIHBI200B'
    #Status Message
    statusMessageFormat = "<HHHB"

    instructions = "Usage: python simplePingExample.py -d <device_name>"

    #UDP input
    # UDP_IP="0.0.0.0"
    # UDP_PORT=5009
    #
    # sock = socket.socket( socket.AF_INET, # Internet
    #                   socket.SOCK_DGRAM ) # UDP
    # sock.bind( (UDP_IP,UDP_PORT) )

    #Parameters
    fw_version_major                      = 0
    fw_version_minor                      = 0
    num_results                           = 0
    supply_millivolts                     = 0
    start_mm                              = 0
    length_mm                             = 0
    this_ping_distance_mm                 = 0
    smoothed_distance_mm                  = 0
    smoothed_distance_confidence_percent  = 0
    ping_duration_usec                    = 0
    goertzel_n                            = 0
    goertzel_m                            = 0
    analog_gain                           = 0
    ping_number                           = 0
    timestamp_msec                        = 0
    index_of_bottom_result                = 0
    results                               = [0]*200

    #Start signal detection
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

    #Read and Update
    def updateSonar(self):
        #TODO this is temporary to get the altitude message only
        self.request(0x3, 1)
        sonarData = self.readSonar()
        if (sonarData != None):
           self.handleSonar(sonarData)

    #Update values from new sonar report
    def handleSonar(self, sonarData):
        messageID = sonarData[0]
        payloadPacked = sonarData[1]

        if  (messageID == 1):
            print("ACK")

        elif(messageID == 2):
            payload = struct.unpack(self.msgNACKFormat, payloadPacked)
            print("Error: " + payload[1])
            print("NACK")

        elif(messageID == 3):
            payload = struct.unpack(self.msgAltitudeMessageFormat, payloadPacked)
            self.ping_range                           = payload[0]
            self.smoothed_distance_mm                 = payload[1]
            self.smoothed_distance_confidence_percent = payload[2]

        elif(messageID == 4):
            print("Full Profile")

        elif(messageID == 6):
            print("General Info")

        elif(messageID == 7):
            print("Ascii")

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
            header = struct.unpack(self.headerFormat, headerRaw)

            #Look at header metadata
            payloadLength = header[2]
            messageID = header[3]

            #Get the message body
            for i in range(0, payloadLength):
                byte = self.ser.read()
                payloadRaw += struct.pack("<c", byte)

            #Get the Checksum
            for i in range(0, 2):
                byte = self.ser.read()
                checksumRaw += struct.pack("<c", byte)

            #Decode the checksum
            checksum = struct.unpack(self.checksumFormat, checksumRaw)[0]
            checksumMatch = self.evaluateChecksum(headerRaw, payloadRaw, checksum)

            #Return None if there is a checksum error
            if (not checksumMatch):
                return None

            return (messageID, payloadRaw)

        except Exception as e:
            print "Error: "+str(e)
            pass

    #Control Methods
    ###################

    #Request the given message ID
    def request(self, m_id, m_rate):
        payloadData = [m_id, m_rate]
        self.sendMessage(0x101, self.msgRequestFormat, payloadData)

    #Manually set the scanning range
    def setRange(self, auto, start, range):
        #TODO implement
        return false

    #Set special debug options
    def setDebugOptions(self, raw, auto, gain, c):
        #TODO implement
        return false

    #Used for sending of all messages
    def sendMessage(self, m_id, m_format, m_payload):
        #Pack payload first, because metadata is required for the header
        finalPayload = self.packPayload(m_format, m_payload)

        #Needed to build header
        payloadLength = struct.calcsize(m_format)

        #Create and pack header
        header = self.buildHeader(payloadLength, m_id)
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
        return (str(self.fw_version_major) + "." + str(self.fw_version_minor))

    #Returns the number of data points in the last ping
    def getNumResults(self):
        return self.num_results

    #Returns the operating voltage in mV
    def getVoltage(self):
        return self.supply_millivolts

    #Returns the closest distance that Ping will look at, in mm
    def getScanStart(self):
        return self.start_mm

    #Returns the range that is being scanned in mm. Beginning at the start distance.
    def getScanRange(self):
        return self.length_mm

    #Returns the best guess for this individual ping in mm. It is recommended to use getDistance() instead
    def getInstantDistance(self):
        return self.this_ping_distance_mm

    #Returns the most recent smoothed distance reading in mm
    def getDistance(self):
        return self.smoothed_distance_mm

    #Returns the confidence in the distance measurement, as a percentage
    def getConfidence(self):
        return self.smoothed_distance_confidence_percent

    #Returns the duration of the sent ping, in microseconds
    def getPingDuration(self):
        return self.ping_duration_usec

    #Retuns the index of the analog gain
    def getGain(self):
        return self.analog_gain

    #Returns the number of pings that Ping has sent
    def getPingNumber(self):
        return self.ping_number

    #Returns the uptime, in milliseconds
    def getTimestamp(self):
        return self.timestamp_msec

    #Returns the index of the distance reading that was chosen as the bottom
    def getBottomIndex(self):
        return self.index_of_bottom_result

    #Returns list of all results from last ping. Each point is on a scale of 0 to 255
    def getResults(self):
        return self.results

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
    def buildHeader(self, length, messageID):
        headerData = [self.validation_1, self.validation_2, length, messageID, 0]
        return headerData

    #Pack the header so it can be sent
    def packHeader(self, headerData):
        headerPacked = struct.pack(self.headerFormat, *headerData)
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
        return struct.pack(self.checksumFormat, c)
