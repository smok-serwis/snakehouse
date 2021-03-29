import hashlib
import os
import logging
import collections
import typing as tp
import warnings

import pkg_resources
from satella.files import split
from mako.template import Template
from setuptools import Extension


CdefSection = collections.namedtuple('CdefSection', ('h_file_name', 'module_name', 'coded_module_name'))
GetDefinitionSection = collections.namedtuple('GetDefinitionSection', (
    'module_name', 'pyinit_name', 'coded_module_name'
))

logger = logging.getLogger(__name__)


def load_mako_lines(template_name: str) -> tp.List[str]:
    return pkg_resources.resource_string('snakehouse', os.path.join('templates', template_name)).decode('utf8')


def cull_path(path):
    if not path:
        return path
    if path[0] == os.path.sep:
        if len(path) > 1:
            if path[1] == os.path.sep:
                return path[2:]
        return path[1:]
    else:
        return path


def render_mako(template_name: str, **kwargs) -> str:
    tpl = Template(pkg_resources.resource_string(
        'snakehouse', os.path.join('templates', template_name)).decode('utf8'))
    return tpl.render(**kwargs)


LINES_IN_HFILE = len(load_mako_lines('hfile.mako').split('\n'))


class Multibuild:
    """
    This specifies a single Cython extension, called {extension_name}.__bootstrap__

    All kwargs will be sent straight to Cython's Extension

    :param extension_name: the module name
    :param files: list of pyx and c files
    :param kwargs: extra arguments to be passed to Extension() object
    :param dont_snakehouse: snakehouse won't be enabled, each element will be built
      as a separate extension. It is for these cases when you're testing and something segfaults.
    """
    def __init__(self, extension_name: str, files: tp.Iterator[str],
                 dont_snakehouse: bool = False,
                 **kwargs):
        # sanitize path separators so that Linux-style paths are supported on Windows
        logger.warning('Building extension %s with files %s', extension_name, files)
        files = list(files)
        self.dont_snakehouse = dont_snakehouse
        self.kwargs = kwargs
        if files:
            files = [os.path.join(*split(file)) for file in files]
            self.files = list([file for file in files if not file.endswith('__bootstrap__.pyx')])
            self.pyx_files = [file for file in self.files if file.endswith('.pyx')]
            self.c_files = [file for file in self.files if file.endswith('.c') or file.endswith('.cpp')]
        else:
            self.pyx_files = []
            self.c_files = []

        self.do_generate = True
        if not self.pyx_files:
            warnings.warn('No pyx files, probably installing from a source archive, skipping '
                          'generating files', RuntimeWarning)
            self.do_generate = False
        else:
            self.extension_name = extension_name        # type: str
            if len(self.files) == 1:
                self.bootstrap_directory, _ = os.path.split(self.files[0])      # type: str
            else:
                self.bootstrap_directory = os.path.commonpath(self.files)       # type: str
            self.modules = []    # type: tp.List[tp.Tuple[str, str, str]]
            self.module_name_to_loader_function = {}
            for filename in self.pyx_files:
                with open(filename, 'rb') as f_in:
                    self.module_name_to_loader_function[filename] = hashlib.sha256(f_in.read()).hexdigest()

    def generate_header_files(self):
        for filename in self.pyx_files:
            path, name, cmod_name_path, module_name, coded_module_name, complete_module_name = self.transform_module_name(filename)
            if not name.endswith('.pyx'):
                continue

            h_file = filename.replace('.pyx', '.h')

            if os.path.exists(h_file):
                with open(h_file, 'r') as f_in:
                    data = f_in.readlines()

                linesep = 'cr' if '\r\n' in data[0] else 'lf'
                rendered_mako = render_mako('hfile.mako', initpy_name=coded_module_name) + \
                                '\r\n' if linesep == 'cr' else '\n'
                assert len(rendered_mako) > 0

                if any('#define SNAKEHOUSE_FILE' in line for line in data):
                    data = [rendered_mako, *data[LINES_IN_HFILE:]]
                else:
                    data = [rendered_mako, *data]
            else:
                rendered_mako = render_mako('hfile.mako', initpy_name=coded_module_name)
                assert len(rendered_mako) > 0
                data = rendered_mako

            with open(h_file, 'w') as f_out:
                f_out.write(''.join(data))

    def transform_module_name(self, filename):
        path, name = os.path.split(filename)
        module_name = name.replace('.pyx', '')
        if path.startswith(self.bootstrap_directory):
            cmod_name_path = path[len(self.bootstrap_directory):]
        else:
            cmod_name_path = path
        path = cull_path(path)
        cmod_name_path = cull_path(cmod_name_path)

        if path:
            intro = '.'.join((e for e in cmod_name_path.split(os.path.sep) if e))
            if not intro:
                complete_module_name = '%s.%s' % (self.extension_name, module_name)
            else:
                complete_module_name = '%s.%s.%s' % (self.extension_name,
                                                     intro,
                                                     module_name)
        else:
            complete_module_name = '%s.%s' % (self.extension_name, module_name)

        coded_module_name = self.module_name_to_loader_function[filename]
        return path, name, cmod_name_path, module_name, coded_module_name, complete_module_name

    def do_after_cython(self):
        if self.dont_snakehouse:
            return
        self.generate_header_files()
        for filename in self.pyx_files:
            path, name, cmod_name_path, module_name, coded_module_name, complete_module_name = self.transform_module_name(filename)
            to_replace = '__Pyx_PyMODINIT_FUNC PyInit_%s' % (module_name, )
            replace_with = '__Pyx_PyMODINIT_FUNC PyInit_%s' % (coded_module_name, )
            with open(filename.replace('.pyx', '.c'), 'r') as f_in:
                data_in = f_in.read()
                data = data_in.replace(to_replace, replace_with)
            with open(filename.replace('.pyx', '.c'), 'w') as f_out:
                f_out.write(data)

    def generate_bootstrap(self) -> str:

        cdef_section = []
        for filename in self.pyx_files:
            path, name, cmod_name_path, module_name, coded_module_name, complete_module_name = self.transform_module_name(filename)

            if os.path.exists(filename.replace('.pyx', '.c')):
                os.unlink(filename.replace('.pyx', '.c'))

            h_path_name = os.path.join(cmod_name_path, name.replace('.pyx', '.h')).replace('\\', '\\\\')

            cdef_section.append(CdefSection(h_path_name, module_name, coded_module_name))

            self.modules.append((complete_module_name, module_name, coded_module_name))

        get_definition = []
        for mod_name, init_fun_name, coded_module_name in self.modules:
            get_definition.append(GetDefinitionSection(mod_name, init_fun_name, coded_module_name))

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
        if not self.dont_snakehouse and self.do_generate:
            self.write_bootstrap_file()
            self.alter_init()

    def for_cythonize(self, *args, **kwargs):
        if self.dont_snakehouse:
            extensions = []
            len_to_sub = len(self.bootstrap_directory) + len(os.path.pathsep)
            for pyx_file in self.pyx_files:
                file_name = pyx_file[len_to_sub:-4].replace('\\', '.').replace('/', '.')
                ext = Extension(self.extension_name+'.'+file_name,
                                [pyx_file] + self.c_files, *args, **kwargs)
                extensions.append(ext)
            return extensions
        else:
            kwargs.update(self.kwargs)
            for_cythonize = [*self.files, os.path.join(self.bootstrap_directory, '__bootstrap__.pyx')]
            return [Extension(self.extension_name+".__bootstrap__",
                              for_cythonize,
                              *args,
                              **kwargs)]
