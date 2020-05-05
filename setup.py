#!/usr/bin/env python3

from setuptools import setup, find_packages

long_description = """
Python library for the Blue Robotics ping-protocol, and devices that implement it.

This library provides message apis to use the protocol, as well as device apis to use with the
Blue Robotics Ping Echosounder and Ping360 scanning sonar.
"""

setup(name='bluerobotics-ping',
      version='0.1.0',
      python_requires='>=3.4',
      description='A python module for the Blue Robotics ping-protocol and products',
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
