#!/usr/bin/python -u
#Messages.py

class Message:
    def __init__(self, id, name, format = '', payload_fields=(), action = None):
        self.id = id
        self.name = name
        self.format = format
        self.payload_fields = payload_fields
    def __repr__(self):
        representation = (
            'ID: ' + str(self.id) + '\n' +
            'Name: ' + str(self.name) + '\n' +
            'Format: ' + str(self.format) + '\n' +
            'Fields: ' + str(self.payload_fields) + '\n'
        )
        return representation

ping1D_empty = Message(
    0,
    'empty',
)

ping1D_undefined = Message(
    0,
    'undefined',
)

ping1D_ack = Message(
    1,
    'ack',
)

ping1D_nack = Message(
    2,
    'nack',
)

ping1D_ascii_text = Message(
    3,
    'ascii_text',
)

ping1D_set_device_id = Message(
    1000,
    'set_device_id',
    '<B',
    (
        'device_id',
    )
)

ping1D_set_range = Message(
    1001,
    'set_range',
    '<LL',
    (
        'start_mm',
        'length_mm',
    )
)

ping1D_set_speed_of_sound = Message(
    1002,
    'set_speed_of_sound',
    '<L',
    (
        'speed',
    )
)

ping1D_set_auto_manual = Message(
    1003,
    'set_auto_manual',
    '<B',
    (
        'mode',
    )
)

ping1D_set_ping_rate_msec = Message(
    1004,
    'set_ping_rate_msec',
    '<H',
    (
        'rate_msec',
    )
)

ping1D_set_gain_index = Message(
    1005,
    'set_gain_index',
    '<B',
    (
        'index',
    )
)

ping1D_set_ping_enable = Message(
    1006,
    'set_ping_enable',
    '<B',
    (
        'enable',
    )
)

ping1D_goto_bootloader = Message(
    1100,
    'goto_bootloader',
)

ping1D_fw_version = Message(
    1200,
    'fw_version',
    '<BBHH',
    (
        'device_type',
        'device_model',
        'fw_version_major',
        'fw_version_minor',
    )
)

ping1D_device_id = Message(
    1201,
    'device_id',
    '<B',
    (
        'device_id',
    )
)

ping1D_voltage_5 = Message(
    1202,
    'voltage_5',
    '<H',
    (
        'mvolts',
    )
)

ping1D_speed_of_sound = Message(
    1203,
    'speed_of_sound',
    '<L',
    (
        'speed_mmps',
    )
)

ping1D_range = Message(
    1204,
    'range',
    '<LL',
    (
        'start_mm',
        'length_mm',
    )
)

ping1D_mode = Message(
    1205,
    'mode',
    '<B',
    (
        'auto_manual',
    )
)

ping1D_ping_rate_msec = Message(
    1206,
    'ping_rate_msec',
    '<H',
    (
        'msec_per_ping',
    )
)

ping1D_gain_index = Message(
    1207,
    'gain_index',
    '<L',
    (
        'gain_index',
    )
)

ping1D_pulse_usec = Message(
    1208,
    'pulse_usec',
    '<H',
    (
        'pulse_usec',
    )
)

ping1D_background_data = Message(
    1209,
    'background_data',
    '<LHHLL',
    (
        'depth_mm',
        'milli_confidence',
        'gain_index',
        'range_mm',
        'rms_goertzel_noise',
    )
)

ping1D_general_info = Message(
    1210,
    'general_info',
    '<HHHHBB',
    (
        'vers_major',
        'vers_minor',
        'mvolts',
        'msec_per_ping',
        'gain_index',
        'is_auto',
    )
)

ping1D_distance_simple = Message(
    1211,
    'distance_simple',
    '<LB',
    (
        'distance',
        'confidence',
    )
)

ping1D_distance = Message(
    1212,
    'distance',
    '<LHHLLLL',
    (
        'distance',
        'confidence',
        'pulse_usec',
        'ping_number',
        'start_mm',
        'length_mm',
        'gain_index',
    )
)

ping1D_processor_temperature = Message(
    1213,
    'processor_temperature',
    '<H',
    (
        'temp',
    )
)

ping1D_pcb_temperature = Message(
    1214,
    'pcb_temperature',
    '<H',
    (
        'temp',
    )
)

ping1D_profile = Message(
    1300,
    'profile',
    '<LHHLLLLH200B',
    (
        'distance',
        'confidence',
        'pulse_usec',
        'ping_number',
        'start_mm',
        'length_mm',
        'gain_index',
        'num_points',
        'data',
    )
)

ping1D_full_profile = Message(
    1301,
    'full_profile',
    '<llbbhlHHlllllLhh200B',
    (
        'this_ping_depth_mm',
        'smoothed_depth_mm',
        'smoothed_depth_confidence_percent',
        'this_ping_confidence_percent',
        'ping_duration_usec',
        'ping_number',
        'supply_millivolts',
        'degC',
        'start_mm',
        'length_mm',
        'y0_mm',
        'yn_mm',
        'gain_index',
        'outlier_bits',
        'index_of_bottom_result',
        'num_results',
        'results',
    )
)

ping1D_raw_data = Message(
    1302,
    'raw_data',
    '<LLHHLLLLLLLLL',
    (
        'v_major',
        'v_minor',
        'supply_millivolts',
        'degC',
        'gain_index',
        'start_mm',
        'len_mm',
        'num_samples',
        'ping_usec',
        'ping_hz',
        'adc_sample_hz',
        'ping_num',
        'rms_goertzel_noise',
    )
)

ping1D_continuous_start = Message(
    1400,
    'continuous_start',
)

ping1D_continuous_stop = Message(
    1401,
    'continuous_stop',
)
