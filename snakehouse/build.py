from Cython.Build import cythonize


def build(extensions, *args, **kwargs):
    for multibuild in extensions:
        multibuild.generate()
    return cythonize([ext.for_cythonize() for ext in extensions], *args, **kwargs)
