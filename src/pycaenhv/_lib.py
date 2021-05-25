from ctypes import CDLL
from .utils import find_dll

def load_lib():
    """ Find and load libcaenhvwrapper.so
    """
    lib_path = find_dll()
    if lib_path is None:
        raise ValueError('Cannot find libcaenhvwrapper.so in known library paths or LD_LIBRARY_PATH')
    return CDLL(str(lib_path))