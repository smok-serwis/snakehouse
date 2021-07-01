import os

from setuptools import setup

from snakehouse import Multibuild, build, monkey_patch_parallel_compilation, find_pyx_and_c, \
    find_all
from setuptools import Extension

monkey_patch_parallel_compilation()

dont_snakehouse = False
if 'DEBUG' in os.environ:
    print('Debug is enabled!')
    dont_snakehouse = True


# note that you can include standard Extension classes in this list, those won't be touched
# and will be directed directly to Cython.Build.cythonize()
cython_multibuilds = [
        # note that Windows-style pathes are supported on Linux build environment,
        # the reverse not necessarily being true (issue #5)
    Multibuild('example_module', find_all('example_module', True),
               define_macros=[("CYTHON_TRACE_NOGIL", "1")],
               dont_snakehouse=dont_snakehouse),
    Extension('example2.example', ['example2/example.pyx']),
    Multibuild('example3.example3.example3', ['example3/example3/example3/test.pyx'],
               dont_snakehouse=dont_snakehouse)
]

# first argument is used directly by snakehouse, the rest and **kwargs are passed to
# Cython.Build.cythonize()
ext_modules = build(cython_multibuilds,
                    compiler_directives={
                       'language_level': '3',
                    })

setup(name='example_module',
      version='0.1',
      packages=['example_module', 'example2'],
      install_requires=[
            'Cython', 'snakehouse'
      ],
      zip_safe=False,
      tests_require=[
          "nose2"
      ],
      test_suite='nose2.collector.collector',
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      ext_modules=ext_modules
)

