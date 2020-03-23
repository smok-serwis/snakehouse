import typing as tp
from Cython.Build import cythonize
from setuptools import Extension
from .multibuild import Multibuild


def build(extensions: tp.List[tp.Union[Multibuild, Extension]], *args, **kwargs):
    returns = []
    for multi_build in extensions:
        if isinstance(multi_build, Extension):
            returns.append(multi_build)
        else:
            multi_build.generate()
            returns.append(multi_build.for_cythonize())
    return cythonize(returns, *args, **kwargs)
