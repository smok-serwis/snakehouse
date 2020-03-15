import logging
import typing as tp

logger = logging.getLogger(__name__)

from Cython import Build

old_cythonize = Build.cythonize


def build(extensions, *args, **kwargs):
    for multibuild in extensions:
        multibuild.generate()
    return old_cythonize([ext.for_cythonize() for ext in extensions], *args, **kwargs)

Build.cythonize = build
