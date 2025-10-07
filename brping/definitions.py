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
PING1D_SET_OSS_PROFILE_CONFIGURATION = 1007
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
PING1D_OSS_PROFILE_CONFIGURATION = 1301
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

    PING1D_SET_OSS_PROFILE_CONFIGURATION: {
        "name": "set_oss_profile_configuration",
        "format": "HBB",
        "field_names": (
             "number_of_points",
             "normalization_enabled",
             "enhance_enabled",
            ),
        "payload_length": 4
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

    PING1D_OSS_PROFILE_CONFIGURATION: {
        "name": "oss_profile_configuration",
        "format": "HBB",
        "field_names": (
             "number_of_points",
             "normalization_enabled",
             "enhance_enabled",
            ),
        "payload_length": 4
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

PING360_SET_DEVICE_ID = 2000
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
    PING360_SET_DEVICE_ID: {
        "name": "set_device_id",
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

SURVEYOR240_SET_NET_INFO = 17
SURVEYOR240_SET_PING_PARAMETERS = 3023
SURVEYOR240_UTC_RESPONSE = 15
SURVEYOR240_UTC_REQUEST = 14
SURVEYOR240_JSON_WRAPPER = 10
SURVEYOR240_ATOF_POINT_DATA = 3012
SURVEYOR240_ATTITUDE_REPORT = 504
SURVEYOR240_WATER_STATS = 118
SURVEYOR240_YZ_POINT_DATA = 3011

# variable length fields are formatted with 's', and always occur at the end of the payload
# the format string for these messages is adjusted at runtime, and 's' inserted appropriately at runtime
# see PingMessage.get_payload_format()
payload_dict_surveyor240 = {
    SURVEYOR240_SET_NET_INFO: {
        "name": "set_net_info",
        "format": "III",
        "field_names": (
             "ntp_ip_address",
             "subnet_mask",
             "gateway_ip",
            ),
        "payload_length": 12
    },

    SURVEYOR240_SET_PING_PARAMETERS: {
        "name": "set_ping_parameters",
        "format": "iifhhHBBBBBBiHHf",
        "field_names": (
             "start_mm",
             "end_mm",
             "sos_mps",
             "gain_index",
             "msec_per_ping",
             "deprecated",
             "diagnostic_injected_signal",
             "ping_enable",
             "enable_channel_data",
             "reserved_for_raw_data",
             "enable_yz_point_data",
             "enable_atof_data",
             "target_ping_hz",
             "n_range_steps",
             "reserved",
             "pulse_len_steps",
            ),
        "payload_length": 36
    },

    SURVEYOR240_UTC_RESPONSE: {
        "name": "utc_response",
        "format": "QI",
        "field_names": (
             "utc_msec",
             "accuracy_msec",
            ),
        "payload_length": 12
    },

    SURVEYOR240_UTC_REQUEST: {
        "name": "utc_request",
        "format": "",
        "field_names": (
            ),
        "payload_length": 0
    },

    SURVEYOR240_JSON_WRAPPER: {
        "name": "JSON_WRAPPER",
        "format": "",
        "field_names": (
             "string",
            ),
        "payload_length": 0
    },

    SURVEYOR240_ATOF_POINT_DATA: {
        "name": "atof_point_data",
        "format": "IQffIIfIHH",
        "field_names": (
             "pwr_up_msec",
             "utc_msec",
             "listening_sec",
             "sos_mps",
             "ping_number",
             "ping_hz",
             "pulse_sec",
             "flags",
             "num_points",
             "reserved",
             "atof_point_data",
            ),
        "payload_length": 40
    },

    SURVEYOR240_ATTITUDE_REPORT: {
        "name": "attitude_report",
        "format": "ffffffQI",
        "field_names": (
             "up_vec_x",
             "up_vec_y",
             "up_vec_z",
             "reserved_1",
             "reserved_2",
             "reserved_3",
             "utc_msec",
             "pwr_up_msec",
            ),
        "payload_length": 36
    },

    SURVEYOR240_WATER_STATS: {
        "name": "water_stats",
        "format": "ff",
        "field_names": (
             "temperature",
             "pressure",
            ),
        "payload_length": 8
    },

    SURVEYOR240_YZ_POINT_DATA: {
        "name": "yz_point_data",
        "format": "IIfffffffIIIIIIIIIIfffffHH",
        "field_names": (
             "timestamp_msec",
             "ping_number",
             "sos_mps",
             "up_vec_x",
             "up_vec_y",
             "up_vec_z",
             "mag_vec_x",
             "mag_vec_y",
             "mag_vec_z",
             "reserved_0",
             "reserved_1",
             "reserved_2",
             "reserved_3",
             "reserved_4",
             "reserved_5",
             "reserved_6",
             "reserved_7",
             "reserved_8",
             "reserved_9",
             "water_degC",
             "water_bar",
             "heave_m",
             "start_m",
             "end_m",
             "unused",
             "num_points",
             "yz_point_data",
            ),
        "payload_length": 100
    },

}

S500_JSON_WRAPPER = 10
S500_SET_PING_PARAMS = 1015
S500_SET_SPEED_OF_SOUND = 1002
S500_ALTITUDE = 1211
S500_DISTANCE2 = 1223
S500_FW_VERSION = 1200
S500_GAIN_INDEX = 1207
S500_PING_RATE_MSEC = 1206
S500_PROCESSOR_DEGC = 1213
S500_PROFILE6_T = 1308
S500_RANGE = 1204
S500_SPEED_OF_SOUND = 1203

# variable length fields are formatted with 's', and always occur at the end of the payload
# the format string for these messages is adjusted at runtime, and 's' inserted appropriately at runtime
# see PingMessage.get_payload_format()
payload_dict_s500 = {
    S500_JSON_WRAPPER: {
        "name": "JSON_WRAPPER",
        "format": "",
        "field_names": (
             "string",
            ),
        "payload_length": 0
    },

    S500_SET_PING_PARAMS: {
        "name": "set_ping_params",
        "format": "IIhhHHHBB",
        "field_names": (
             "start_mm",
             "length_mm",
             "gain_index",
             "msec_per_ping",
             "pulse_len_usec",
             "report_id",
             "reserved",
             "chirp",
             "decimation",
            ),
        "payload_length": 20
    },

    S500_SET_SPEED_OF_SOUND: {
        "name": "set_speed_of_sound",
        "format": "I",
        "field_names": (
             "sos_mm_per_sec",
            ),
        "payload_length": 4
    },

    S500_ALTITUDE: {
        "name": "altitude",
        "format": "IB",
        "field_names": (
             "altitude_mm",
             "quality",
            ),
        "payload_length": 5
    },

    S500_DISTANCE2: {
        "name": "distance2",
        "format": "IIHBBI",
        "field_names": (
             "ping_distance_mm",
             "averaged_distance_mm",
             "reserved",
             "ping_confidence",
             "average_distance_confidence",
             "timestamp",
            ),
        "payload_length": 16
    },

    S500_FW_VERSION: {
        "name": "fw_version",
        "format": "BBHH",
        "field_names": (
             "device_type",
             "device_model",
             "version_major",
             "version_minor",
            ),
        "payload_length": 6
    },

    S500_GAIN_INDEX: {
        "name": "gain_index",
        "format": "I",
        "field_names": (
             "gain_index",
            ),
        "payload_length": 4
    },

    S500_PING_RATE_MSEC: {
        "name": "ping_rate_msec",
        "format": "H",
        "field_names": (
             "msec_per_ping",
            ),
        "payload_length": 2
    },

    S500_PROCESSOR_DEGC: {
        "name": "processor_degC",
        "format": "I",
        "field_names": (
             "centi_degC",
            ),
        "payload_length": 4
    },

    S500_PROFILE6_T: {
        "name": "profile6_t",
        "format": "IIIIIIIIfffffffBBBBH",
        "field_names": (
             "ping_number",
             "start_mm",
             "length_mm",
             "start_ping_hz",
             "end_ping_hz",
             "adc_sample_hz",
             "timestamp_msec",
             "spare2",
             "pulse_duration_sec",
             "analog_gain",
             "max_pwr_db",
             "min_pwr_db",
             "this_ping_depth_m",
             "smooth_depth_m",
             "fspare2",
             "ping_depth_measurement_confidence",
             "gain_index",
             "decimation",
             "smoothed_depth_measurement_confidence",
             "num_results",
             "pwr_results",
            ),
        "payload_length": 66
    },

    S500_RANGE: {
        "name": "range",
        "format": "II",
        "field_names": (
             "start_mm",
             "length_mm",
            ),
        "payload_length": 8
    },

    S500_SPEED_OF_SOUND: {
        "name": "speed_of_sound",
        "format": "I",
        "field_names": (
             "sos_mm_per_sec",
            ),
        "payload_length": 4
    },

}

OMNISCAN450_JSON_WRAPPER = 10
OMNISCAN450_SET_SPEED_OF_SOUND = 1002
OMNISCAN450_OS_PING_PARAMS = 2197
OMNISCAN450_OS_MONO_PROFILE = 2198

# variable length fields are formatted with 's', and always occur at the end of the payload
# the format string for these messages is adjusted at runtime, and 's' inserted appropriately at runtime
# see PingMessage.get_payload_format()
payload_dict_omniscan450 = {
    OMNISCAN450_JSON_WRAPPER: {
        "name": "JSON_WRAPPER",
        "format": "",
        "field_names": (
             "string",
            ),
        "payload_length": 0
    },

    OMNISCAN450_SET_SPEED_OF_SOUND: {
        "name": "set_speed_of_sound",
        "format": "I",
        "field_names": (
             "speed_of_sound",
            ),
        "payload_length": 4
    },

    OMNISCAN450_OS_PING_PARAMS: {
        "name": "os_ping_params",
        "format": "IIIffffhHBBBB",
        "field_names": (
             "start_mm",
             "length_mm",
             "msec_per_ping",
             "reserved_1",
             "reserved_2",
             "pulse_len_percent",
             "filter_duration_percent",
             "gain_index",
             "num_results",
             "enable",
             "reserved_3",
             "reserved_4",
             "reserved_5",
            ),
        "payload_length": 36
    },

    OMNISCAN450_OS_MONO_PROFILE: {
        "name": "os_mono_profile",
        "format": "IIIIIHHHBBffffff",
        "field_names": (
             "ping_number",
             "start_mm",
             "length_mm",
             "timestamp_ms",
             "ping_hz",
             "gain_index",
             "num_results",
             "sos_dmps",
             "channel_number",
             "reserved",
             "pulse_duration_sec",
             "analog_gain",
             "max_pwr_db",
             "min_pwr_db",
             "transducer_heading_deg",
             "vehicle_heading_deg",
             "pwr_results",
            ),
        "payload_length": 52
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
payload_dict_all.update(payload_dict_surveyor240)
payload_dict_all.update(payload_dict_s500)
payload_dict_all.update(payload_dict_omniscan450)
