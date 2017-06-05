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
k    'gen_reset',
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

#Message Dictionary
es_distance_simple
es_distance
es_profile
es_range
es_mode
es_rate
es_gain
es_pulse
