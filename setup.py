#!/usr/bin/env python3

from setuptools import setup, find_packages

long_description = """
Python library for the Ping sonar. Ping is the simple,
affordable, and compact ultrasonic altimeter for any aquatic project.

This library exposes all functionality of the device, such as getting profiles,
controlling parameters, switching modes, or just simply reading in the distance measurement."""

setup(name='bluerobotics-ping',
      version='0.0.7',
      description='A python module for the Blue Robotics Ping1D echosounder',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Blue Robotics',
      author_email='support@bluerobotics.com',
      url='https://www.bluerobotics.com',
      packages=find_packages(), install_requires=['pyserial', 'future'],
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      scripts=[
          "examples/simplePingExample.py",
          "tools/pingproxy.py",
          "tools/ping1d-simulation.py"]
      )
