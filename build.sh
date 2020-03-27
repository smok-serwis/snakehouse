#!/bin/bash

set -x
set -e

if [ $TRAVIS_BRANCH == "master" ]; then
    pip install wheel twine
    python setup.py bdist bdist_wheel
    twine upload -u $PYPI_USER -p $PYPI_PWD dist/*
fi
