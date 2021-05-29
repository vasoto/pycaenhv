import os

from pycaenhv.wrappers import init_system, deinit_system, get_board_parameters, get_crate_map
from pycaenhv.enums import CAENHV_SYSTEM_TYPE, LinkType
from pycaenhv.errors import CAENHVError


def main():
    system_type = CAENHV_SYSTEM_TYPE[os.environ['CAENHV_BOARD_TYPE']]
    link_type = LinkType[os.environ['CAENHV_LINK_TYPE']]
    handle = init_system(system_type, link_type,
                         os.environ['CAENHV_BOARD_ADDRESS'],
                         os.environ.get('CAENHV_USER', ''),
                         os.environ.get('CAENHV_PASSWORD', ''))
    try:
        print(f"Got handle: {handle}")
        crate_map = get_crate_map(handle)
        for name, value in crate_map.items():
            print(name, value)
        board_parameters = get_board_parameters(handle, 0)
        print(f"Board parameters: {board_parameters}")

    except CAENHVError as err:
        print(f"Got error: {err}\nExiting ...")
    finally:
        print("Deinitialize.")
        deinit_system(handle=handle)
    print("Bye bye.")


if __name__ == '__main__':
    """ Set environment variables
    CAENHV_BOARD_TYPE
    CAENHV_LINK_TYPE
    CAENHV_BOARD_ADDRESS
    CAENHV_USER (if set)
    CAENHV_PASSWORD (if set)
    """
    main()
