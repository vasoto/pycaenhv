from ctypes import CDLL
from .utils import find_dll

def load_lib():
    """ Find and load CAENHVWrapper Library
    """
    lib_path = find_dll()
    if lib_path is None:
        raise ValueError('Cannot find CAENHVWrapper in known library paths or LD_LIBRARY_PATH')
    return CDLL(str(lib_path))