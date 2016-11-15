#!/usr/bin/python -u
#Ping.py

import struct
import serial

class Ping1D:
    #Sonar report packet
    #452 Bytes
    packetFormat = "<ccHHhiiiiihhhhiIIhHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHcc"

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

    #Open the serial port
    #ser = serial.Serial('/dev/tty.usbserial-A5059KLC', 115200)
    ser = serial.Serial('/dev/ttyUSB0', 115200)


    def __init__(self):
        pass

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
        buf = []
        data = ""

        try:
            #Burn through data until start signal
            while(self.ser.read() != "s"):
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


    #Accessor Methods
    ################

    #Returns a string of the version number
    def getVersion(self):
        return (str(self.fw_version_major) + "." + str(fw_version_minor))

    #Returns the number of data points in the last ping
    def getNumResults(self):
        return self.num_results

    #Returns the operating voltage in mV
    def getVoltage(self):
        return self.supply_millivolts

    #Returns the shallowest depth that Ping will look at
    def getStartDepth(self):
        return self.start_mm

    #Returns the range of depth that is being scanned. Beginning at the start depth.
    def getDepthRange(self):
        return self.length_mm

    #Returns the best guess for this individual ping. It is recommended to use getDepth() instead.
    def getInstantDepth(self):
        return self.this_ping_depth_mm

    #Returns the most recent smoothed depth reading.
    def getDepth(self):
        return self.smoothed_depth_mm

    #Returns the confidence in the depth measurement
    def getConfidence(self):
        return self.smoothed_depth_confidence_percent

    #Returns the duration of the sent ping
    def getPingDuration(self):
        return self.ping_duration_usec

    #Retuns the index of the analog gain
    def getGain(self):
        return self.analog_gain

    #Returns the number of pings that Ping has sent
    def getPingNumber(self):
        return self.ping_number

    #Returns the milliseconds of uptime
    def getTimestamp(self):
        return self.timestamp_msec

    #Returns the index of the depth reading that was chosen as the bottom
    def getBottomIndex(self):
        return self.index_of_bottom_result

    #Returns list of all results from last ping
    def getResults(self):
        return self.results
