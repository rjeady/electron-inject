#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except Exception:
        return "Not available"


setup(
    name="injectron",
    version="0.4",
    description="A wrapper for injecting javascript and css into electron apps",
    long_description=read("README.md"),
    url="https://github.com/rjeady/injectron-py/",
    author="Rob Eady",
    keywords=["electron", "inject", "injectron", "devtools", "developer tools"],
    license="GPLv3",
    packages=["injectron"],
    install_requires=["websocket-client","requests"],
    package_data={"injectron": ["*.js"]},
)
