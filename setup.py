#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='ping-python',
      version='0.0.1-dev',
      description='A python module for the Blue Robotics Ping1D echosounder',
      author='Blue Robotics',
      url='https://www.bluerobotics.com',
      packages=find_packages(), install_requires=['pyserial']
      )
