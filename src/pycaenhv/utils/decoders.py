from ctypes import POINTER as P, c_char, c_char_p, cast, addressof
from typing import List

CharPtrList = c_char_p


def get_strlist_element(char_ptr_list: CharPtrList,
                        index: int,
                        max_val: int = 1) -> str:
    """ Get an element of a list of char*
    """
    return (cast(char_ptr_list, P(c_char * max_val)))[index].value.decode()


def iter_str_list(char_ptr_list, size: int) -> List[str]:
    i = 0
    j = 0
    result = []
    while (i < size):
        elem = bytearray()
        while (cast(char_ptr_list, P(c_char * 1)))[j].value != b'':
            elem.extend((cast(char_ptr_list, P(c_char * 1)))[j].value)
            j += 1
        j += 1
        i += 1
        result.append(elem.decode())
    return result


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