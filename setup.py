#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='ping-python',
      version='0.0.1-dev',
      description='A python module for the Blue Robotics Ping1D echosounder',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Blue Robotics',
      url='https://www.bluerobotics.com',
      packages=find_packages(), install_requires=['pyserial']
      )
