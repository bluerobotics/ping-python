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

        unpacked = struct.unpack("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",data)
        print(unpacked)
        print()

    except:
        pass
