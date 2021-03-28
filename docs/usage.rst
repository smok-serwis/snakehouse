Usage
=====

To use snakehouse just use the following in your :code:`setup.py`:

.. code-block:: python

    list_of_pyx_files = [ ... ]

    setup(name='example_module',
      version='0.1',
      packages=['example_module'],
      ext_modules=Multibuild('example_module', list_of_pyx_files)
    )

Full documentation of Multibuild is here

.. autoclass:: snakehouse.Multibuild
    :members:

You should use :code:`dont_snakehouse` for debugging and unit tests, as
snakehouse has a sad tendency to dump core on unhandled exceptions. To prevent that
from happening remember to handle your exceptions and debug using this flag.

Helper functions
----------------

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

