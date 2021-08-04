from typing import List, Any

from ._channel import Channel


class CaenHVBoard:
    """ Represents a single CAEN HV/LV board in a crate, determined by `slot`
    """
    def __init__(self,
                 module,
                 slot: int,
                 num_channels: int,
                 model: str = '',
                 description: str = '',
                 serial_number: int = -1,
                 firmware_release=None):
        self.module = module
        self.description = description
        self.serial_number = serial_number
        self.firmware_release = firmware_release
        self.slot: int = slot
        self.model: str = model
        self.slot = slot
        self.num_channels = num_channels
        self.channels: List[Channel] = list()
        self.__init()

    @property
    def handle(self):
        return self.module.handle

    def __init(self):
        # Get the number of channels for this board
        # Populate channels information
        self.channels = [Channel(self, ch) for ch in range(self.num_channels)]
