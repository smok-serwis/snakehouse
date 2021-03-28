import typing as tp
from satella.coding import for_argument
from satella.files import read_lines, find_files


@for_argument(returns=list)
def find_pyx(directory_path: str) -> tp.List[str]:
    """
    Return all .pyx files found in given directory.

    :param directory_path: directory to look through
    :return: .pyx files found
    """
    return find_files(directory_path, '(.*)\\.pyx$', scan_subdirectories=True)


@for_argument(returns=list)
def find_c(directory_path: str) -> tp.List[str]:
    """
    Return all .c files found in given directory.

    :param directory_path: directory to look through
    :return: .c files found
    """
    return find_files(directory_path, '(.*)\\.c$', scan_subdirectories=True)


def find_pyx_and_c(directory_path: str) -> tp.List[str]:
    """
    Return a list of all .pyx and .c files found in given directory.

    :param directory_path:
    :return: list of all .pyx and .c files found in given directory
    """
    files = find_pyx(directory_path)
    files.extend(find_c(directory_path))
    return files


def read_requirements_txt(path: str = 'requirements.txt'):
    """
    Read requirements.txt and parse it into a list of packages
    as given by setup(install_required=).

    This means it will read in all lines, discard empty and commented ones,
    and discard all those who are an URL.

    Remember to include your requirements.txt inside your MANIFEST.in!

    :param path: path to requirements.txt. Default is `requirements.txt`.
    :return: list of packages ready to be fed to setup(install_requires=)
    """
    lines = read_lines(path)
    lines = (line.strip() for line in lines)
    lines = (line for line in lines if not line.startswith('#'))
    lines = (line for line in lines if not line.startswith('git+'))
    lines = (line for line in lines if not line.startswith('http'))
    lines = (line for line in lines if line)
    return list(lines)
