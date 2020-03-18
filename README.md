snakehouse
==========
[![Build Status](https://travis-ci.org/smok-serwis/snakehouse.svg)](https://travis-ci.org/smok-serwis/snakehouse)
[![PyPI](https://img.shields.io/pypi/pyversions/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)
[![PyPI version](https://badge.fury.io/py/snakehouse.svg)](https://badge.fury.io/py/snakehouse)
[![PyPI](https://img.shields.io/pypi/implementation/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)

snakehouse is a tool to pack mutiple .pyx files
into a single extension.

Inspired by [this StackOverflow discussion](https://stackoverflow.com/questions/30157363/collapse-multiple-submodules-to-one-cython-extension).

Tested and works on Python 3.8 and Python 3.7, 
both Windows and Linux.

Usage
-----
Take a look at [example](example/) on how to multi-build your Cython extensions.

Limitations
-----------

* Two modules with the same name cannot be mentioned in a single Multibuild (issue #1).

