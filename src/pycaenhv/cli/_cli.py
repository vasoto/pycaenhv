import json
import os
import sys
import logging
from typing import Optional

import click
from click import UsageError
from tabulate import tabulate

from pycaenhv.wrappers import get_channel_parameters, get_crate_map, set_channel_parameter, get_channel_parameter
from pycaenhv.context import HVContext
from pycaenhv.helpers import channel_info, check_channel_parameter, check_channel_parameter_value, is_parameter_readonly

_logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.option("--system",
              "-s",
              metavar="CAEN_SYSTEM_TYPE",
              envvar="CAENHV_SYSTEM",
              required=True,
              help="System type")
@click.option("--link",
              "-l",
              metavar="LINK_TYPE",
              envvar="CAENHV_LINK",
              required=True,
              help="Link type")
@click.option("--arg",
              "-a",
              metavar="Argument",
              envvar="CAENHV_ARGUMENT",
              required=True,
              help="Argument")
@click.option("--user",
              "-u",
              metavar="User",
              default='',
              envvar="CAENHV_USER",
              help="User name (if set)")
@click.option("--password",
              "-p",
              metavar="Password",
              default='',
              envvar="CAENHV_PASSWORD",
              help="Password (if set)")
@click.pass_context
def cli(ctx, system, link, arg, user, password):
    ctx.obj = HVContext(system, link, arg, user, password)


@cli.command("map", help="Display crate mapping")
@click.option("--json",
              "-j",
              'use_json',
              is_flag=True,
              help="export to JSON format")
@click.pass_obj
def crate_map(hv, use_json):
    with hv as cntx:
        crate_map = get_crate_map(cntx.handle)
        if use_json:
            print(json.dumps(crate_map, indent=4, sort_keys=True))
        else:
            del crate_map['slots']
            print(
                tabulate(crate_map,
                         headers='keys',
                         showindex="always",
                         tablefmt="fancy_grid"))


@click.group("channels", help="Channels information and settings")
def channels():
    pass


@channels.command("info")
@click.argument('slot', type=int)
@click.argument('channel', required=False, type=int)
@click.option("--json",
              "-j",
              'use_json',
              is_flag=True,
              help="export to JSON format")
@click.pass_obj
def info(hv, slot: int, channel: int, use_json):
    with hv as cntx:
        if channel is not None:
            info = channel_info(handle=cntx.handle, slot=slot, channel=channel)
            if use_json:
                result = dict(channel=channel, slot=slot, parameters=info)
                print(json.dumps(result, indent=4, sort_keys=True))
            else:
                print(
                    f"Channel {channel} in slot {slot} supports following parameters:\n"
                )

                print(tabulate(info, headers='keys', tablefmt='fancy_grid'))
        else:
            crate_map = get_crate_map(cntx.handle)
            num_channels = crate_map['channels'][slot]
            for ch in range(num_channels):
                parameters = get_channel_parameters(cntx.handle, slot, ch)
                print(f"{ch}: {parameters}")


@channels.command("set", help="Set parameter of channel(s)")
@click.argument('slot', type=int)
@click.argument('channel', required=False, type=int)
@click.argument('parameter', required=True, type=str)
@click.argument('value', required=True)
@click.pass_obj
def set_params(hv, slot: int, channel: int, parameter, value):
    """ Set parameter value
    """
    # 1. Check if parameter is available
    with hv as cntx:
        if not check_channel_parameter(cntx.handle, slot, channel, parameter):
            print(
                f"Error: Parameter {parameter} is not available for this channel"
            )
            exit()
    # 2. Check if parameter value is in range
        if not check_channel_parameter_value(cntx.handle, slot, channel,
                                             parameter, value):
            print(f"Error: Parameter {parameter} outside allowed margins")
            exit()
    # 3. Check if parameter is
        if is_parameter_readonly(cntx.handle, slot, channel, parameter):
            print(f"Parameter {parameter} is readonly.")
            exit()
        set_channel_parameter(cntx.handle, slot, channel, parameter, value)


@channels.command("get", help="Set parameter of channel(s)")
@click.argument('slot', type=int)
@click.argument('channel', required=False, type=int)
@click.argument('parameter', required=True, type=str)
@click.pass_obj
def get_params(hv, slot: int, channel: int, parameter):
    """ Get parameter value
    """
    # 1. Check if parameter is available
    with hv as cntx:
        if not check_channel_parameter(cntx.handle, slot, channel, parameter):
            print(
                f"Error: Parameter {parameter} is not available for this channel"
            )
            exit()
        value = get_channel_parameter(cntx.handle, slot, channel, parameter)
        print(f"{value}")


cli.add_command(channels)

# @cli.command(short_help="Initialize CAEN HV system")

# def initialize(system, link, arg):
#     handle = init_system(system_type=system, link_type=link, argument=arg)
