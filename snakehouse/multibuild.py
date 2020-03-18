import logging
import typing as tp
import os

from setuptools import Extension

logger = logging.getLogger(__name__)

SEP_LEN = len(os.path.sep)

class Multibuild:
    def __init__(self, extension_name: str, files: tp.Iterable[str]):
        self.files = list([file for file in files if not file.endswith('__bootstrap__.pyx')])
        file_name_set = set(os.path.split(file)[1] for file in self.files)
        if len(self.files) != len(file_name_set):
            raise ValueError('Two modules with the same name cannot appear together in a single '
                             'Multibuild')

        self.extension_name = extension_name
        self.bootstrap_directory = os.path.commonpath(self.files)
        self.modules = set()    # tp.Set[tp.Tuple[str, str]]

    def generate_header_files(self):
        for filename in self.files:
            path, name = os.path.split(filename)
            if not name.endswith('.pyx'):
                continue

            module_name = name.replace('.pyx', '')

            h_name = name.replace('.pyx', '.h')
            exported_line = 'PyObject* PyInit_%s();' % (module_name,)

            if os.path.exists(h_name):
                with open(os.path.join(path, h_name), 'r') as f_in:
                    data = f_in.read()

                if '#include "Python.h"' not in data:
                    data = '#include "Python.h"\n'+data

                if exported_line not in data:
                    data = data+'\n'+exported_line+'\n'

                with open(os.path.join(path, h_name), 'w') as f_out:
                    f_out.write(data)
            else:
                with open(os.path.join(path, h_name), 'w') as f_out:
                    f_out.write('#include "Python.h"\n')
                    f_out.write('\n'+exported_line+'\n')

    def generate_bootstrap(self) -> str:
        bootstrap_contents = ["""
cdef extern from "Python.h":
    ctypedef struct PyModuleDef:
        const char* m_name;

    void Py_INCREF(object)
    object PyModule_FromDefAndSpec(PyModuleDef *definition, object spec)
    int PyModule_ExecDef(object module, PyModuleDef* definition)

"""]
        for filename in self.files:
            path, name = os.path.split(filename)
            if path.startswith(self.bootstrap_directory):
                path = path[len(self.bootstrap_directory):]
            module_name = name.replace('.pyx', '')
            if path:
                h_path_name = os.path.join(path[1:], name.replace('.pyx', '.h')).replace('\\', '\\\\')
            else:
                h_path_name = name.replace('.pyx', '.h')
            bootstrap_contents.append('cdef extern from "%s":\n' % (h_path_name, ))
            bootstrap_contents.append('    object PyInit_%s()\n\n' % (module_name, ))

            if path:
                complete_module_name = self.extension_name+'.'+'.'.join(path[1:].split(os.path.sep))+'.'+module_name
            else:
                complete_module_name = self.extension_name + '.'+module_name

            self.modules.add((complete_module_name, 'PyInit_%s()' % (module_name, )))

        bootstrap_contents.append('''cdef object get_definition_by_name(str name):\n''')
        modules = iter(self.modules)
        mod_name, init_fun_name = next(modules)
        bootstrap_contents.append('''    if name == %s:
        return %s
''' % (repr(mod_name), init_fun_name))
        for mod_name, init_fun_name in modules:
            bootstrap_contents.append('''    elif name == %s:
        return %s
''' % (repr(mod_name), init_fun_name))

        bootstrap_contents.append('\n')
        bootstrap_contents.append("""
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
    
""" % (repr(set(x[0] for x in self.modules)), ))

        return ''.join(bootstrap_contents)

    def write_bootstrap_file(self):
        with open(os.path.join(self.bootstrap_directory, '__bootstrap__.pyx'), 'w') as f_out:
            f_out.write(self.generate_bootstrap())

    def alter_init(self):
        if os.path.exists(os.path.join(self.bootstrap_directory, '__init__.py')):
            with open(os.path.join(self.bootstrap_directory, '__init__.py'), 'r') as f_in:
                data = f_in.read()
        else:
            data = ''

        if 'bootstrap_cython_submodules' not in data:
            data = ("""
from %s.__bootstrap__ import bootstrap_cython_submodules
bootstrap_cython_submodules()
""" % (self.extension_name, )) + data

        with open(os.path.join(self.bootstrap_directory, '__init__.py'), 'w') as f_out:
            f_out.write(data)

    def generate(self):
        self.generate_header_files()
        self.write_bootstrap_file()
        self.alter_init()

    def for_cythonize(self, *args, **kwargs):
        return Extension(self.extension_name+".__bootstrap__",
                         self.files + [os.path.join(self.bootstrap_directory, '__bootstrap__.pyx')],
                         *args,
                         **kwargs)
