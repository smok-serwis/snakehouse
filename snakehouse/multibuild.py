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


def render_mako(template_name: str, **kwargs) -> str:
    tpl = Template(pkg_resources.resource_string('snakehouse', template_name).decode('utf8'))
    return tpl.render(**kwargs)


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

            if os.path.exists(h_name):
                with open(os.path.join(path, h_name), 'r') as f_in:
                    data = f_in.read()

                if 'PyObject* PyInit_' not in data:
                    data = render_mako('hfile.mako', initpy_name=module_name) + data
            else:
                data = render_mako('hfile.mako', initpy_name=module_name)

            with open(os.path.join(path, h_name), 'w') as f_out:
                f_out.write(data)

    def generate_bootstrap(self) -> str:

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
            cdef_section.append(CdefSection(h_path_name, module_name))

            if path:
                complete_module_name = self.extension_name+'.'+'.'.join(path[1:].split(
                    os.path.sep))+'.'+module_name
            else:
                complete_module_name = self.extension_name + '.'+module_name

            self.modules.add((complete_module_name, module_name, ))

        get_definition = []
        for mod_name, init_fun_name in self.modules:
            get_definition.append(GetDefinitionSection(mod_name, init_fun_name))

        return render_mako('bootstrap.mako', cdef_sections=cdef_section,
                                             get_definition_sections=get_definition,
                                             module_set=repr(set(x[0] for x in self.modules)))

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
            data = render_mako('initpy.mako', module_name=self.extension_name) + data

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
