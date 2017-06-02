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

)

gen_reset = Message(
    102,
    ''
)
gen_device_id
gen_new_data
gen_cmd_request
gen_voltage

#Sonar Messages
sonar_velocity = Message(
    999,
    "sonar_velocity",
    "<I",
    ("dev_c_water",),
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
