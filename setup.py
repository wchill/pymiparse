#!/usr/bin/env python

# Borrowed this file from urllib3, with changes as needed.

from setuptools import setup

import os
import re
import codecs

base_path = os.path.dirname(__file__)

# Get the version (borrowed from SQLAlchemy)
with open(os.path.join(base_path, 'pymiparse', '__init__.py')) as fp:
    VERSION = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(fp.read()).group(1)

with codecs.open('README.rst', encoding='utf-8') as fp:
    readme = fp.read()
with codecs.open('CHANGES.rst', encoding='utf-8') as fp:
    changes = fp.read()
version = VERSION


###################################################################

setup(
    name='pymiparse',
    version=version,
    description="Python parser for MediaInfo text logs.",
    long_description=u'\n\n'.join([readme, changes]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='mediainfo parser parsing audio video',
    author='Eric Ahn',
    author_email='ericahn3@illinois.edu',
    url='https://github.com/wchill/pymiparse',
    license='MIT',
    packages=[
        'pymiparse',
    ],
    requires=[],
)
