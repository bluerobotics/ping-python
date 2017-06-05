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
    ('dev_id')
)

gen_new_data = Message(
    112,
    'gen_new_data',
    '<B',
    ('dev_is_new_data')
)

gen_cmd_request
gen_voltage

#Sonar Messages
sonar_velocity = Message(
    999,
    'sonar_velocity',
    ''<I',
    ('dev_c_water',),
    None
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
