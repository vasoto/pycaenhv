from itertools import compress
from time import sleep
from typing import Any, List

from pycaenhv.constants import ChannelStatusLabels

from ..helpers import bitfield, channel_info
from ..wrappers import get_channel_name, get_channel_parameter, set_channel_name
from ._channel_parameter import ChannelParameter


class Channel:
    """ Channel in a CAEN HV/LV module
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
        status_raw: int = get_channel_parameter(self.module.handle,
                                                self.module.slot, self.index,
                                                'Status')
        mask = bitfield(status_raw)
        value = compress(ChannelStatusLabels, mask)
        return list(value)

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

    def __getattr__(self, name: str) -> Any:
        """ Dynamically get attributes
        """
        if name in self.parameters and self.parameters[name].mode in ('R',
                                                                      'R/W'):
            return self.parameters[name]