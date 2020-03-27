from setuptools import setup

from snakehouse import Multibuild, build
from setuptools import Extension

# note that you can include standard Extension classes in this list, those won't be touched
# and will be directed directly to Cython.Build.cythonize()
cython_multibuilds = [
        # note that Windows-style pathes are supported on Linux build environment,
        # the reverse not necessarily being true (issue #2)
    Multibuild('example_module', ['example_module/test.pyx', 'example_module/test2.pyx',
                                  'example_module/test3/test3.pyx',
                                  'example_module/test_n.c']),
    Extension('example2.example', ['example2/example.pyx']),
    Multibuild('example3.example3.example3', ['example3/example3/example3/test.pyx'])
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

