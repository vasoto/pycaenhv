from itertools import compress
from time import sleep
from typing import Any, List

from pycaenhv.constants import ChannelStatusLabels

from ..helpers import bitfield, channel_info, status_unpack
from ..wrappers import get_channel_name, get_channel_parameter, set_channel_name, set_channel_parameter
from ._channel_parameter import ChannelParameter


class Channel:
    """ Channel in a CAEN HV/LV board
    """
    def __init__(self, module, index: int):
        self.module = module
        self.index = index
        self.parameters = {
            p['name']: ChannelParameter(self, p['name'], p.copy())
            for p in channel_info(self.module.handle, self.module.slot,
                                  self.index)
        }

    def __str__(self) -> str:
        return f"Channel #{self.index}: {self.parameter_names}"

    def __repr__(self) -> str:
        return f"Channel({self.index}, {self.parameters})"

    @property
    def parameter_names(self):
        """ List all available parameters
        """
        return tuple(self.parameters.keys())

    @property
    def status(self) -> List[str]:
        """ Decodes channel status
        """
        status_raw: int = get_channel_parameter(self.module.handle,
                                                self.module.slot, self.index,
                                                'Status')
        return status_unpack(status_raw)

    @property
    def name(self) -> str:
        """ Get channel name
        """
        return get_channel_name(self.module.handle, self.module.slot,
                                self.index)

    @name.setter
    def name(self, name: str):
        """ Set channel name
        """
        set_channel_name(self.module.handle, self.module.slot, self.index,
                         name)
        # TODO: check if value is set
        sleep(0.5)

    def toggle(self, flag: bool) -> None:
        """ Toggle on or off
        """
        set_channel_parameter(self.module.handle, self.module.slot, self.index,
                              'Pw', int(flag))
        # TODO: wait until finished

    def switch_on(self) -> None:
        """ switch the channel ON
        """
        self.toggle(True)

    def switch_off(self) -> None:
        """ switch the channel OFF
        """
        self.toggle(False)

    def is_powered(self) -> bool:
        """ Returns True if the channel is ON, False otherwise
        """
        res = get_channel_parameter(self.module.handle, self.module.slot,
                                    self.index, 'Pw')
        return bool(res)

    def __getattr__(self, name: str) -> Any:
        """ Dynamically get attributes
        """
        if name in self.parameters and self.parameters[name].mode in ('R',
                                                                      'R/W'):
            return self.parameters[name]