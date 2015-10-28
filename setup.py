import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "environmentmodules",
    version = "0.0.1",
    author = "Ben Albrecht",
    author_email = "benalbrecht@pitt.edu",
    description = "Python API for Environment Modules",
    license = "Apache2.0",
    keywords = "environment modules",
    url = "https://github.com/ben-albrecht/environmentmodules",
    packages=['environmentmodules'],
    long_description=read('README'),
)
