cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

% for cdef_section in cdef_sections:
cdef extern from "${cdef_section.h_file_name}":
    object PyInit_${cdef_section.module_name}()
% endfor

cdef object get_definition_by_name(str name):
% for i, getdef_section in enumerate(get_definition_sections):
% if i == 0:
    if name == "${getdef_section.module_name}":
        return PyInit_${getdef_section.pyinit_name}()
% else:
    elif name == "${getdef_section.module_name}":
        return PyInit_${getdef_section.pyinit_name}()
% endif
% endfor

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
    modules_set = ${module_set}
    sys.meta_path.append(CythonPackageMetaPathFinder(modules_set))
