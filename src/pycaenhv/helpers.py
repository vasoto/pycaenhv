from itertools import compress
from typing import Any, Dict, List

from pycaenhv.constants import ChannelStatusLabels

from . import parameters as par
from .wrappers import get_channel_parameter, get_channel_parameter_property, get_channel_parameters


def format_numeric(param_info: Dict[str, Any]) -> str:
    props = param_info['properties']
    value = param_info['value']
    mode = param_info['mode']
    exponent = par.ExpShortValues[props['Exp']]
    unit = par.UnitShortValues[props['Unit']]
    return f"{value} {exponent}{unit} ({props['Minval']}:{props['Maxval']}) [{mode}]"


def format_chstatus(param_info: Dict[str, Any]) -> str:
    pass


ParameterDecoder = {0: format_numeric}


def get_parameter_information(handle: int, slot: int, channel: int,
                              parameter: str) -> Dict[str, Any]:

    value = get_channel_parameter(handle=handle,
                                  slot=slot,
                                  channel=channel,
                                  param_name=parameter)
    param_type = get_channel_parameter_property(handle=handle,
                                                slot=slot,
                                                channel=channel,
                                                param_name=parameter,
                                                prop_name='Type')
    param_mode = get_channel_parameter_property(handle=handle,
                                                slot=slot,
                                                channel=channel,
                                                param_name=parameter,
                                                prop_name='Mode')

    mode = par.Modes[param_mode]
    # type_ = par.ParameterTypes[param_type]
    properties = dict()

    for prop_name, prop_type in par.ParameterProperties[param_type].items():
        r = get_channel_parameter_property(handle=handle,
                                           slot=slot,
                                           channel=channel,
                                           param_name=parameter,
                                           prop_name=prop_name)
        properties[prop_name] = r
    result = dict(value=value,
                  mode=mode,
                  type=param_type,
                  properties=properties)
    return result


def bitfield_int(n) -> List[int]:
    return [n >> i & 1 for i in range(n.bit_length() - 1, -1, -1)]


def bitfield(n) -> List[int]:
    return [1 if digit == '1' else 0
            for digit in bin(n)[2:]]  # [2:] to chop off the "0b" part


def status_unpack(status: int) -> List[str]:
    mask = bitfield(status)
    # Pad with 0s
    mask = [0] * (len(ChannelStatusLabels) - len(mask)) + mask
    return list(compress(reversed(ChannelStatusLabels), mask))


def normalize_channel_info(name, info: Dict[str, Any]) -> Dict[str, Any]:
    min_ = info['properties'].get('Minval', '')
    max_ = info['properties'].get('Maxval', '')
    value = info['value']
    if info['type'] == 1:
        min_ = False
        max_ = True
        value = bool(value)
    elif info['type'] == 2:
        value = status_unpack(value)
    unit_exp = par.ExpShortValues[info['properties'].get('Exp', 0)]
    unit = par.UnitShortValues[info['properties'].get('Unit', 0)]
    return dict(
        name=name,
        value=value,
        unit=f"{unit_exp}{unit}",
        min=min_,
        max=max_,
        mode=info['mode'],
    )


def channel_info(handle: int, slot: int, channel: int) -> List:
    """ Returns all information about a channel
    """
    parameters = get_channel_parameters(handle, slot, channel)
    result = []
    for param in parameters:
        param_info = get_parameter_information(handle, slot, channel, param)

        result.append(normalize_channel_info(param, param_info))
    return result


def check_channel_parameter(handle, slot, channel, parameter) -> bool:
    """ Check if parameter is supported by the channel
    """
    parameters = get_channel_parameters(handle, slot, channel)
    return parameter in parameters


def cast_parameter_value(handle, slot, channel, parameter, value) -> Any:
    """ Cast parameter value to the appropriate type
    """
    _type = get_channel_parameter_property(handle, slot, channel, parameter,
                                           'Type')
    return par.ParameterTypes[_type](par.ParameterPythonTypes[_type](value))


def check_channel_parameter_value(handle, slot, channel, parameter,
                                  value) -> bool:
    """
    """
    value_ = cast_parameter_value(handle, slot, channel, parameter,
                                  value).value
    type_ = get_channel_parameter_property(handle, slot, channel, parameter,
                                           'Type')
    if type_ == 0:
        min_value = get_channel_parameter_property(handle, slot, channel,
                                                   parameter, 'Minval')
        max_value = get_channel_parameter_property(handle, slot, channel,
                                                   parameter, 'Maxval')
        if (min_value > value_) or (max_value < value_):
            return False
    return True


def is_parameter_readonly(handle, slot, channel, parameter) -> bool:
    return get_channel_parameter_property(handle, slot, channel, parameter,
                                          'Mode') == 0
