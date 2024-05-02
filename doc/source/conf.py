import os
import sys

project = 'ping-python'
copyright = '2024, Blue Robotics'
author = 'Blue Robotics'

sys.path.insert(0, os.path.abspath('../..'))  # Source code dir relative to this file

extensions = [
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    'sphinx.ext.autosummary',  # Create neat summary tables
    'sphinx_rtd_theme',
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary

html_theme = 'sphinx_rtd_theme'

templates_path = ['_templates']

html_logo = '../ping.png'
