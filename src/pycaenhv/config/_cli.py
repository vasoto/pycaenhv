import argparse
import logging

from .configurator import ChannelConfigurator
from ._toml import read_toml_config

logger = logging.getLogger('configurator')


def parse_args():
    parser = argparse.ArgumentParser(description="Configure CAEN HV Modules")
    parser.add_argument('--verbose', action='store_true', help='verbose flag')
    parser.add_argument('filename', metavar="CONFIGFILE")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-on', action='store_const', dest='switch', const=True)
    group.add_argument('-off',
                       action='store_const',
                       dest='switch',
                       const=False)
    parser.set_defaults(switch=None)
    return parser.parse_args()


def main():
    args = parse_args()
    config = read_toml_config(args.filename)
    for conf_name, hv_conf in config.hv.items():
        logging.info("Applying configuration %s", conf_name)
        configurator = ChannelConfigurator(hv_conf)
        try:
            configurator.initialize()
            configurator.configure()
            if args.switch is not None:
                configurator.switch(args.switch)
        except Exception as err:
            logger.error("Error: %s", err)
        finally:
            configurator.finish()