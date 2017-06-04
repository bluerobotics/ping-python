#Messages.py

class Message:
    def __init__(self, id, name, format = None, payload_fields=(), action = None):
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

gen_goto_bootloader = Message(
    100,
    'gen_version'
)

gen_version = Message(
    101,
    'gen_version',
    '<BBHH',
    ('device_type', 'device_model', 'fw_version_major', 'fw_version_minor')
)

#TODO add a reset action here
gen_reset = Message(
    102,
    'gen_reset'
)

gen_device_id = Message(
    110,
    'gen_device_id',
    '<B',
    ('device_id',)
)

gen_new_data = Message(
    112,
    'gen_new_data',
    '<B',
    ('is_new_data',)
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
    ('voltage',)
)

#Sonar Messages
sonar_velocity = Message(
    999,
    'sonar_velocity',
    '<I',
    ('c_water',)
)

#EchoSounder Messages
es_distance_simple = Message(
    1100,
    'es_distance_simple',
    '<IB',
    ('distance','confidence')
)

es_distance = Message(
    1101,
    'es_distance',
    '<IBH4I',
    (
        'distance',
        'confidence',
        'pulse_usec',
        'ping_number',
        'start_mm',
        'length_mm',
        'gain_index'
    )
)

es_profile = Message(
    1102,
    'es_profile',
    '<IBH4IH200B',
    (
        'distance',
        'confidence',
        'pulse_usec',
        'ping_number',
        'start_mm',
        'length_mm',
        'gain_index',
        'num_points',
        'points'
    )
)

es_range = Message(
    1110,
    'es_range',
    '<II',
    ('start_mm','length_mm')
)

es_mode = Message(
    1111,
    'es_mode',
    '<B',
    ('auto_manual',)
)

es_rate = Message(
    1112,
    'es_rage',
    '<H',
    ('msec_per_ping',)
)

es_gain = Message(
    1113,
    'es_gain',
    '<I',
    ('gain_index',)
)

es_pulse = Message(
    1114,
    'es_pulse',
    '<H',
    ('pulse_usec',)
)
