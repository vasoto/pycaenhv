import time
from typing import Dict, Any

from ..wrappers import get_channel_parameter, set_channel_parameter


class ChannelParameter:
    """ Parameter of CAEN HV/LV board channel
    """
    def __init__(self, channel, name: str, attributes: Dict) -> None:
        self.channel = channel
        self.name = name
        # Set available attributes for a given parameter
        self.attributes = attributes
        # Remove duplicated or static info
        if 'value' in self.attributes:
            del self.attributes['value']
        if 'name' in self.attributes:
            del self.attributes['name']

    def __str__(self) -> str:
        return f"{self.name}: {self.attributes}"

    def __repr__(self) -> str:
        return f"ChannelParameter({self.__str__()})"

    @property
    def value(self) -> Any:
        """ Reads (if possible) the value of a parameter from the board's channel
        """
        if 'R' in self.attributes['mode']:
            return get_channel_parameter(self.channel.module.handle,
                                         self.channel.module.slot,
                                         self.channel.index, self.name)
        else:
            raise ValueError(
                f"Trying to read write-only parameter {self.name}")

    @value.setter
    def value(self, value: Any) -> None:
        """ Writes (if possible) parameter value to the board
        """
        if 'W' in self.attributes['mode']:
            if value > self.attributes['max']:
                raise ValueError(
                    f"Value {value} for {self.name} is too big. Maximum value is {self.attributes['max']}"
                )
            if value < self.attributes['min']:
                raise ValueError(
                    f"Value {value} for {self.name} is too small. Minimum value is {self.attributes['min']}"
                )
            set_channel_parameter(self.channel.module.handle,
                                  self.channel.module.slot, self.channel.index,
                                  self.name, value)
            # TODO: Implement wait until param is set
            time.sleep(1)
        else:
            raise ValueError(
                f"Trying to write read-only parameter {self.name}")

    def __getattr__(self, name: str) -> Any:
        """ Dynamically reads preset attributes
        """
        if name in self.attributes:
            return self.attributes[name]
