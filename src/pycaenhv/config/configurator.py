import logging
from typing import Dict, Any, Optional, Union

from ..context import HVContext
from ..helpers import get_channel_parameter, check_channel_parameter_value
from ..wrappers import set_channel_parameter, get_crate_map
from .enitites import HVBase, Channel

logger = logging.getLogger(__name__)


class ChannelConfigurator:
    def __init__(self, config: HVBase) -> None:
        self.config = config
        self.context: Union[HVContext, None] = None
        self._channels_count: Union[int, None] = None
        self.crate_map: Union[Dict[str, Any], None] = None

    def initialize(self):
        logger.info("Initialize configurator")
        arg = self.config.address
        logger.debug("Board=%s Link=%s Argument=%s", self.config.board,
                     self.config.link.name, str(arg))
        self.context = HVContext(system=self.config.board,
                                 link=self.config.link.name,
                                 argument=arg)
        self.context.start()
        self.crate_map = get_crate_map(self.context.handle)
        logger.debug("Configurator initialized. Found %d channels",
                     self.crate_map['channels'][self.config.slot])

    def finish(self):
        self.context.close()
        logger.info("Configurator finished")

    @property
    def channels_count(self) -> int:
        """ Get the number of channels in the module
        """
        if self.crate_map is None:
            self.initialize()
        return self.crate_map['channels'][self.config.slot]

    def _set_param(self, channel: int, parameter: str, value: Any) -> None:
        current_state = get_channel_parameter(self.context.handle,
                                              self.config.slot, channel, "Pw")
        if value != current_state:
            if not check_channel_parameter_value(
                    self.context.handle, self.config.slot, channel, parameter,
                    value):
                msg = f"Value for parameter {parameter} ({value}) is out of the allowed range."
                logger.error(msg)
                raise ValueError(msg)
            set_channel_parameter(self.context.handle, self.config.slot,
                                  channel, parameter, value)
            logger.debug("Parameter %s for channel %d set to %s", parameter,
                         channel, str(value))
        else:
            logger.debug(
                "Channel %d parameter %s already set to %s. Skipping...",
                channel, parameter, str(value))

    def _apply_config(self, channel: int, config: Channel) -> None:
        """ Apply channel configuration
        """
        logger.debug("Applying configuration")
        parameters = config.dict(exclude_none=True)  # Exclude unset fields
        for param, value in parameters.items():
            self._set_param(channel=channel, parameter=param, value=value)

    def configure(self):
        if self.context is None:
            raise ValueError("Context is not set, please initialize")
        channels_config = self.config.channels
        defaults = channels_config.default or {}
        configs = channels_config.channels or {}
        for channel in range(self.channels_count):
            conf = configs.get(channel, defaults)
            self._apply_config(channel, conf)

    def _switch_channel(self, channel: int, switch: bool):
        _switch = int(switch)
        self._set_param(channel, "Pw", _switch)

    def switch(self, value: bool):
        logger.info("Switch channels %s", {True: "ON", False: "OFF"}[value])
        for channel in range(self.channels_count):
            self._switch_channel(channel=channel, switch=value)
