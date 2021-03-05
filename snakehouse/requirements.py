from satella.files import read_lines


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
