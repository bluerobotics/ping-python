# BlueRobotics-Ping

<a href="https://bluerobotics.com">
<img src="https://avatars2.githubusercontent.com/u/7120633?v=3&s=200" align="left" hspace="10" vspace="6">
</a>


Python library for the Ping sonar. Ping is the simple, affordable, and compact ultrasonic altimeter for any aquatic project.

This library exposes all functionality of the device, such as getting profiles, controlling parameters, switching modes, or just simply reading in the distance measurement.

[Available here](https://www.bluerobotics.com/store/electronics/lumen-light-r1/)

<br/>
<br/>


## Resources

* [API Reference](https://docs.bluerobotics.com/ping-python/)
* [Device Specifications](http://www.bluerobotics.com/)
* [Serial Protocol](https://github.com/bluerobotics/ping-protocol)
* [Support](http://docs.bluerobotics.com)
* [License](http://github.com/bluerobotics/ping-python/blob/master/LICENSE)


## Installing

* `git clone --recursive http://github.com/bluerobotics/ping-python.git`
* `cd ping-python`


## Quick Start

You can run a simple example that prints the distance reading repeatedly by executing the command below. Place your device's file descriptor after the --device option. For example, on Linux this will likely be /dev/ttyUSB0.

`python simplePingExample.py --device <your-device>`
