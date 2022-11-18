class CAENHVError(Exception):
    pass


Errors = {
    0: "Command wrapper correctly executed",
    1: "Error of operatived system",
    2: "Write error in communication channel",
    3: "Read error in communication channel",
    4: "Time out in server communication",
    5: "Command Front End application is down",
    6: "Communication with system not yet connected by a Login command",
    7: "Communication with a not present board/slot",
    8: "Communication with RS232 not yet implemented",
    9: "User memory not sufficient",
    10: "Value out of range",
    11: "Execute command not yet implemented",
    12: "Get Property not yet implemented",
    13: "Set Property not yet implemented",
    14: "Property not found",
    15: "Execute command not found",
    16: "No System property",
    17: "No get property",
    18: "No set property",
    19: "No execute command",
    20: "Device configuration changed",
    21: "Property of param not found",
    22: "Param not found",
    23: "No data present",
    24: "Device already open",
    25: "To Many devices opened",
    26: "Function Parameter not valid",
    27: "Function not available for the connected device",
    0x1001: "Device already connected",
    0x1002: "Device not connected",
    0x1003: "Operating system error",
    0x1004: "Login failed ",
    0x1005: "Logout failed",
    0x1006: "Link type not supported",
    0x1007: "Login failed for username/password ( SY4527 / SY5527 )",
}


def check_function_output(command_output: int,
                          should_raise: bool = True) -> bool:
    """ Checks the output of CAEN HV command and print error message
    """
    if command_output != 0:
        err_msg = Errors[command_output]
        if should_raise:
            raise CAENHVError(err_msg)
        print(f"Error: {err_msg}")
        return False
    return True


# TODO: Add decorator
