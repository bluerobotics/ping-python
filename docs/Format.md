##Data Format

|    Byte     |   Type   |    Name    |                      Value                      |
|-------------|----------|------------|-------------------------------------------------|
| 0           | uint8_t  | startByte1 | "B"                                             |
| 1           | uint8_t  | startByte2 | "R"                                             |
| 2-3         | uint16_t | length     | Length of message body (not including checksum) |
| 4-5         | uint16_t | messageID  | Message identifier                              |
| 6-n         |          | data       | data packet                                     |
| (n+1)-(n+2) | uint16_t | checksum   | CRC16                                           |


##Message Definitions

###Altitude

Message ID: 0x01

| Byte |   Type   |    Name    |           Value           |
|------|----------|------------|---------------------------|
| 5    | uint8_t  | confidence | Percent confidence, 0-100 |
| 6-9  | uint32_t | altitude   | Measured altitude, in mm  |


###Profile

Message ID: 0x02

|        Byte         |   Type   |    Name    |                  Value                   |
|---------------------|----------|------------|------------------------------------------|
| 5                   | uint8_t  | confidence | Percent confidence, 0-100                |
| 6-9                 | uint32_t | altitude   | Measured altitude, in mm                 |
| 10-13               | uint32_t | startAlt   | Upper altitude range of returned profile |
| 14-17               | uint32_t | endAlt     | Low altitude range of returned profile   |
| 18-19               | uint16_t | gain       | Analog gain value                        |
| 20                  | uint8_t  | pulse      | Pulse length in µs from 0-255            |
| 21-22               | uint16_t | numPoints  | Number of data points returned           |
| 23-(23+numPoints-1) | uint8_t  | data       | Echo data array                          |


###Status

Message ID: 0x03

| Byte |   Type   |      Name      |             Value             |
|------|----------|----------------|-------------------------------|
| 5-6  | uint16_t | fwVersionMajor | Major firmware version number |
| 7-8  | uint16_t | fwVersionMinor | Minor firmware version number |
| 9-10 | uint16_t | voltage        | Supply voltage in millivolts  |
| 11   | uint8_t  | error          | Error code bitmask            |
