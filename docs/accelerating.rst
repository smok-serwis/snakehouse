Accelerating builds
===================

distutils by default compiles using a single process.
To enable faster, multiprocess compilations just use:

.. code-block:: python

    from snakehouse import monkey_patch_parallel_compilation

    monkey_patch_parallel_compilation()

In your :code:`setup.py` before your call to :code:`setup()`.

It is also used in example_ so you can just copy that.

.. _example: https://github.com/smok-serwis/snakehouse/blob/develop/example/setup.py
