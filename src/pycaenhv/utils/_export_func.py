from typing import Any, Optional, List
import os

PYCAENHV_NOLIB = os.environ.get('PYCAENHV_NOLIB', False)


def export_func(lib: Any,
                function_name: str,
                return_type: Any,
                arguments: Optional[List[Any]] = None,
                doc_str: str = None) -> Any:
    """ Export function from dll `lib`
    """
    if PYCAENHV_NOLIB and lib is None:
        # Allow running without libcaenhvwrapper.so being available on the system
        # i.e. testing or documentation generation
        return None
    func_ = getattr(lib, function_name)
    if arguments:
        func_.argtypes = arguments
    func_.restype = return_type
    if doc_str:
        func_.__doc__ = doc_str
    else:
        func_.__doc__ = function_name
    return func_
