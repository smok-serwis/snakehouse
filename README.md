cython-multibuild
=================
[![PyPI](https://img.shields.io/pypi/pyversions/cython-multibuild.svg)](https://pypi.python.org/pypi/cython-multibuild)
[![PyPI version](https://badge.fury.io/py/cython-multibuild.svg)](https://badge.fury.io/py/cython-multibuild)
[![PyPI](https://img.shields.io/pypi/implementation/cython-multibuild.svg)](https://pypi.python.org/pypi/cython-multibuild)

cython-multibuild is a tool to pack mutiple .pyx files
into a single extension.

Inspired by [https://stackoverflow.com/questions/30157363/collapse-multiple-submodules-to-one-cython-extension](this StackOverflow discussion).

This will monkey-patch Cython's Build.cythonize, so take care to import
Build instead of Cythonize itself.

Tested and works on Python 3.8 and Python 3.7.

Usage
-----
Take a look at [example](example/) on how to multi-build your Cython extensions.


Limitations
-----------

* Two modules with the same name cannot be mentioned in a single Multibuild
