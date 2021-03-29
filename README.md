snakehouse
==========
[![Build status](https://circleci.com/gh/smok-serwis/snakehouse.svg?style=shield)](https://github.com/smok-serwis/snakehouse)
[![Code Climate](https://codeclimate.com/github/smok-serwis/snakehouse/badges/gpa.svg)](https://codeclimate.com/github/smok-serwis/snakehouse)
[![Issue Count](https://codeclimate.com/github/smok-serwis/snakehouse/badges/issue_count.svg)](https://codeclimate.com/github/smok-serwis/snakehouse)
[![PyPI](https://img.shields.io/pypi/pyversions/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)
[![PyPI version](https://badge.fury.io/py/snakehouse.svg)](https://badge.fury.io/py/snakehouse)
[![PyPI](https://img.shields.io/pypi/implementation/snakehouse.svg)](https://pypi.python.org/pypi/snakehouse)
[![PyPI](https://img.shields.io/pypi/wheel/snakehouse.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()
[![Documentation Status](https://readthedocs.org/projects/snakehouse/badge/?version=latest)](http://snakehouse.readthedocs.io/en/latest/?badge=latest)

snakehouse is a tool to pack mutiple .pyx files
into a single extension.

_There's a **MANDATORY READING** part at the end of this README. Read it or you will be sure to run into trouble._

Inspired by [this StackOverflow discussion](https://stackoverflow.com/questions/30157363/collapse-multiple-submodules-to-one-cython-extension).

Tested and works on CPython 3.5-3.9, 
both Windows and [Linux](https://travis-ci.org/github/smok-serwis/snakehouse).
It doesn't work on PyPy.

Contributions most welcome! If you contribute, feel free to attach
a change to [CONTRIBUTORS.md](/CONTRIBUTORS.md) as 
a part of your pull request as well!
Note what have you changed in
[CHANGELOG.md](/CHANGELOG.md) as well!

Usage notes - MANDATORY READING
-------------------------------
