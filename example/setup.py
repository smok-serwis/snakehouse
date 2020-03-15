from Cython import Build
from setuptools import setup, find_packages

from cython_multibuild import Multibuild


cython_multibuilds = [
    Multibuild('example_module', ['example_module/test.pyx', 'example_module/test2.pyx',
                                  'example_module/test3/test3.pyx'])
]

ext_modules = Build.cythonize(cython_multibuilds,
                        compiler_directives={
                            'language_level': '3',
                        })

setup(name='example_module',
      version='0.1',
      packages=find_packages(include=['example_module']),
      install_requires=[
            'Cython'
      ],
      zip_safe=False,
      tests_require=[
          "nose2"
      ],
      test_suite='nose2.collector.collector',
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      ext_modules=ext_modules
)

