import typing as tp
from Cython.Build import cythonize
from setuptools import Extension
from .multibuild import Multibuild

MultiBuildType = tp.Union[Multibuild, Exception]


def build(extensions: tp.List[MultiBuildType], *args, **kwargs):
    returns = []
    for multi_build in extensions:
        if isinstance(multi_build, Extension):
            returns.append(multi_build)
        elif isinstance(multi_build, Multibuild):
            multi_build.generate()
            returns.append(multi_build.for_cythonize())
        else:
            raise ValueError('Invalid value in list, expected either an instance of Multibuild '
                             'or an Extension')
    return cythonize(returns, *args, **kwargs)
