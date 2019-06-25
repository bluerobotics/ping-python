#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='bluerobotics-ping',
      version='0.0.8',
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
