#!/usr/bin/python -u
#Ping.py

import sys
import struct
import serial
import getopt
import socket

class Ping1D:
    #Early Sonar report packet
    #452 Bytes
    packetFormat = "<ccHHhiiiiihhhhiIIhHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHcc"

    #Meta Formats
    ############
    #Header
    headerFormat = "<BBHHH"
    #Checksum
    checksumFormat = "<H"

    #Message Formats
    ################
    #Altitude Message
    altitudeMessageFormat = '<IIB'
    #Full Profile Message
    fullProfileFormat = '<IIHHIIIhhHIIHH' + 'B' * 200

    #Profile Message
    #200 Points
    profileMessageFormat = '<BIIIHBI' + 'B' * 200
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
    validation_1 = 'B'
    validation_2 = 'R'
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

        sonarData = self.readSonar()
        if (sonarData != None):
            self.handleSonar(sonarData)

    #Update values from new sonar report
    def handleSonar(self, sonarData):
        self.fw_version_major                      = sonarData[2]
        self.fw_version_minor                      = sonarData[3]
        self.num_results                           = sonarData[4]
        self.supply_millivolts                     = sonarData[5]
        self.start_mm                              = sonarData[6]
        self.length_mm                             = sonarData[7]
        self.this_ping_distance_mm                 = sonarData[8]
        self.smoothed_distance_mm                  = sonarData[9]
        self.smoothed_distance_confidence_percent  = sonarData[10]
        self.ping_duration_usec                    = sonarData[11]
        self.goertzel_n                            = sonarData[12]
        self.goertzel_m                            = sonarData[13]
        self.analog_gain                           = sonarData[14]
        self.ping_number                           = sonarData[15]
        self.timestamp_msec                        = sonarData[16]
        self.index_of_bottom_result                = sonarData[17]

        for i in range(0,self.num_results):
            self.results[i] = sonarData[18 + i]

    def readSonar(self):
        timeout = 10000
        readCount = 0
        buf = []

        headerRaw = []
        bodyRaw = []
        checksumRaw = []

        data = ""
        start_signal_found = False

        print("readSonar()")

        try:
            #Burn through data until start signal
            while(not start_signal_found):
                #Put new byte in second index
                self.test_2 = self.ser.read()

                #Check if start signal
                if((self.test_1 == self.validation_1) and (self.test_2 == self.validation_2)):
                    print("Found start")
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
            buf.append(validation_1)
            buf.append(validation_2)
            data += struct.pack("<B", validation_1)
            data += struct.pack("<B", validation_2)


            #Get the header
            for i in range(2, 7):
                byte = self.ser.read()
                print(byte)
                headerRaw += struct.pack("<B", byte)

            #Decode Header
            header = struct.unpack(self.headerFormat, header)

            #Find how long the message body is
            bodyLength = header[2]
            print(bodyLength)
            #Get the message body

            #Get the Checksum


            # for i in range(0,450):
            #     byte = self.ser.read()
            #     data += struct.pack("<c", byte)
            #     buf.append(byte)
            #
            # unpacked = struct.unpack(self.packetFormat, data)
            return unpacked

        except Exception as e:
            print "Error: "+str(e)
            pass

    #Control Methods
    ###################

    #Set mandatory configuration settings
    #Run once on boot
    #Rate, speed of sound in water
    def setConfiguration(self, rate, c):
        #TODO implement
        return false

    #Request the given message ID
    def request(self, id, rate):

        self.sendMessage(id, payload)
        return false

    #Manually set the scanning range
    def setRange(self, auto, start, range):
        #TODO implement
        return false

    #Set special debug options
    def setDebugOptions(self, raw, auto, gain, c):
        #TODO implement
        return false

    def sendMessage(self, id, payload):


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
    #
    # def initUDP(self, ip, port):
    #     UDP_IP="0.0.0.0"
    #     UDP_PORT="5009"
    #     self.sock = socket.socket( socket.AF_INET, # Internet
    #                   socket.SOCK_DGRAM ) # UDP
    #
    #     self.sock.bind( (UDP_IP,UDP_PORT) )

    #This will create a CRC of the message and check it against the sent one
    def validateChecksum(message, claimedChecksum):
        #TODO Length of message must exclude checksum
        messageSize = len(message)
        checksum = 0

        for i in range(0, messageSize):
            checksum += message[i]

        checksum = checksum & 0xffff

        return (checksum == claimedChecksum)
