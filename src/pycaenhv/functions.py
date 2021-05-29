from ctypes import POINTER, c_char_p, c_int, c_ushort, c_ubyte, c_void_p

from ._lib import load_lib
from .errors import check_function_output
from .utils import export_func

P = POINTER
c_int_p = POINTER(c_int)

lib = load_lib()

# Software release
# CAENHVLIB_API char* CAENHVLibSwRel(void)
CAENHVLibSwRel = export_func(lib,
                             'CAENHVLibSwRel',
                             c_char_p,
                             doc_str="Get software version")

# Initialize
# CAENHVLIB_API CAENHVRESULT CAENHV_InitSystem(CAENHV_SYSTEM_TYPE_t system,
# 											 int LinkType,
# 											 void *Arg,
#                                              const char *UserName,
# 											 const char *Passwd,  int *handle);

CAENHV_InitSystem = export_func(
    lib, 'CAENHV_InitSystem', c_int,
    [c_int, c_int, c_void_p, c_char_p, c_char_p, c_int_p],
    'Initialize HV system')

# Deinitialize
# CAENHVLIB_API CAENHVRESULT  CAENHV_DeinitSystem(int handle);
CAENHV_DeinitSystem = export_func(lib, 'CAENHV_DeinitSystem', c_int, [c_int],
                                  'Deinitialize HV system')

# Board parameters Info
#     CAENHVLIB_API CAENHVRESULT  CAENHV_GetBdParamInfo(int handle,
#  ushort slot, char **ParNameList);
CAENHV_GetBdParamInfo = export_func(
    lib, 'CAENHV_GetBdParamInfo', c_int,
    [c_int, c_ushort, P(c_char_p)], "Get all available board parameters")

CAENHV_GetChParam = export_func(
    lib,
    'CAENHV_GetChParam',
    c_int,
    [
        c_int,  # handle
        c_ushort,  # slot,
        c_char_p,  # ParName
        c_ushort,  # ChNum
        P(c_ushort),  # ChList
        c_void_p  # ParValue
    ],
    "Get channel parameter's value")

CAENHV_GetChParamInfo = export_func(
    lib, 'CAENHV_GetChParamInfo', c_int,
    [c_int, c_ushort, c_ushort,
     P(c_char_p), P(c_int)], "Enumerate channel parameters")

CAENHV_GetChParamProp = export_func(
    lib, 'CAENHV_GetChParamProp', c_int,
    [c_int, c_ushort, c_ushort, c_char_p, c_char_p, c_void_p],
    "Get channel parameter's property")

# CAENHVLIB_API CAENHVRESULT CAENHV_GetCrateMap(int handle,
#  ushort *NrOfSlot, ushort **NrofChList, char **ModelList, char **DescriptionList,
#  ushort **SerNumList, uchar **FmwRelMinList, uchar **FmwRelMaxList);
CAENHV_GetCrateMap = export_func(
    lib,
    'CAENHV_GetCrateMap',
    c_int,
    [
        c_int,
        P(c_ushort),  # Number of slots
        P(P(c_ushort)),  # Number of channels list
        P(c_char_p),  # Model list
        P(c_char_p),  # Description list
        P(P(c_ushort)),  # Serial numbers list
        P(P(c_ubyte)),  # Firmware min rel list
        P(P(c_ubyte))  # Firmware max rel list
    ],
    "Get the crate map")

# CAENHVLIB_API CAENHVRESULT  CAENHV_SetChParam(int handle, ushort slot,
#  const char *ParName, ushort ChNum, const ushort *ChList, void *ParValue);
CAENHV_SetChParam = export_func(
    lib,
    'CAENHV_SetChParam',
    c_int,
    [
        c_int,  # handle
        c_ushort,  # slot
        c_char_p,  # ParName
        c_ushort,  # ChNum
        P(c_ushort),  # ChList
        c_void_p  # ParValue
    ],
    "Set channel parameter's value")
