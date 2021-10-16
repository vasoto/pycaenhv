from ctypes import POINTER, c_char, c_char_p, c_int, c_ushort, c_ubyte, c_void_p

from ._lib import load_lib
from .utils import export_func
from .constants import MAX_CH_NAME

P = POINTER
c_int_p = POINTER(c_int)

lib = load_lib()

# CAENHVLIB_API char *CAENHV_GetError(int handle);

CAENHV_GetError = export_func(lib, 'CAENHV_GetError', c_char_p, [c_int],
                              'Get error')

# CAENHVLIB_API CAENHVRESULT  CAENHV_GetChName(int handle, ushort slot,
#  ushort ChNum, const ushort *ChList, char (*ChNameList)[MAX_CH_NAME]);
NamesArrayType = P(c_char_p * MAX_CH_NAME)

CAENHV_GetChName = export_func(
    lib,
    'CAENHV_GetChName',
    c_int,
    [
        c_int,  # handle
        c_ushort,  # slot
        c_ushort,  # ChNum
        P(c_ushort),  # ChList
        # P(c_char_p) # ChNameList
        NamesArrayType
        # c_void_p
    ])

# CAENHVLIB_API CAENHVRESULT  CAENHV_SetChName(int handle, ushort slot,
#  ushort ChNum, const ushort *ChList, const char *ChName)

CAENHV_SetChName = export_func(
    lib,
    'CAENHV_SetChName',
    c_int,
    [
        c_int,  # handle
        c_ushort,  # slot
        c_ushort,  # ChNum
        P(c_ushort),  # ChList
        c_char_p  # ChName
    ],
    "Set Channel Name")
""" Set Channel Name
"""

CAENHV_GetExecCommList = export_func(
    lib,
    'CAENHV_GetExecCommList',
    c_int,
    [
        c_int,  # handle
        P(c_ushort),  # NummComm
        P(P(c_char))  # CommNameList
    ])
"""
Get the list of availble commands to execute.

* `handle` - Handle returned by the CAENHV_InitSystem function
* `NummComm` - Number of commands in the list
* `CommNameList` - List of the possible commands to send to the system. Memory pointed by `CommNameList` must be deallocated by the user.

### C Function Signature

```C
CAENHVLIB_API CAENHVRESULT  CAENHV_GetExecCommList(
    int handle,
    ushort *NumComm,
    char **CommNameList);
```
"""
CAENHV_ExecComm = export_func(
    lib,
    'CAENHV_ExecComm',
    c_int,  # result
    [
        c_int,  # handle
        c_char_p  # command
    ])
"""
Execute command

* `handle` - handle to module
* `CommName` - command name. For full list of commands for a given board see `CAENHV_GetExecCommList`.

### C Function Signature

```C
CAENHVLIB_API CAENHVRESULT  CAENHV_ExecComm(int handle, const char *CommName);
```
"""
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
