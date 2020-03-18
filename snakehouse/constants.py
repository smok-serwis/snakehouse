import logging
import typing as tp

logger = logging.getLogger(__name__)

BOOTSTRAP_PYX_HEADER = """
cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

"""

BOOTSTRAP_PYX_PACKAGE_LOADER = """
import sys        

cdef class CythonPackageLoader:
    cdef PyModuleDef* definition
    cdef object def_o
    cdef str name

    def __init__(self, name):
        self.def_o = get_definition_by_name(name)
        self.definition = <PyModuleDef*>self.def_o
        self.name = name
        Py_INCREF(self.def_o)

    def load_module(self, fullname):
        raise ImportError

    def create_module(self, spec):
        if spec.name != self.name:
            raise ImportError()
        return PyModule_FromDefAndSpec(self.definition, spec)

    def exec_module(self, module):
        PyModule_ExecDef(module, self.definition)


class CythonPackageMetaPathFinder:
    def __init__(self, modules_set):
        self.modules_set = modules_set

    def find_module(self, fullname, path):
        if fullname not in self.modules_set:
            return None
        return CythonPackageLoader(fullname)

    def invalidate_caches(self):
        pass
        
def bootstrap_cython_submodules():
    modules_set = %s
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
    
"""

INIT_PY_CONTENTS = """
from %s.__bootstrap__ import bootstrap_cython_submodules
bootstrap_cython_submodules()
"""

BOOTSTRAP_PYX_CDEF = """
cdef extern from "%s":
    object PyInit_%s()    
'"""

BOOTSTRAP_PYX_GET_DEFINITION_HEADER = """
cdef object get_definition_by_name(str name):
"""

BOOTSTRAP_PYX_GET_DEFINITION_IF = """   if name == %s:
        return %s
"""

BOOTSTRAP_PYX_GET_DEFINITION_ELIF = """    elif name == %s:
        return %s
"""

INCLUDE_PYTHON_H = '#include "Python.h"\n'

INCLUDE_PYINIT = 'PyObject* PyInit_%s();'

