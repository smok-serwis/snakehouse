import os
import collections
import pkg_resources
from mako.template import Template
from setuptools import Extension
from .constants import BOOTSTRAP_PYX_GET_DEFINITION_IF, \
    BOOTSTRAP_PYX_GET_DEFINITION_ELIF, INCLUDE_PYTHON_H, INCLUDE_PYINIT


CdefSection = collections.namedtuple('CdefSection', ('h_file_name', 'module_name'))
GetDefinitionSection = collections.namedtuple('GetDefinitionSection', (
    'module_name', 'pyinit_name'
))

class Multibuild:
    """
    This specifies a single Cython extension, called {extension_name}.__bootstrap__
    """
    def __init__(self, extension_name: str, files):
        """
        :param extension_name: the module name
        :param files: list of pyx and c files
        """
        self.files = list([file for file in files if not file.endswith('__bootstrap__.pyx')])
        file_name_set = set(os.path.split(file)[1] for file in self.files)
        if len(self.files) != len(file_name_set):
            raise ValueError('Two modules with the same name cannot appear together in a single '
                             'Multibuild')

        self.pyx_files = [file for file in files if file.endswith('.pyx')]

        self.extension_name = extension_name
        self.bootstrap_directory = os.path.commonpath(self.files)
        self.modules = set()    # tp.Set[tp.Tuple[str, str]]

    def generate_header_files(self):
        for filename in self.pyx_files:
            path, name = os.path.split(filename)
            if not name.endswith('.pyx'):
                continue

            module_name = name.replace('.pyx', '')
            h_name = name.replace('.pyx', '.h')
            exported_line = INCLUDE_PYINIT % (module_name,)

            if os.path.exists(h_name):
                with open(os.path.join(path, h_name), 'r') as f_in:
                    data = f_in.read()

                if INCLUDE_PYTHON_H not in data:
                    data = INCLUDE_PYTHON_H+data

                if exported_line not in data:
                    data = data+'\n'+exported_line+'\n'
            else:
                data = INCLUDE_PYTHON_H+'\n'+exported_line+'\n'

            with open(os.path.join(path, h_name), 'w') as f_out:
                f_out.write(data)

    def generate_bootstrap(self) -> str:
        bootstrap_contents = pkg_resources.resource_string('snakehouse', 'bootstrap.template').decode('utf8')
        cdef_section = []
        for filename in self.pyx_files:
            path, name = os.path.split(filename)
            if path.startswith(self.bootstrap_directory):
                path = path[len(self.bootstrap_directory):]
            module_name = name.replace('.pyx', '')
            if path:
                h_path_name = os.path.join(path[1:], name.replace('.pyx', '.h')).\
                    replace('\\', '\\\\')
            else:
                h_path_name = name.replace('.pyx', '.h')
            cdef_template = pkg_resources.resource_string('snakehouse', 'cdef.template').decode('utf8')
            cdef_section.append(CdefSection(h_path_name, module_name))

            if path:
                complete_module_name = self.extension_name+'.'+'.'.join(path[1:].split(
                    os.path.sep))+'.'+module_name
            else:
                complete_module_name = self.extension_name + '.'+module_name

            self.modules.add((complete_module_name, module_name, ))

        get_definition = []
        modules = iter(self.modules)
        mod_name, init_fun_name = next(modules)
        get_definition.append(BOOTSTRAP_PYX_GET_DEFINITION_IF % (repr(mod_name), init_fun_name))
        for mod_name, init_fun_name in modules:
            get_definition.append(GetDefinitionSection(mod_name, init_fun_name))

        return Template(bootstrap_contents).render(cdef_sections=cdef_section,
                                                   get_definition_sections=get_definition,
                                                   module_set=repr(set(x[0] for x in self.modules)))

    def write_bootstrap_file(self):
        with open(os.path.join(self.bootstrap_directory, '__bootstrap__.pyx'), 'w') as f_out:
            f_out.write(self.generate_bootstrap())

    def alter_init(self):
        pyinit_contents = pkg_resources.resource_string('snakehouse', 'initpy.template').decode('utf8')

        if os.path.exists(os.path.join(self.bootstrap_directory, '__init__.py')):
            with open(os.path.join(self.bootstrap_directory, '__init__.py'), 'r') as f_in:
                data = f_in.read()
        else:
            data = ''

        if 'bootstrap_cython_submodules' not in data:
            data = pyinit_contents.format(module_name=self.extension_name) + data

        with open(os.path.join(self.bootstrap_directory, '__init__.py'), 'w') as f_out:
            f_out.write(data)

    def generate(self):
        self.generate_header_files()
        self.write_bootstrap_file()
        self.alter_init()

    def for_cythonize(self, *args, **kwargs):
        return Extension(self.extension_name+".__bootstrap__",
                         self.files + [os.path.join(self.bootstrap_directory,
                                                    '__bootstrap__.pyx')],
                         *args,
                         **kwargs)
