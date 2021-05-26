""" Channel property types
"""
from ctypes import c_char_p, c_short, c_ushort, c_ulong, c_float, c_bool, c_uint, c_int, POINTER as P

PropertyTypes = dict(Type=c_ulong,
                     Mode=c_ulong,
                     Minval=c_float,
                     Maxval=c_float,
                     Unit=c_ushort,
                     Exp=c_short,
                     Decimal=c_ushort,
                     Onstate=c_char_p,
                     Offstate=c_char_p,
                     Enum=P(c_char_p))

ParameterTypes = [
    c_float,  # PARAM_TYPE_NUMERIC
    c_bool,  # PARAM_TYPE_ONOFF (0, 1)
    c_uint,  # PARAM_TYPE_CHSTATUS -> bitmask
    c_uint,  # PARAM_TYPE_BDSTATUS -> bitmask
    c_int,  # PARAM_TYPE_BINARY
    c_char_p,  # PARAM_TYPE_STRING
    c_ushort,  # PARAM_TYPE_ENUM
]
