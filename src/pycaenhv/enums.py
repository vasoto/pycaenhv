from enum import IntEnum


class CAENHV_SYSTEM_TYPE(IntEnum):
    SY1527 = 0
    SY2527 = 1
    SY4527 = 2
    SY5527 = 3
    N568 = 4
    V65XX = 5
    N1470 = 6
    V8100 = 7
    N568E = 8
    DT55XX = 9
    FTK = 10
    DT55XXE = 11
    N1068 = 12
    SMARTHV = 13
    NGPS = 14


class LinkType(IntEnum):
    """ Link Types for InitSystem
    """
    TCPIP = 0
    RS232 = 1
    CAENET = 2
    USB = 3
    OPTLINK = 4
    USB_VCP = 5
