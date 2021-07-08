from pathlib import Path
from typing import MutableMapping, Union, Any

import toml

from .enitites import Config


def read_toml_config(config_file: Union[str, Path]) -> Config:
    """ Read configuration from TOML file
    """
    conf = toml.load(config_file)
    return Config(**conf)