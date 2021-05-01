from setuptools import setup, find_packages


setup(keywords=['cython', 'extension', 'multiple', 'pyx'],
      packages=find_packages(include=['snakehouse']),
      version='1.5a5',
      install_requires=[
            'Cython', 'mako', 'satella>=2.14.46',
      ],
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      package_data={
            'snakehouse': ['templates/*.mako']
      },
      package_dir={'snakehouse': 'snakehouse'},
      )
