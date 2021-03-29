Helper functions
================

Snakehouse contains a bunch of functions to help you with everyday work. They are
meant to be primarily used in your :code:`setup.py`.

Finding files
~~~~~~~~~~~~~

Instead of manually specifying list of pyx and c files to compile you can use the following
functions:

.. autofunction:: snakehouse.find_pyx

.. autofunction:: snakehouse.find_c

.. autofunction:: snakehouse.find_pyx_and_c

Specifying requirements
~~~~~~~~~~~~~~~~~~~~~~~

If you add a MANIFEST.in file with contents:

.. code-block::

    include requirements.txt

Then you can write the following in your setup.py:

.. code-block:: python

    from snakehouse import read_requirements_txt

    setup(install_requires=read_requirements_txt())

.. autofunction:: snakehouse.read_requirements_txt

