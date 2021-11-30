#!/usr/bin/env python3

# PingMessage.py
# Python implementation of the Blue Robotics 'Ping' binary message protocol

import struct
from brping import definitions
payload_dict = definitions.payload_dict_all
asciiMsgs = [definitions.COMMON_NACK, definitions.COMMON_ASCII_TEXT]
variable_msgs = [definitions.PING1D_PROFILE, definitions.PING360_DEVICE_DATA, ]


class PingMessage(object):
    ## header start byte 1
    start_1 = ord("B")

    ## header start byte 2
    start_2 = ord("R")

    ## header struct format
    header_format = "BBHHBB"

    ## checksum struct format
    checksum_format = "H"

    ## data endianness for struct formatting
    endianess = "<"

    ## names of the header fields
    header_field_names = (
        "start_1",
        "start_2",
        "payload_length",
        "message_id",
        "src_device_id",
        "dst_device_id")

    ## number of bytes in a header
    headerLength = 8

    ## number of bytes in a checksum
    checksumLength = 2

    ## Messge constructor
    #
    # @par Ex request:
    # @code
    # m = PingMessage()
    # m.request_id = m_id
    # m.pack_msg_data()
    # write(m.msg_data)
    # @endcode
    #
    # @par Ex set:
    # @code
    # m = PingMessage(PING1D_SET_RANGE)
    # m.start_mm = 1000
    # m.length_mm = 2000
    # m.update_checksum()
    # write(m.msg_data)
    # @endcode
    #
    # @par Ex receive:
    # @code
    # m = PingMessage(rxByteArray)
    # if m.message_id == PING1D_RANGE
    #     start_mm = m.start_mm
    #     length_mm = m.length_mm
    # @endcode
    def __init__(self, msg_id=0, msg_data=None):
        ## The message id
        self.message_id = msg_id

        ## The request id for request messages
        self.request_id = None

        ## The message destination
        self.dst_device_id = 0
        ## The message source
        self.src_device_id = 0
        ## The message checksum
        self.checksum = 0

        ## The raw data buffer for this message
        # update with pack_msg_data()
        self.msg_data = None

        # Constructor 1: make a pingmessage object from a binary data buffer
        # (for receiving + unpacking)
        if msg_data is not None:
            if not self.unpack_msg_data(msg_data):
                # Attempted to create an unknown message
                return
        # Constructor 2: make a pingmessage object cooresponding to a message
        # id, with field members ready to access and populate
        # (for packing + transmitting)
        else:

            try:
                ## The name of this message
                self.name = payload_dict[self.message_id]["name"]

                ## The field names of this message
                self.payload_field_names = payload_dict[self.message_id]["field_names"]

                # initialize payload field members
                for attr in self.payload_field_names:
                    setattr(self, attr, 0)

                # initialize vector fields
                if self.message_id in variable_msgs:
                    setattr(self, self.payload_field_names[-1], bytearray())

                ## Number of bytes in the message payload
                self.update_payload_length()

                ## The struct formatting string for the message payload
                self.payload_format = self.get_payload_format()

            # TODO handle better here, and catch Constructor 1 also
            except KeyError as e:
                print("message id not recognized: %d" % self.message_id, msg_data)
                raise e

    ## Pack object attributes into self.msg_data (bytearray)
    # @return self.msg_data
    def pack_msg_data(self):
        # necessary for variable length payloads
        # update using current contents for the variable length field
        self.update_payload_length()

        # Prepare struct packing format string
        msg_format = PingMessage.endianess + PingMessage.header_format + self.get_payload_format()

        # Prepare complete list of field names (header + payload)
        attrs = PingMessage.header_field_names + payload_dict[self.message_id]["field_names"]

        # Prepare iterable ordered list of values to pack
        values = []
        for attr in attrs:
            # this is a hack for requests
            if attr == "message_id" and self.request_id is not None:
                values.append(self.request_id)
            else:
                values.append(getattr(self, attr))

        # Pack message contents into bytearray
        self.msg_data = bytearray(struct.pack(msg_format, *values))

        # Update and append checksum
        self.msg_data += bytearray(struct.pack(PingMessage.endianess + PingMessage.checksum_format, self.update_checksum()))

        return self.msg_data

    ## Attempts to unpack a bytearray into object attributes
    # @Returns True if successful, False otherwise
    def unpack_msg_data(self, msg_data):
        self.msg_data = msg_data

        # Extract header
        header = struct.unpack(PingMessage.endianess + PingMessage.header_format, self.msg_data[0:PingMessage.headerLength])

        for i, attr in enumerate(PingMessage.header_field_names):
            setattr(self, attr, header[i])

        ## The name of this message
        try:
            self.name = payload_dict[self.message_id]["name"]
        except KeyError:
            print("Unknown message: ", self.message_id)
            return False

        ## The field names of this message
        self.payload_field_names = payload_dict[self.message_id]["field_names"]

        if self.payload_length > 0:
            ## The struct formatting string for the message payload
            self.payload_format = self.get_payload_format()

            # Extract payload
            try:
                payload = struct.unpack(PingMessage.endianess + self.payload_format, self.msg_data[PingMessage.headerLength:PingMessage.headerLength + self.payload_length])
            except Exception as e:
                print("error unpacking payload: %s" % e)
                print("msg_data: %s, header: %s" % (msg_data, header))
                print("format: %s, buf: %s" % (PingMessage.endianess + self.payload_format, self.msg_data[PingMessage.headerLength:PingMessage.headerLength + self.payload_length]))
                print(self.payload_format)
            else:  # only use payload if didn't raise exception
                for i, attr in enumerate(self.payload_field_names):
                    try:
                        setattr(self, attr, payload[i])
                    # empty trailing variable data field
                    except IndexError as e:
                        if self.message_id in variable_msgs:
                            setattr(self, attr, bytearray())
                            pass

        # Extract checksum
        self.checksum = struct.unpack(PingMessage.endianess + PingMessage.checksum_format, self.msg_data[PingMessage.headerLength + self.payload_length: PingMessage.headerLength + self.payload_length + PingMessage.checksumLength])[0]
        return True

    ## Calculate the checksum from the internal bytearray self.msg_data
    def calculate_checksum(self):
        return sum(self.msg_data[0:PingMessage.headerLength + self.payload_length]) & 0xffff

    ## Update the object checksum value
    # @return the object checksum value
    def update_checksum(self):
        self.checksum = self.calculate_checksum()
        return self.checksum

    ## Verify that the object checksum attribute is equal to the checksum calculated according to the internal bytearray self.msg_data
    def verify_checksum(self):
        return self.checksum == self.calculate_checksum()

    ## Update the payload_length attribute with the **current** payload length, including dynamic length fields (if present)
    def update_payload_length(self):
        if self.message_id in variable_msgs or self.message_id in asciiMsgs:
            # The last field self.payload_field_names[-1] is always the single dynamic-length field
            self.payload_length = payload_dict[self.message_id]["payload_length"] + len(getattr(self, self.payload_field_names[-1]))
        else:
            self.payload_length = payload_dict[self.message_id]["payload_length"]

    ## Get the python struct formatting string for the message payload
    # @return the payload struct format string
    def get_payload_format(self):
        # messages with variable length fields
        if self.message_id in variable_msgs or self.message_id in asciiMsgs:
            var_length = self.payload_length - payload_dict[self.message_id]["payload_length"]  # Subtract static length portion from payload length
            if var_length <= 0:
                return payload_dict[self.message_id]["format"]  # variable data portion is empty

            return payload_dict[self.message_id]["format"] + str(var_length) + "s"
        else: # messages with a static (constant) length
            return payload_dict[self.message_id]["format"]

    ## Dump object into string representation
    # @return string representation of the object
    def __repr__(self):
        header_string = "Header:"
        for attr in PingMessage.header_field_names:
            header_string += " " + attr + ": " + str(getattr(self, attr))

        if self.payload_length == 0:  # this is a hack/guard for empty body requests
            payload_string = ""
        else:
            payload_string = "Payload:"

            # handle variable length messages
            if self.message_id in variable_msgs:

                # static fields are handled as usual
                for attr in payload_dict[self.message_id]["field_names"][:-1]:
                    payload_string += "\n  - " + attr + ": " + str(getattr(self, attr))

                # the variable length field is always the last field
                attr = payload_dict[self.message_id]["field_names"][-1:][0]

                # format this field as a list of hex values (rather than a string if we did not perform this handling)
                payload_string += "\n  - " + attr + ": " + str([hex(item) for item in getattr(self, attr)])

            else:  # handling of static length messages and text messages
                for attr in payload_dict[self.message_id]["field_names"]:
                    payload_string += "\n  - " + attr + ": " + str(getattr(self, attr))

        representation = (
            "\n\n--------------------------------------------------\n"
            "ID: " + str(self.message_id) + " - " + self.name + "\n" +
            header_string + "\n" +
            payload_string + "\n" +
            "Checksum: " + str(self.checksum) + " check: " + str(self.calculate_checksum()) + " pass: " + str(self.verify_checksum())
        )

        return representation


# A class to digest a serial stream and decode PingMessages
class PingParser(object):
    # pre-declare instance variables for faster access and reduced memory overhead 
    __slots__ = (
        "buf",
        "state",
        "payload_length",
        "message_id",
        "errors",
        "parsed",
        "rx_msg",
    )

    NEW_MESSAGE       = 0    # Just got a complete checksum-verified message
    WAIT_START        = 1    # Waiting for the first character of a message 'B'
    WAIT_HEADER       = 2    # Waiting for the second character in the two-character sequence 'BR'
    WAIT_LENGTH_L     = 3    # Waiting for the low byte of the payload length field
    WAIT_LENGTH_H     = 4    # Waiting for the high byte of the payload length field
    WAIT_MSG_ID_L     = 5    # Waiting for the low byte of the payload id field
    WAIT_MSG_ID_H     = 6    # Waiting for the high byte of the payload id field
    WAIT_SRC_ID       = 7    # Waiting for the source device id
    WAIT_DST_ID       = 8    # Waiting for the destination device id
    WAIT_PAYLOAD      = 9    # Waiting for the last byte of the payload to come in
    WAIT_CHECKSUM_L   = 10   # Waiting for the checksum low byte
    WAIT_CHECKSUM_H   = 11   # Waiting for the checksum high byte
    ERROR             = 12   # Checksum didn't check out

    def __init__(self):
        self.buf = bytearray()
        self.state = self.WAIT_START
        self.payload_length = 0 # remaining for the message currently being parsed
        self.message_id = 0     # of the message currently being parsed
        self.errors = 0
        self.parsed = 0
        self.rx_msg = None      # most recently parsed message

    def wait_start(self, msg_byte):
        self.buf = bytearray()
        if msg_byte == ord('B'):
            self.buf.append(msg_byte)
            self.state += 1

    def wait_header(self, msg_byte):
        if msg_byte == ord('R'):
            self.buf.append(msg_byte)
            self.state += 1
        else:
            self.state = self.WAIT_START

    def wait_length_l(self, msg_byte):
        self.payload_length = msg_byte
        self.buf.append(msg_byte)
        self.state += 1

    def wait_length_h(self, msg_byte):
        self.payload_length |= (msg_byte << 8)
        self.buf.append(msg_byte)
        self.state += 1

    def wait_msg_id_l(self, msg_byte):
        self.message_id = msg_byte
        self.buf.append(msg_byte)
        self.state += 1

    def wait_msg_id_h(self, msg_byte):
        self.message_id |= (msg_byte << 8)
        self.buf.append(msg_byte)
        self.state += 1

    def wait_src_id(self, msg_byte):
        self.buf.append(msg_byte)
        self.state += 1

    def wait_dst_id(self, msg_byte):
        self.buf.append(msg_byte)
        self.state += 1
        if self.payload_length == 0: # no payload bytes -> skip waiting
            self.state += 1

    def wait_payload(self, msg_byte):
        self.buf.append(msg_byte)
        self.payload_length -= 1
        if self.payload_length == 0: # no payload bytes remaining -> stop waiting:
            self.state += 1

    def wait_checksum_l(self, msg_byte):
        self.buf.append(msg_byte)
        self.state += 1

    def wait_checksum_h(self, msg_byte):
        self.state = self.WAIT_START
        self.payload_length = 0
        self.message_id = 0

        self.buf.append(msg_byte)
        self.rx_msg = PingMessage(msg_data=self.buf)

        if self.rx_msg.verify_checksum():
            self.parsed += 1
            return self.NEW_MESSAGE
        else:
            self.errors += 1
            return self.ERROR

        return self.state

    def parse_byte(self, msg_byte):
        """ Returns the current parse state after feeding the parser a single byte.

        'msg_byte' is the byte to parse.
            If it completes a valid message, returns PingParser.NEW_MESSAGE.
            The decoded PingMessage will be available in the self.rx_msg attribute
                until a new message is decoded.

        """
        # Apply the relevant parsing method for the current state.
        #  (offset by 1 because NEW_MESSAGE isn't processed - start at WAIT_START)
        result = self._PARSE_BYTE[self.state - 1](self, msg_byte)

        return self.state if result is None else result

    # Tuple of parsing methods, in order of parser state
    #  at bottom because otherwise methods won't be defined
    _PARSE_BYTE = (
        wait_start,
        wait_header,
        wait_length_l,
        wait_length_h,
        wait_msg_id_l,
        wait_msg_id_h,
        wait_src_id,
        wait_dst_id,
        wait_payload,
        wait_checksum_l,
        wait_checksum_h,
    )


if __name__ == "__main__":
    # Hand-written data buffers for testing and verification
    test_protocol_version_buf = bytearray([
        0x42,
        0x52,
        4,
        0,
        definitions.COMMON_PROTOCOL_VERSION,
        0,
        77,
        211,
        1,
        2,
        3,
        99,
        0x26,
        0x02])

    test_profile_buf = bytearray([
        0x42, # 'B'
        0x52, # 'R'
        0x24, # 36_L payload length
        0x00, # 36_H
        0x14, # 1300_L message id
        0x05, # 1300_H
        56,
        45,
        0xe8, # 1000_L distance
        0x03, # 1000_H
        0x00, # 1000_H
        0x00, # 1000_H
        93,   # 93_L confidence
        0x00, # 93_H
        0x3f, # 2111_L transmit duration
        0x08, # 2111_H
        0x1c, # 44444444_L ping number
        0x2b, # 44444444_H
        0xa6, # 44444444_H
        0x02, # 44444444_H
        0xa0, # 4000_L scan start
        0x0f, # 4000_H
        0x00, # 4000_H
        0x00, # 4000_H
        0xb8, # 35000_L scan length
        0x88, # 35000_H
        0x00, # 35000_H
        0x00, # 35000_H
        0x04, # 4_L gain setting
        0x00, # 4_H
        0x00, # 4_H
        0x00, # 4_H
        10,   # 10_L profile data length
        0x00, # 10_H
        0,1,2,3,4,5,6,7,8,9, # profile data
        0xde, # 1502_H checksum
        0x05  # 1502_L
        ])

    p = PingParser()

    result = None
    # A text message
    print("\n---Testing protocol_version---\n")
    for byte in test_protocol_version_buf:
        result = p.parse_byte(byte)

    if result == p.NEW_MESSAGE:
        print(p.rx_msg)
    else:
        print("fail:", result)
        exit(1)

    # A dynamic vector message
    print("\n---Testing profile---\n")
    for byte in test_profile_buf:
        result = p.parse_byte(byte)

    if result == p.NEW_MESSAGE:
        print(p.rx_msg)
    else:
        print("fail:", result)
        exit(1)
