# ping-python

<a href="https://bluerobotics.com">
<img src="https://avatars2.githubusercontent.com/u/7120633?v=3&s=200" align="left" hspace="10" vspace="6">
</a>

[![Travis Build Status](https://travis-ci.org/bluerobotics/ping-python.svg?branch=master)](https://travis-ci.org/bluerobotics/ping-python)
[![Gitter](https://img.shields.io/badge/gitter-online-green.svg)](https://gitter.im/bluerobotics/discussion/)
[![PyPI version](https://badge.fury.io/py/bluerobotics-ping.svg)](https://badge.fury.io/py/bluerobotics-ping)

Python library for the Ping sonar. Ping is the simple, affordable, and compact ultrasonic altimeter for any aquatic project.

This library exposes all functionality of the device, such as getting profiles, controlling parameters, switching modes, or just simply reading in the distance measurement.

[Available here](https://www.bluerobotics.com/store/sensors-sonars-cameras/sonar/ping-sonar-r2-rp/)

<br/>
<br/>

## Resources

* [API Reference](https://docs.bluerobotics.com/ping-python/)
* [Device Specifications](https://www.bluerobotics.com/store/sensors-sonars-cameras/sonar/ping-sonar-r2-rp/#tab-technical-details)
* [Communication Protocol](https://github.com/bluerobotics/ping-protocol)
* [Support](https://gitter.im/bluerobotics/discussion)
* [License](https://github.com/bluerobotics/ping-python/blob/master/LICENSE)


## Installing

### pip

```sh
$ pip install --user bluerobotics-ping --upgrade
```

### From source

```sh
$ git clone --single-branch --branch deployment https://github.com/bluerobotics/ping-python.git
$ cd ping-python
$ python setup.py install --user
```

The library is ready to use: `import brping`. If you would like to use the command line [examples](/examples) or [tools](/tools) provided by this package, follow the notes in python's [installing to user site](https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site) directions (eg `export PATH=$PATH:~/.local/bin`).

## Quick Start

The `bluerobotics-ping` package installs a `simplePingExample.py` script to get started. Place your device's file descriptor (eg. `/dev/ttyUSB0`, `COM1`) after the --device option.

`$ simplePingExample.py --device <your-device>`

It's also possible to connect via UDP server using the `--udp` option with IP:PORT as input (e.g `192.168.2.2:9090`).

## Usage

The [Ping1D](https://docs.bluerobotics.com/ping-python/classPing_1_1Ping1D_1_1Ping1D.html) class provides an easy interface to configure a Ping device and retrieve data.

A Ping1D object must be initialized with the serial device path and the baudrate.

```py
from brping import Ping1D
myPing = Ping1D()
myPing.connect_serial("/dev/ttyUSB0", 115200)
# For UDP
# myPing.connect_udp("192.168.2.2", 9090)
```

Call initialize() to establish communications with the device.

```py
if myPing.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)
```

Use [`get_<message_name>`](https://github.com/bluerobotics/ping-protocol#get) to request data from the device. The data is returned as a dictionary with keys matching the names of the message payload fields. The messages you may request are documented in the [ping-protocol](https://github.com/bluerobotics/ping-protocol).

```py
    data = myPing.get_distance()
    if data:
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Failed to get distance data")
```

Use the [`set_*`](https://github.com/bluerobotics/ping-protocol#set) messages (eg. [set_speed_of_sound()](https://docs.bluerobotics.com/ping-python/classPing_1_1Ping1D_1_1Ping1D.html#a79a3931e5564644187198ad2063e5ed9)) to change settings on the Ping device.

```py
    # set the speed of sound to use for distance calculations to
    # 1450000 mm/s (1450 m/s)
    myPing.set_speed_of_sound(1450000)
```

See the [doxygen](https://docs.bluerobotics.com/ping-python/) documentation for complete API documentation.
