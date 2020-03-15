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
      ext_modules=ext_modules
)

