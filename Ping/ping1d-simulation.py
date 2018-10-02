from Ping import PingMessage
import serial
import socket
import time
from collections import deque
import errno

client = None

parser = PingMessage.PingParser()

## Socket to serve on
sockit = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockit.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockit.setblocking(False)
sockit.bind(('0.0.0.0', 6676))

def distance():
    return 1000 * sin(time.time())

def confidence():
    return 100 * cos(time.time())

def profile():
    return range(0,200)

def temperature():
    return 3500 * sin(time.time())

def handleMessage(message):
    print("handling message: %s" % message)
    print("payload length: %s" % message.payload_length)

    if message.payload_length == 0:
        print("sending message: %s" % message.message_id)

        if message.message_id == PingMessage.PING1D_FIRMWARE_VERSION:
            msg = PingMessage.PingMessage(PingMessage.PING1D_FIRMWARE_VERSION)
            msg.firmware_version_minor = 6
            msg.firmware_version_major = 76
            msg.packMsgData()
            write(msg.msgData)
        if message.message_id == PingMessage.PING1D_VOLTAGE_5:
            msg = PingMessage.PingMessage(PingMessage.PING1D_VOLTAGE_5)
            msg.voltage_5 = 685
            msg.packMsgData()
            write(msg.msgData)

def read():
        try:
            global client
            data, client = sockit.recvfrom(4096)

            # digest data coming in from client
            for byte in data:
                if parser.parseByte(byte) == PingMessage.PingParser.NEW_MESSAGE:
                    print("got message from %s: %s" % (client, parser.rxMsg))
                    handleMessage(parser.rxMsg)

        except Exception as e:
            if e.errno == errno.EAGAIN:
              pass # waiting for data
            else:
              print("Error reading data", e)

def write(data):
    global client
    print("client: %s" % str(client))

    if client is not None:
        print("sending message: %s" % parser.rxMsg)
        sockit.sendto(data, client)

while True:
    read()
