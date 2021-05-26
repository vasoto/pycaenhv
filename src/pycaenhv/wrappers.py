from ctypes import byref, c_int, c_short, c_ubyte, c_ushort, c_char_p, POINTER as P
from typing import List, NoReturn, Union, Any, Optional, Dict

from .errors import CAENHVError, check_function_output
from .enums import CAENHV_SYSTEM_TYPE, LinkType
from .utils import get_char_list, get_strlist_element
from .constants import MAX_PARAM_NAME, MAX_BOARD_DESC, MAX_BOARD_NAME
from .parameters import PropertyTypes, ParameterTypes
from .functions import CAENHVLibSwRel, CAENHV_GetBdParamInfo, CAENHV_InitSystem, CAENHV_DeinitSystem, CAENHV_GetChParamInfo, CAENHV_GetChParamProp, CAENHV_GetChParam, CAENHV_GetCrateMap


def software_release() -> str:
    """ Returns the software release of the library
    """
    return CAENHVLibSwRel().decode()


def init_system(system_type: Union[CAENHV_SYSTEM_TYPE, int],
                link_type: Union[LinkType, int],
                argument: Any,
                username: str = '',
                password: str = '') -> int:
    """ Initialize the system and returns the handle
    """
    _handle = c_int()
    _system = int(system_type)
    _link = int(link_type)
    _arg = argument
    if isinstance(_arg, str):
        _arg = _arg.encode()
    err = CAENHV_InitSystem(_system, _link, _arg, username.encode(),
                            password.encode(), byref(_handle))
    check_function_output(err)
    return _handle.value


def deinit_system(handle: int) -> NoReturn:
    """ Deinitialize system 
    """
    err = CAENHV_DeinitSystem(handle)
    check_function_output(err)


def get_board_parameters(handle: int, slot: int) -> Union[None, List[str]]:
    """ List all available board parameters
    """
    _slot = c_ushort(slot)  # apply the appropriate type
    raw_param_list = c_char_p()  # result will be stored here
    err = CAENHV_GetBdParamInfo(handle, _slot, byref(raw_param_list))
    check_function_output(err)
    result = get_char_list(raw_param_list, MAX_PARAM_NAME)
    return result


def get_channel_parameters(handle: int, slot: int, channel: int) -> List[str]:
    """ List all available board parameters
    """
    _slot = c_ushort(slot)
    _ch = c_ushort(channel)
    raw_char_list = c_char_p()
    _count = c_int()
    err = CAENHV_GetChParamInfo(handle, _slot, _ch, byref(raw_char_list),
                                byref(_count))
    count = _count.value
    result = [
        get_strlist_element(raw_char_list, i, MAX_PARAM_NAME)
        for i in range(count)
    ]
    return result


def get_channel_parameter_property(handle: int, slot: int, channel: int,
                                   param_name: str, prop_name: str) -> Any:
    """ Get channel parameter's property value
    """
    # Set appropriate types
    _slot = c_ushort(slot)
    _ch = c_ushort(channel)
    _param = c_char_p(param_name.encode())
    _prop = c_char_p(prop_name.encode())
    # Set the result type according to property name
    _res = PropertyTypes[prop_name]()
    err = CAENHV_GetChParamProp(handle, _slot, _ch, _param, _prop, byref(_res))
    check_function_output(err)
    return _res.value


def get_channel_parameter(
    handle: int,
    slot: int,
    channel: int,
    param_name: str,
    channel_list: Optional[List[str]] = None,
) -> Any:
    """ Get the value of a channel `channel` parameter `param_name`
    """
    # TODO: use channel list
    type_ = get_channel_parameter_property(handle, slot, channel, param_name,
                                           "Type")
    _res = ParameterTypes[type_]()
    _slot = c_ushort(slot)
    _ch = c_ushort(channel)
    _param = c_char_p(param_name.encode())
    _ch_list = P(ctypes.c_ushort)()
    err = CAENHV_GetChParam(handle, _slot, _param, _ch, _ch_list, byref(_res))
    check_function_output(err)
    return _res.value


def get_crate_map(handle: int) -> Dict[str, Any]:
    """ Get crate map
    """
    _slots = c_ushort()
    _channels = P(c_ushort)()
    _models = c_char_p()
    _descriptions = c_char_p()
    _serial_numbers = P(c_ushort)()
    _fw_min_rel = P(c_ubyte)()
    _fw_max_rel = P(c_ubyte)()

    err = CAENHV_GetCrateMap(handle, byref(_slots), byref(_channels),
                             byref(_models), byref(_descriptions),
                             byref(_serial_numbers), byref(_fw_min_rel),
                             byref(_fw_max_rel))
    check_function_output(err)
    slots = _slots.value
    channels = [_channels[i] for i in range(slots)]
    models = [
        get_strlist_element(_models, i, MAX_BOARD_NAME) for i in range(slots)
    ]
    descriptions = [
        get_strlist_element(_descriptions, i, MAX_BOARD_DESC)
        for i in range(slots)
    ]
    serial_numbers = [_serial_numbers[i] for i in range(slots)]
    firmware_releases = [(_fw_max_rel[i], _fw_min_rel[i])
                         for i in range(slots)]
    result = dict(slots=slots,
                  channels=channels,
                  models=models,
                  descriptions=descriptions,
                  serial_numbers=serial_numbers,
                  firmware_releases=firmware_releases)
    return result
