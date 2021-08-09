from ctypes import CDLL
from .utils import find_dll, PYCAENHV_NOLIB


def load_lib():
    """ Find and load libcaenhvwrapper.so
    """
    lib_path = find_dll()
    if lib_path is None:
        if not PYCAENHV_NOLIB:
            raise ValueError(
                'Cannot find libcaenhvwrapper.so in known library paths or LD_LIBRARY_PATH'
            )
        else:
            return None
    return CDLL(str(lib_path))