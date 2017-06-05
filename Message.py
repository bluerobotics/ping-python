#Messages.py

class Message:
    def __init__(self, id, name, format = None, payload_fields=(), action = None):
        self.id = id
        self.name = name
        self.format = format
        self.payload_fields = payload_fields

def foo_action(ping,msg):
    pass

#General Messages

##Example:
#message_name = Message(
#  id,
#  message_name,
#  struct_format_string,
#  ('field_1', 'field_2'),
#  None
#)

gen_bootloader = Message(
    100,
    'gen_version'
)

gen_version = Message(
    101,
    'gen_version',
    '<BBHH',
    ('dev_type', 'dev_model', 'dev_fw_version_major', 'dev_fw_version_minor')
)

#TODO add a reset action here
gen_reset = Message(
    102,
    'gen_reset',
    '<',
    (,)
)

gen_device_id = Message(
    110,
    'gen_device_id',
    '<B',
    ('dev_id',)
)

gen_new_data = Message(
    112,
    'gen_new_data',
    '<B',
    ('dev_is_new_data',)
)

gen_cmd_request = Message(
    120,
    'gen_cmd_request',
    '<H'
)

gen_voltage = Message(
    130,
    'gen_voltage',
    '<H',
    ('dev_voltage',)
)

#Sonar Messages
sonar_velocity = Message(
    999,
    'sonar_velocity',
    '<I',
    ('dev_c_water',)
)

#EchoSounder Messages
es_distance_simple = Message(
    1100,
    'es_distance_simple',
    '<IB',
    ('dev_distance','dev_confidence')
)

es_distance = Message(
    1101,
    es_distance,
    'IBH4I',
    (
        'dev_distance',
        'dev_confidence',
        'dev_pulse_usec',
        'dev_ping_number',
        'dev_start_mm',
        'dev_length_mm',
        'dev_gain_index'
    )
)

#TODO add storage of points
es_profile = Message(
    1102,
    'es_profile',
    '<IBH4IH200B',
    (
        'dev_distance',
        'dev_confidence',
        'dev_pulse_usec',
        'dev_ping_number',
        'dev_start_mm',
        'dev_length_mm',
        'dev_gain_index',
        'dev_num_points'
    )
)

es_range = Message(
    1110,
    'es_range',
    '<II',
    ('dev_start_mm','dev_length_mm')
)

es_mode = Message(
    1111,
    'es_mode',
    '<B',
    ('dev_auto_manual',)
)

es_rate = Message(
    1112,
    'es_rage',
    '<H',
    ('dev_msec_per_ping',)
)

es_gain = Message(
    1113,
    'es_gain',
    '<I',
    ('dev_gain_index',)
)

es_pulse = Message(
    1114,
    'es_pulse',
    '<H',
    ('dev_pulse_usec',)
)
