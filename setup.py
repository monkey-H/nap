#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os
import re
import sys

from setuptools import find_packages
from setuptools import setup

def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

install_requires = [
    'docker-py >= 1.5.0, < 2'
]

setup(
    name = 'just4happy',
    version = find_version('orchestration', '__init__.py'),
    description = 'new version of nap-core',
    url = 'github.com/icsnju/nap-core',
    author = 'nap-Ying & nap-Yuan',
    packages = find_packages(),
    include_package_data = True,
    install_requires = install_requires,
)
