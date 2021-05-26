from ctypes import POINTER as P, c_char, c_char_p, cast
from typing import List

CharPtrList = c_char_p


def get_strlist_element(char_ptr_list: CharPtrList,
                        index: int,
                        max_val: int = 1) -> str:
    """ Get an element of a list of char*
    """
    return (cast(char_ptr_list, P(c_char * max_val)))[index].value.decode()


def get_char_list(charp_list: c_char_p, max_element_size: int) -> List[str]:
    """ Converts char** list to python list of strings, without knowing the size of the list.
    """
    result = []
    index = 0
    element = get_strlist_element(charp_list, index, max_element_size)
    # Loop until the element is None
    while element:
        result.append(element)
        index += 1
        element = get_strlist_element(charp_list, index, max_element_size)
    return result