Usage
=====

To use snakehouse just use the following in your :code:`setup.py`:

.. code-block:: python

    from snakehouse import Multibuild, build

    extensions = build([
                    Multibuild('example_module', list_of_pyx_files)
                    ], compiler_directives={
                       'language_level': '3',
                    })

    setup(name='example_module',
      version='0.1',
      packages=['example_module'],
      ext_modules=extensions
    )

You can pass also :code:`setuptools`'s :code:`Extensions` objects, as detailed in
example_.

.. _example: https://github.com/smok-serwis/snakehouse/blob/develop/example/setup.py

Full pydoc of :code:`Multibuild` and :code:`build` is here

.. autoclass:: snakehouse.Multibuild
    :members:

.. autofunction:: snakehouse.build

You should use :code:`dont_snakehouse` for debugging and unit tests, as
snakehouse has a sad tendency to dump core on unhandled exceptions. To prevent that
from happening remember to handle your exceptions and debug using this flag.

If you need to locate all .pyx files in a certain directory, you can do the following:

.. code-block:: python

    from snakehouse import Multibuild, build, find_all

    extensions = build([
                    Multibuild('example_module', find_all('src'))
                    ], compiler_directives={
                       'language_level': '3',
                    })

The documentation to :class:`~snakehouse.find_all` is as follows:

.. autoclass:: snakehouse.find_all
