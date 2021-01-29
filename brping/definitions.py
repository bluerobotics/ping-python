COMMON_ACK = 1
COMMON_NACK = 2
COMMON_ASCII_TEXT = 3
COMMON_GENERAL_REQUEST = 6
COMMON_DEVICE_INFORMATION = 4
COMMON_PROTOCOL_VERSION = 5
COMMON_SET_DEVICE_ID = 100

# variable length fields are formatted with 's', and always occur at the end of the payload
# the format string for these messages is adjusted at runtime, and 's' inserted appropriately at runtime
# see PingMessage.get_payload_format()
payload_dict_common = {
    COMMON_ACK: {
        "name": "ack",
        "format": "H",
        "field_names": (
             "acked_id",
            ),
        "payload_length": 2
    },

    COMMON_NACK: {
        "name": "nack",
        "format": "H",
        "field_names": (
             "nacked_id",
             "nack_message",
            ),
        "payload_length": 2
    },

    COMMON_ASCII_TEXT: {
        "name": "ascii_text",
        "format": "",
        "field_names": (
             "ascii_message",
            ),
        "payload_length": 0
    },

    COMMON_GENERAL_REQUEST: {
        "name": "general_request",
        "format": "H",
        "field_names": (
             "requested_id",
            ),
        "payload_length": 2
    },

    COMMON_DEVICE_INFORMATION: {
        "name": "device_information",
        "format": "BBBBBB",
        "field_names": (
             "device_type",
             "device_revision",
             "firmware_version_major",
             "firmware_version_minor",
             "firmware_version_patch",
             "reserved",
            ),
        "payload_length": 6
    },

    COMMON_PROTOCOL_VERSION: {
        "name": "protocol_version",
        "format": "BBBB",
        "field_names": (
             "version_major",
             "version_minor",
             "version_patch",
             "reserved",
            ),
        "payload_length": 4
    },

    COMMON_SET_DEVICE_ID: {
        "name": "set_device_id",
        "format": "B",
        "field_names": (
             "device_id",
            ),
        "payload_length": 1
    },

}

PING1D_SET_DEVICE_ID = 1000
PING1D_SET_RANGE = 1001
PING1D_SET_SPEED_OF_SOUND = 1002
PING1D_SET_MODE_AUTO = 1003
PING1D_SET_PING_INTERVAL = 1004
PING1D_SET_GAIN_SETTING = 1005
PING1D_SET_PING_ENABLE = 1006
PING1D_FIRMWARE_VERSION = 1200
PING1D_DEVICE_ID = 1201
PING1D_VOLTAGE_5 = 1202
PING1D_SPEED_OF_SOUND = 1203
PING1D_RANGE = 1204
PING1D_MODE_AUTO = 1205
PING1D_PING_INTERVAL = 1206
PING1D_GAIN_SETTING = 1207
PING1D_TRANSMIT_DURATION = 1208
PING1D_GENERAL_INFO = 1210
PING1D_DISTANCE_SIMPLE = 1211
PING1D_DISTANCE = 1212
PING1D_PROCESSOR_TEMPERATURE = 1213
PING1D_PCB_TEMPERATURE = 1214
PING1D_PING_ENABLE = 1215
PING1D_PROFILE = 1300
PING1D_GOTO_BOOTLOADER = 1100
PING1D_CONTINUOUS_START = 1400
PING1D_CONTINUOUS_STOP = 1401

# variable length fields are formatted with 's', and always occur at the end of the payload
# the format string for these messages is adjusted at runtime, and 's' inserted appropriately at runtime
# see PingMessage.get_payload_format()
payload_dict_ping1d = {
    PING1D_SET_DEVICE_ID: {
        "name": "set_device_id",
        "format": "B",
        "field_names": (
             "device_id",
            ),
        "payload_length": 1
    },

    PING1D_SET_RANGE: {
        "name": "set_range",
        "format": "II",
        "field_names": (
             "scan_start",
             "scan_length",
            ),
        "payload_length": 8
    },

    PING1D_SET_SPEED_OF_SOUND: {
        "name": "set_speed_of_sound",
        "format": "I",
        "field_names": (
             "speed_of_sound",
            ),
        "payload_length": 4
    },

    PING1D_SET_MODE_AUTO: {
        "name": "set_mode_auto",
        "format": "B",
        "field_names": (
             "mode_auto",
            ),
        "payload_length": 1
    },

    PING1D_SET_PING_INTERVAL: {
        "name": "set_ping_interval",
        "format": "H",
        "field_names": (
             "ping_interval",
            ),
        "payload_length": 2
    },

    PING1D_SET_GAIN_SETTING: {
        "name": "set_gain_setting",
        "format": "B",
        "field_names": (
             "gain_setting",
            ),
        "payload_length": 1
    },

    PING1D_SET_PING_ENABLE: {
        "name": "set_ping_enable",
        "format": "B",
        "field_names": (
             "ping_enabled",
            ),
        "payload_length": 1
    },

    PING1D_FIRMWARE_VERSION: {
        "name": "firmware_version",
        "format": "BBHH",
        "field_names": (
             "device_type",
             "device_model",
             "firmware_version_major",
             "firmware_version_minor",
            ),
        "payload_length": 6
    },

    PING1D_DEVICE_ID: {
        "name": "device_id",
        "format": "B",
        "field_names": (
             "device_id",
            ),
        "payload_length": 1
    },

    PING1D_VOLTAGE_5: {
        "name": "voltage_5",
        "format": "H",
        "field_names": (
             "voltage_5",
            ),
        "payload_length": 2
    },

    PING1D_SPEED_OF_SOUND: {
        "name": "speed_of_sound",
        "format": "I",
        "field_names": (
             "speed_of_sound",
            ),
        "payload_length": 4
    },

    PING1D_RANGE: {
        "name": "range",
        "format": "II",
        "field_names": (
             "scan_start",
             "scan_length",
            ),
        "payload_length": 8
    },

    PING1D_MODE_AUTO: {
        "name": "mode_auto",
        "format": "B",
        "field_names": (
             "mode_auto",
            ),
        "payload_length": 1
    },

    PING1D_PING_INTERVAL: {
        "name": "ping_interval",
        "format": "H",
        "field_names": (
             "ping_interval",
            ),
        "payload_length": 2
    },

    PING1D_GAIN_SETTING: {
        "name": "gain_setting",
        "format": "I",
        "field_names": (
             "gain_setting",
            ),
        "payload_length": 4
    },

    PING1D_TRANSMIT_DURATION: {
        "name": "transmit_duration",
        "format": "H",
        "field_names": (
             "transmit_duration",
            ),
        "payload_length": 2
    },

    PING1D_GENERAL_INFO: {
        "name": "general_info",
        "format": "HHHHBB",
        "field_names": (
             "firmware_version_major",
             "firmware_version_minor",
             "voltage_5",
             "ping_interval",
             "gain_setting",
             "mode_auto",
            ),
        "payload_length": 10
    },

    PING1D_DISTANCE_SIMPLE: {
        "name": "distance_simple",
        "format": "IB",
        "field_names": (
             "distance",
             "confidence",
            ),
        "payload_length": 5
    },

    PING1D_DISTANCE: {
        "name": "distance",
        "format": "IHHIIII",
        "field_names": (
             "distance",
             "confidence",
             "transmit_duration",
             "ping_number",
             "scan_start",
             "scan_length",
             "gain_setting",
            ),
        "payload_length": 24
    },

    PING1D_PROCESSOR_TEMPERATURE: {
        "name": "processor_temperature",
        "format": "H",
        "field_names": (
             "processor_temperature",
            ),
        "payload_length": 2
    },

    PING1D_PCB_TEMPERATURE: {
        "name": "pcb_temperature",
        "format": "H",
        "field_names": (
             "pcb_temperature",
            ),
        "payload_length": 2
    },

    PING1D_PING_ENABLE: {
        "name": "ping_enable",
        "format": "B",
        "field_names": (
             "ping_enabled",
            ),
        "payload_length": 1
    },

    PING1D_PROFILE: {
        "name": "profile",
        "format": "IHHIIIIH",
        "field_names": (
             "distance",
             "confidence",
             "transmit_duration",
             "ping_number",
             "scan_start",
             "scan_length",
             "gain_setting",
             "profile_data_length",
             "profile_data",
            ),
        "payload_length": 26
    },

    PING1D_GOTO_BOOTLOADER: {
        "name": "goto_bootloader",
        "format": "",
        "field_names": (
            ),
        "payload_length": 0
    },

    PING1D_CONTINUOUS_START: {
        "name": "continuous_start",
        "format": "H",
        "field_names": (
             "id",
            ),
        "payload_length": 2
    },

    PING1D_CONTINUOUS_STOP: {
        "name": "continuous_stop",
        "format": "H",
        "field_names": (
             "id",
            ),
        "payload_length": 2
    },

}

PING360_DEVICE_ID = 2000
PING360_DEVICE_DATA = 2300
PING360_AUTO_DEVICE_DATA = 2301
PING360_RESET = 2600
PING360_TRANSDUCER = 2601
PING360_AUTO_TRANSMIT = 2602
PING360_MOTOR_OFF = 2903

# variable length fields are formatted with 's', and always occur at the end of the payload
# the format string for these messages is adjusted at runtime, and 's' inserted appropriately at runtime
# see PingMessage.get_payload_format()
payload_dict_ping360 = {
    PING360_DEVICE_ID: {
        "name": "device_id",
        "format": "BB",
        "field_names": (
             "id",
             "reserved",
            ),
        "payload_length": 2
    },

    PING360_DEVICE_DATA: {
        "name": "device_data",
        "format": "BBHHHHHH",
        "field_names": (
             "mode",
             "gain_setting",
             "angle",
             "transmit_duration",
             "sample_period",
             "transmit_frequency",
             "number_of_samples",
             "data_length",
             "data",
            ),
        "payload_length": 14
    },

    PING360_AUTO_DEVICE_DATA: {
        "name": "auto_device_data",
        "format": "BBHHHHHHBBHH",
        "field_names": (
             "mode",
             "gain_setting",
             "angle",
             "transmit_duration",
             "sample_period",
             "transmit_frequency",
             "start_angle",
             "stop_angle",
             "num_steps",
             "delay",
             "number_of_samples",
             "data_length",
             "data",
            ),
        "payload_length": 20
    },

    PING360_RESET: {
        "name": "reset",
        "format": "BB",
        "field_names": (
             "bootloader",
             "reserved",
            ),
        "payload_length": 2
    },

    PING360_TRANSDUCER: {
        "name": "transducer",
        "format": "BBHHHHHBB",
        "field_names": (
             "mode",
             "gain_setting",
             "angle",
             "transmit_duration",
             "sample_period",
             "transmit_frequency",
             "number_of_samples",
             "transmit",
             "reserved",
            ),
        "payload_length": 14
    },

    PING360_AUTO_TRANSMIT: {
        "name": "auto_transmit",
        "format": "BBHHHHHHBB",
        "field_names": (
             "mode",
             "gain_setting",
             "transmit_duration",
             "sample_period",
             "transmit_frequency",
             "number_of_samples",
             "start_angle",
             "stop_angle",
             "num_steps",
             "delay",
            ),
        "payload_length": 16
    },

    PING360_MOTOR_OFF: {
        "name": "motor_off",
        "format": "",
        "field_names": (
            ),
        "payload_length": 0
    },

}

PINGMESSAGE_UNDEFINED = 0
payload_dict_all = {
    PINGMESSAGE_UNDEFINED: {
        "name": "undefined",
        "format": "",
        "field_names": (),
        "payload_length": 0
    },
}
payload_dict_all.update(payload_dict_common)
payload_dict_all.update(payload_dict_ping1d)
payload_dict_all.update(payload_dict_ping360)
