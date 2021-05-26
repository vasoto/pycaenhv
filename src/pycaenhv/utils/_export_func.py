from typing import Any, Optional, List


def export_func(lib: Any,
                function_name: str,
                return_type: Any,
                arguments: Optional[List[Any]] = None,
                doc_str: str = None) -> Any:
    """ Export function from dll `lib`
    """
    func_ = getattr(lib, function_name)
    if arguments:
        func_.argtypes = arguments
    func_.restype = return_type
    if doc_str:
        func_.__doc__ = doc_str
    else:
        func_.__doc__ = function_name
    return func_
