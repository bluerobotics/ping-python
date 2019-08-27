#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

scriptPath = Path(__file__).parent.absolute()
generatorPath = "%s/../lib/ping-protocol/src" % scriptPath

import sys
sys.path.append(generatorPath)

from generator import Generator

parser = argparse.ArgumentParser(description="generate markdown documentation files for message definitions")
parser.add_argument('--output-directory', action="store", default="./", type=str, help="directory to save output files")
args = parser.parse_args()

if not os.path.exists(args.output_directory):
    os.makedirs(args.output_directory)

definitionPath = "%s/../lib/ping-protocol/src/definitions" % scriptPath
templatePath = "%s/templates" % scriptPath

templateFile = "%s/pingmessage-definitions.py.in" % templatePath

g = Generator()

definitions = [ "common",
                "ping1d",
                "ping360"]

struct_token = {"u8": "B",
                "u16": "H",
                "u32": "I",
                "i8": "b",
                "i16": "h",
                "i32": "i",
                "char": "s"}

f = open("%s/definitions.py" % args.output_directory, "w")

for definition in definitions:
    definitionFile = "%s/%s.json" % (definitionPath, definition)
    f.write(g.generate(definitionFile, templateFile, {"structToken": struct_token, "base": definition}))

#allString = "payload_dict_all = {}\n"
# add PINGMESSAGE_UNDEFINED for legacy request support
allString = '\
PINGMESSAGE_UNDEFINED = 0\n\
payload_dict_all = {\n\
    PINGMESSAGE_UNDEFINED: {\n\
        "name": "undefined",\n\
        "format": "",\n\
        "field_names": (),\n\
        "payload_length": 0\n\
    },\n\
}\n'

f.write(allString)

for definition in definitions:
    f.write("payload_dict_all.update(payload_dict_")
    f.write(definition)
    f.write(")\n")

f.close()

definitionFile = "%s/common.json" % definitionPath
templateFile = "%s/device.py.in" % templatePath
f = open("%s/device.py" % args.output_directory, "w")
f.write(g.generate(definitionFile, templateFile, {"structToken": struct_token}))
f.close()

definitionFile = "%s/ping1d.json" % definitionPath
templateFile = "%s/ping1d.py.in" % templatePath
f = open("%s/ping1d.py" % args.output_directory, "w")
f.write(g.generate(definitionFile, templateFile, {"structToken": struct_token}))
f.close()

definitionFile = "%s/ping360.json" % definitionPath
templateFile = "%s/ping360.py.in" % templatePath
f = open("%s/ping360.py" % args.output_directory, "w")
f.write(g.generate(definitionFile, templateFile, {"structToken": struct_token}))
f.close()
