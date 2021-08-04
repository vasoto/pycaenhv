from typing import List, Any

from ..wrappers import get_crate_map, init_system, deinit_system
from ..enums import CAENHV_SYSTEM_TYPE, LinkType
from ._channel import Channel


class CaenHVModule:
    """ Represents a single CAEN HV/LV Module in a crate, determined by `slot`
    """
    def __init__(self):
        self.handle: int = None
        self.model: str = ''
        self.slot = -1
        self.channels: List[Channel] = list()
        self.connected: bool = False

    def connect(self,
                system: str,
                link: str,
                slot: int,
                argument: Any,
                user: str = '',
                password: str = '') -> None:
        """ Connect to CAEN HV/LV Module
        """
        system_ = CAENHV_SYSTEM_TYPE[system.upper()]
        link_ = LinkType[link.upper()]
        self.handle = init_system(system_type=system_,
                                  link_type=link_,
                                  argument=argument,
                                  username=user,
                                  password=password)

        self.slot = slot
        mapping = get_crate_map(self.handle)
        num_channels = mapping['channels'][self.slot]
        # Populate channels information
        self.channels = [Channel(self, ch) for ch in range(num_channels)]
        self.model = mapping['models'][self.slot]
        self.connected = True

    def disconnect(self) -> None:
        """ Terminate connection
        """
        if self.connected:
            deinit_system(self.handle)
            self.connected = False