""" Channel property types
"""
from ctypes import c_char_p, c_short, c_ushort, c_ulong, c_float, c_uint, c_int, POINTER as P

PropertyTypes = dict(
    Type=c_ulong,
    Mode=c_ulong,
    Minval=c_float,
    Maxval=c_float,
    Unit=c_ushort,
    Exp=c_short,
    Decimal=c_ushort,
    # Onstate=P(c_char),  #c_char_p,
    # Offstate=P(c_char),  #c_char_p,
    Enum=P(c_char_p))

# PropertyTypesDecoder:Dict = {Onstate: lambda a: }

ParameterTypes = [
    c_float,  # PARAM_TYPE_NUMERIC
    c_uint,  # PARAM_TYPE_ONOFF (0, 1)
    c_uint,  # PARAM_TYPE_CHSTATUS -> bitmask
    c_uint,  # PARAM_TYPE_BDSTATUS -> bitmask
    c_int,  # PARAM_TYPE_BINARY
    c_char_p,  # PARAM_TYPE_STRING
    c_ushort,  # PARAM_TYPE_ENUM
]

ParameterPythonTypes = [float, int, int, int, int, str, list]

ParameterProperties = [
    {
        'Minval': c_float,
        'Maxval': c_float,
        'Unit': c_ushort,
        'Exp': c_short
    },
    {
        # 'Onstate': c_char_p,
        # 'Offstate': c_char_p
    },
    {},
    {},
    {},
    {
        'Minval': c_float,
        'Maxval': c_float,
        'Enum': P(c_char_p)
    }
]

UnitLongValues = [
    '', 'Ampere', 'Volt', 'Watt', 'Celsius', 'Hertz', 'Bar', 'VPS', 'Second',
    'RPM', 'Count'
]
UnitShortValues = ['', 'A', 'V', 'W', 'C', 'Hz', 'b', 'VPS', 's', 'RPM', '']
ExpLongValues = {-6: 'micro', -3: 'mili', 0: '', 3: 'Kilo', 6: 'M'}
ExpShortValues = {-6: 'μ', -3: 'm', 0: '', 3: 'k', 6: 'M'}
Modes = ['R', 'W', 'R/W']
