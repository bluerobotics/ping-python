#!/usr/bin/python -u
#Ping.py

import sys
import struct
import serial
import getopt

class Ping1D:
    #Sonar report packet
    #452 Bytes
    packetFormat = "<ccHHhiiiiihhhhiIIhHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHcc"

    instructions = "Usage: python simplePingExample.py -d <device_name>"

    #Parameters
    fw_version_major                      = 0
    fw_version_minor                      = 0
    num_results                           = 0
    supply_millivolts                     = 0
    start_mm                              = 0
    length_mm                             = 0
    this_ping_depth_mm                    = 0
    smoothed_depth_mm                     = 0
    smoothed_depth_confidence_percent     = 0
    ping_duration_usec                    = 0
    goertzel_n                            = 0
    goertzel_m                            = 0
    analog_gain                           = 0
    ping_number                           = 0
    timestamp_msec                        = 0
    index_of_bottom_result                = 0
    results                               = [0]*200

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
        self.this_ping_depth_mm                    = sonarData[8]
        self.smoothed_depth_mm                     = sonarData[9]
        self.smoothed_depth_confidence_percent     = sonarData[10]
        self.ping_duration_usec                    = sonarData[11]
        self.goertzel_n                            = sonarData[12]
        self.goertzel_m                            = sonarData[13]
        self.analog_gain                           = sonarData[14]
        self.ping_number                           = sonarData[15]
        self.timestamp_msec                        = sonarData[16]
        self.index_of_bottom_result                = sonarData[17]

        for i in range(0,self.num_results):
            self.results[i] = sonarData[18 + i]

    #Read in sonar data over serial
    def readSonar(self):
        timeout = 10000
        readCount = 0
        buf = []
        data = ""

        try:
            #Burn through data until start signal
            while(self.ser.read() != "s"):
                readCount += 1
                if (readCount > timeout):
                    print("Serial Read Timeout. Check device and connections")
                    exit(1)
                pass
            #Check second start signal
            if (self.ser.read() != "s"):
                return None

            #Add start signal to buffer, since we have a valid message
            buf.append("s")
            buf.append("s")
            data += struct.pack("<B", 83)
            data += struct.pack("<B", 83)

            #Get the content of the message
            for i in range(0,450):
                byte = self.ser.read()
                data += struct.pack("<c", byte)
                buf.append(byte)

            unpacked = struct.unpack(self.packetFormat, data)
            return unpacked
            #print(unpacked)

        except Exception as e:
            print "Error: "+str(e)
            pass


    #This will create a CRC of the message and check it against the sent one
    def validateCRC(message):
        return false

    #Control Methods
    ###################

    #Set mandatory configuration settings
    #Run once on boot
    #Rate, speed of sound in water
    def setConfiguration(self, rate, c):
        #TODO implement
        return false

    #Request the given message ID
    def request(self, id):
        #TODO implement
        return false

    #Manually set the scanning range
    def setRange(self, auto, start, range):
        #TODO implement
        return false

    #Set special debug options
    def setDebugOptions(self, raw, auto, gain, c):
        #TODO implement
        return false

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

    #Returns the shallowest depth that Ping will look at, in mm
    def getStartDepth(self):
        return self.start_mm

    #Returns the range of depth that is being scanned in mm. Beginning at the start depth
    def getDepthRange(self):
        return self.length_mm

    #Returns the best guess for this individual ping in mm. It is recommended to use getDepth() instead
    def getInstantDepth(self):
        return self.this_ping_depth_mm

    #Returns the most recent smoothed depth reading in mm
    def getDepth(self):
        return self.smoothed_depth_mm

    #Returns the confidence in the depth measurement, as a percentage
    def getConfidence(self):
        return self.smoothed_depth_confidence_percent

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

    #Returns the index of the depth reading that was chosen as the bottom
    def getBottomIndex(self):
        return self.index_of_bottom_result

    #Returns list of all results from last ping. Each point is on a scale of 0 to 255
    def getResults(self):
        return self.results
