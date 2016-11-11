import struct
import serial

#Open the serial port
ser = serial.Serial('/dev/ttyUSB0', 115200)

while True:
    buf = []
    data = ""

    try:
        #Burn through data until start signal
        while(ser.read() != "s"):
            true
        #Check second start signal
        if (ser.read() != "s"):
            break

        #Add start signal to buffer, since we have a valid message
        buf.append("s")
        buf.append("s")
        data += struct.pack("B", 83)
        data += struct.pack("B", 83)

        #Get the content of the message
        #Message is 444 bytes long
        for i in range(0,442):
            byte = ser.read()
            data += struct.pack("c", byte)
            buf.append(byte)

        #This one works and is just bytes. 444 Bytes long.
        #unpacked = struct.unpack("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",data)

        #This one works with all of the metadata. But contains bytes for the data.
        #There are 394 bytes for the profile data. Meaning 197 data points.
        #unpacked=  struct.unpack("ccHHhiiiiihhhhiIIhBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBcc",data)

        #This one is for experimentation.. I found that this one works, but it cuts off early. The end characters are not reached.
        #For the depth profile data, it only has 197 values when I expect 200.
        unpacked = struct.unpack("ccHHhiiiiihhhhiIIhHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH",data)

        #This should technically be correct for everything, but doesn't work
        #unpacked = struct.unpack("BBHHhiiiiihhhhiIIhHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHBB",data)


        print(unpacked)
        print()

    except:
        pass
