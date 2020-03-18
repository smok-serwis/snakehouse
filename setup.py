from setuptools import setup, find_packages

from snakehouse import __version__

setup(keywords=['cython', 'extension', 'multiple', 'pyx'],
      packages=find_packages(include=['snakehouse']),
      version=__version__,
      install_requires=[
            'Cython', 'mako'
      ],
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      package_data={
            'snakehouse': ['*.template']
      },
      package_dir={'snakehouse': 'snakehouse'},
      )
