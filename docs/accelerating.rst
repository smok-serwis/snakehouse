Accelerating builds
===================

distutils by default compiles using a single process. To enable faster, multiprocess compilations
just type:

.. code-block:: python

    from snakehouse import monkey_patch_parallel_compilation

    monkey_patch_parallel_compilation()

Before your :code:`setup()` call.

