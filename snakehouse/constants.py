import logging
import typing as tp

logger = logging.getLogger(__name__)


BOOTSTRAP_PYX_GET_DEFINITION_IF = """
"""

BOOTSTRAP_PYX_GET_DEFINITION_ELIF = """    elif name == %s:
        return %s
"""

INCLUDE_PYTHON_H = '#include "Python.h"\n'

INCLUDE_PYINIT = 'PyObject* PyInit_%s(void);'

